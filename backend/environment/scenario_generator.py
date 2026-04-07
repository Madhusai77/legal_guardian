from environment.state_manager import init_state

def get_scenario(difficulty="easy"):
    """
    Returns the initial state and metadata for a given task difficulty.
    """
    state = init_state(difficulty)
    scenarios = get_all_scenarios()
    return state, scenarios.get(difficulty, scenarios["easy"])

def get_all_scenarios():
    return {
        "easy": {
            "name": "Initial Harassment",
            "description": "User is receiving aggressive calls from a lender. Goal: Reduce harassment level.",
            "target_reward": 0.6
        },
        "medium": {
            "name": "Legal Threat Resolution",
            "description": "Lender has sent a formal notice. Goal: Negotiate and achieve escalation reduction.",
            "target_reward": 0.7
        },
        "hard": {
            "name": "Court Case Avoidance",
            "description": "Court summons is imminent. Goal: Final debt settlement and case closure.",
            "target_reward": 0.8
        }
    }