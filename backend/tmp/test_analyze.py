import json
import base64
import os
import sys

# Mocking absolute paths for imports
sys.path.append(os.getcwd())

from models.schemas import Action, State
from environment.state_manager import init_state, update_state
from agents.lender_agent import lender_agent
from agents.ai_lawyer import ai_agent

def test_analyze_flow():
    print("Testing /analyze simulation flow...")
    scenario = "easy"
    complaint = "The lender is calling me at 11 PM."
    image_data = None
    
    try:
        # 1. Init state
        current_state = init_state(scenario)
        print("State initialized.")
        
        # 2. Call AI agent (mocked response if key missing)
        action = Action(action_type="initial_analysis", content=complaint)
        print("Calling AI Agent...")
        ai_response_json = ai_agent(action, current_state, image_data)
        print(f"AI Response received: {ai_response_json[:100]}...")
        
        # 3. Robust JSON parsing
        import re
        try:
            ai_data = json.loads(ai_response_json)
        except json.JSONDecodeError:
            match = re.search(r"```json\s*(.*?)\s*```", ai_response_json, re.DOTALL)
            if match:
                ai_data = json.loads(match.group(1))
            else:
                ai_data = {"action": "negotiation", "reasoning": "Parse failure"}
        print("AI JSON parsed.")

        # 4. Lender Agent
        print("Calling Lender Agent...")
        lender_output = lender_agent(current_state, ai_response_json)
        print(f"Lender Output: {lender_output}")

        # 5. Update State
        print("Updating State...")
        new_state = update_state(current_state, ai_response_json, lender_output)
        print(f"New state steps: {new_state.steps}")
        
        print("FLOW SUCCESS!")
    except Exception as e:
        import traceback
        print(f"FLOW FAILED: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    test_analyze_flow()
