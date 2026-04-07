from models.schemas import State

def easy_task_grader(state: State) -> float:
    """
    Goal: Reduce harassment level from medium to low/none.
    """
    score = 0.0
    if state.harassment_level == "none":
        score = 1.0
    elif state.harassment_level == "low":
        score = 0.8
    elif state.harassment_level == "medium":
        score = 0.4
    else:
        score = 0.1
    return float(max(0.0, min(1.0, score)))

def medium_task_grader(state: State) -> float:
    """
    Goal: High compliance score and legal stage progression.
    """
    score = 0.0
    # Compliance weight: 0.5
    score += state.compliance_score * 0.5
    
    # Stage progression weight: 0.5
    if state.legal_stage in ["arbitration", "litigation"]:
        score += 0.5
    elif state.legal_stage == "notices-sent":
        score += 0.2
        
    return float(max(0.0, min(1.0, score)))

def hard_task_grader(state: State) -> float:
    """
    Goal: Full resolution within 8 steps with low stress.
    """
    if state.resolution_status != "resolved":
        return 0.2 * (1.0 - state.user_stress)
    
    score = 0.6 # Base score for resolution
    
    # Efficiency bonus
    if state.steps <= 6:
        score += 0.3
    elif state.steps <= 8:
        score += 0.2
        
    # Stress penalty reduction
    score += (1.0 - state.user_stress) * 0.1
    
    return float(max(0.0, min(1.0, score)))