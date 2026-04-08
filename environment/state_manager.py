from models.schemas import State
import json

def init_state(scenario="easy"):
    # Scenarios: easy, medium, hard
    scenarios = {
        "easy": {
            "harassment_level": "medium",
            "legal_stage": "pre-legal",
            "user_stress": 0.4
        },
        "medium": {
            "harassment_level": "high",
            "legal_stage": "notices-sent",
            "user_stress": 0.7
        },
        "hard": {
            "harassment_level": "critical",
            "legal_stage": "court-summons",
            "user_stress": 0.9
        }
    }
    
    config = scenarios.get(scenario, scenarios["easy"])
    
    return State(
        harassment_level=config["harassment_level"],
        legal_stage=config["legal_stage"],
        resolution_status="unresolved",
        user_stress=config["user_stress"],
        steps=0,
        history=[],
        scenario=scenario,
        compliance_score=0.5
    )

def update_state(state: State, ai_output, lender_output) -> State:
    state.steps += 1
    
    # Try to parse AI output if it's JSON
    ai_action = "unknown"
    try:
        ai_data = json.loads(ai_output)
        ai_action = ai_data.get("action", "unknown")
    except:
        ai_action = ai_output[:50]

    state.history.append({
        "step": state.steps,
        "ai": ai_output,
        "lender": lender_output,
        "ai_action": ai_action
    })

    # Logic for state transitions
    ai_lower = ai_output.lower()
    lender_lower = lender_output.lower()

    # Harassment reduction logic
    if "legal notice" in ai_lower or "complaint" in ai_lower:
        state.compliance_score = min(1.0, state.compliance_score + 0.1)
        if "cease" in lender_lower or "stop" in lender_lower:
            state.harassment_level = "low"
            state.user_stress = max(0.0, state.user_stress - 0.2)
    
    # Legal stage transitions
    if "court" in ai_lower:
        state.legal_stage = "litigation"
    elif "arbitration" in ai_lower:
        state.legal_stage = "arbitration"

    # Resolution logic
    if "settle" in lender_lower or "closed" in lender_lower or "resolved" in ai_lower:
        if state.compliance_score > 0.6:
            state.resolution_status = "resolved"
            state.harassment_level = "none"
            state.user_stress = 0.0

    # Stress management
    if state.harassment_level == "critical":
        state.user_stress = min(1.0, state.user_stress + 0.1)
    
    return state