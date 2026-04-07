from flask import Flask, request, jsonify
from flask_cors import CORS
from environment.debt_env import DebtEnv
from models.schemas import Action, State
import os
import base64
import json

app = Flask(__name__)
CORS(app) # Enable CORS for frontend integration

# Global environment instance
env = DebtEnv()

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "active", "service": "legal-guardian-ai"})

@app.route("/reset", methods=["POST"])
def reset():
    data = request.json or {}
    scenario = data.get("scenario", "easy")
    try:
        obs = env.reset(scenario)
        return jsonify(obs.dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/analyze", methods=["POST"])
def analyze():
    # Handle both multipart and JSON for flexiblity
    if request.content_type.startswith('multipart/form-data'):
        complaint = request.form.get("complaint", "")
        scenario = request.form.get("scenario", "easy")
        image_file = request.files.get("evidence")
        image_data = None
        if image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
    else:
        data = request.json or {}
        complaint = data.get("complaint", "")
        scenario = data.get("scenario", "easy")
        image_data = data.get("image_data")

    try:
        # 1. Initialize environment properly for subsequent /step calls
        from environment.state_manager import init_state
        env.reset(scenario) # This sets env.current_state and env.session_id
        current_state = env.current_state
        
        # 2. Call AI Agent with vision capability
        from agents.ai_lawyer import ai_agent
        action = Action(action_type="initial_analysis", content=complaint)
        ai_response_json = ai_agent(action, current_state, image_data)
        
        # Robust JSON parsing
        import re
        try:
            ai_data = json.loads(ai_response_json)
        except json.JSONDecodeError:
            match = re.search(r"```json\s*(.*?)\s*```", ai_response_json, re.DOTALL)
            if match:
                ai_data = json.loads(match.group(1))
            else:
                ai_data = {"action": "negotiation", "reasoning": "Parse failure", "reply": ai_response_json}

        # 3. Update state based on AI analysis (simulated resolution step)
        from agents.lender_agent import lender_agent
        from environment.state_manager import update_state
        lender_output = lender_agent(current_state, ai_response_json)
        
        prev_state = current_state.copy(deep=True)
        env.current_state = update_state(current_state, ai_response_json, lender_output)
        
        # 4. Persistence
        from db.session_repo import update_session
        from db.log_repo import add_log
        from environment.reward_engine import calculate_reward
        
        reward = calculate_reward(prev_state, env.current_state)
        update_session(env.session_id, env.current_state, False)
        add_log(env.session_id, env.current_state.steps, ai_response_json, lender_output, reward)

        return jsonify({
            "state": env.current_state.dict(),
            "ai_decision": ai_data,
            "lender_response": lender_output,
            "session_id": env.session_id
        })
    except Exception as e:
        import traceback
        error_msg = f"Error in /analyze: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        return jsonify({"error": error_msg, "traceback": traceback.format_exc()}), 500

@app.route("/step", methods=["POST"])
def step():
    data = request.json
    if not data:
        return jsonify({"error": "Missing action data"}), 400
        
    try:
        action = Action(**data)
        result = env.step(action)
        return jsonify(result.dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/state", methods=["GET"])
def state():
    if env.current_state:
        return jsonify(env.current_state.dict())
    return jsonify({"error": "Environment not reset"}), 400

@app.route("/sessions", methods=["GET"])
def sessions():
    try:
        from db.session_repo import list_sessions
        limit = request.args.get("limit", default=10, type=int)
        return jsonify(list_sessions(limit))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/scenarios", methods=["GET"])
def scenarios():
    try:
        from environment.scenario_generator import get_all_scenarios
        return jsonify(get_all_scenarios())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/report/<session_id>", methods=["GET"])
def report(session_id):
    try:
        from db.session_repo import get_session
        from db.log_repo import get_logs
        from utils.report import EvalReport
        
        session = get_session(session_id)
        if not session:
            return jsonify({"error": "Session not found"}), 404
            
        logs = get_logs(session_id)
        
        # We need a State object for the report generator
        from models.schemas import State
        final_state = State(**session["state"])
        
        report_gen = EvalReport(session_id, final_state.scenario)
        report_data = report_gen.generate(final_state, logs)
        
        return jsonify(report_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/logs/<session_id>", methods=["GET"])
def logs(session_id):
    try:
        from db.log_repo import get_logs
        return jsonify(get_logs(session_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    app.run(host="0.0.0.0", port=port)