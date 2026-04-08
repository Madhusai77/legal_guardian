from models.schemas import State

def calculate_reward(prev_state: State, new_state: State) -> float:
    reward = 0.0
    
    # factor 1: harassment reduction (up to 0.3)
    if prev_state.harassment_level != new_state.harassment_level:
        if new_state.harassment_level == "none":
            reward += 0.3
        elif new_state.harassment_level == "low":
            reward += 0.2
            
    # factor 2: legal compliance & stage progression (up to 0.3)
    if new_state.compliance_score > prev_state.compliance_score:
        reward += 0.2
    
    if new_state.legal_stage != prev_state.legal_stage:
        reward += 0.1
        
    # factor 3: resolution achievement (up to 0.4)
    if new_state.resolution_status == "resolved":
        reward += 0.4
        # efficiency bonus
        if new_state.steps < 5:
            reward += 0.1
            
    # factor 4: user stress reduction
    if new_state.user_stress < prev_state.user_stress:
        reward += 0.1
        
    # Penalties
    # penalty for high stress
    if new_state.user_stress > 0.8:
        reward -= 0.1
        
    # penalty for inefficiency
    if new_state.steps > 8:
        reward -= 0.2
        
    # clamp
    return float(max(0.0, min(1.0, reward)))