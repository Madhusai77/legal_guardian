from models.schemas import State
import json

def lender_agent(state: State, ai_output: str) -> str:
    ai_lower = ai_output.lower()
    
    # Try to parse AI output for structured rules
    ai_action = "unknown"
    try:
        ai_data = json.loads(ai_output)
        ai_action = ai_data.get("action", "unknown")
    except:
        ai_action = "negotiation" if "negotiat" in ai_lower else "unknown"

    # Deterministic adaptive logic
    if ai_action == "legal_notice" or "legal notice" in ai_lower:
        if state.compliance_score > 0.7:
            return "We have received your legal notice. We are willing to halt collection activities and discuss a fair settlement."
        else:
            return "Your legal notice is noted. However, the debt remains valid. Prove the violations or pay immediately."

    if ai_action == "settlement" or "settle" in ai_lower:
        if state.user_stress > 0.8:
            return "We can offer a 20% waiver for immediate payment. This is our final offer before legal escalation."
        return "We are open to settlement. Please provide your proposed amount for review."

    if ai_action == "complaint" or "rbi" in ai_lower:
        return "We operate within RBI guidelines. Any false complaints will be contested."

    # Default behaviors based on harassment level
    if state.harassment_level == "critical":
        if state.compliance_score < 0.4:
            return "Immediate payment required to avoid physical verification at your registered address."
        return "Final warning. Clear the dues by end of day."
    
    if state.harassment_level == "high":
        return "Your account is severely past due. Expect calls to all provided references."

    return "This is a reminder to clear your outstanding dues to avoid impact on your credit score."