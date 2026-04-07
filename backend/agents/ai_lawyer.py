from openai import OpenAI
import os
import json
import base64
from models.schemas import Action, State
from environment.rbi_context import get_rbi_context

# Initialize OpenAI client with fallback for local testing
client = OpenAI(
    base_url=os.getenv("API_BASE_URL", "https://api.openai.com/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "your-api-key")
)

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

SYSTEM_PROMPT = f"""
You are a senior Indian legal expert specializing in consumer protection and debt harassment laws.
Your goal is to protect the user from illegal harassment while ensuring legal compliance.

{get_rbi_context()}

Available legal frameworks:
1. RBI Fair Practices Code for Lenders
2. Consumer Protection Act, 2019
3. Indian Penal Code (IPC) Sections 503, 506 (Criminal Intimidation)

INSTRUCTIONS:
- Identify specific violations (e.g., Clause 2: Contacting after 7 PM).
- Explain legal terms for a 'common person' who doesn't understand the level of the case.
- Provide a clear 'Generated Reply' for the user to send to the lender.
- Analyze any uploaded evidence (screenshots of SMS/Calls) for tone, timing, and content.

You must respond ONLY in structured JSON format:
{{
  "action": "legal_notice" | "negotiation" | "complaint" | "settlement",
  "reasoning": "Detailed legal reasoning in plain English",
  "legal_citations": ["Clause X of RBI FPC", "Section Y of IPC"],
  "reply": "The actual message to be sent to the lender",
  "risk_assessment": "low" | "medium" | "high",
  "harassment_type": ["Abusive Language", "Privacy Violation", etc.],
  "suggested_next_step": "Text for what to do if lender doesn't comply"
}}
"""

def ai_agent(action: Action, state: State, image_data: str = None) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    
    user_content = [
        {
            "type": "text", 
            "text": f"""
                Current State:
                - Harassment Level: {state.harassment_level}
                - Legal Stage: {state.legal_stage}
                - Compliance Score: {state.compliance_score}
                - User Stress: {state.user_stress}
                
                User Input Action:
                Type: {action.action_type}
                Content: {action.content}
                
                Recent History:
                {state.history[-2:] if state.history else "None"}

                Analyze based on RBI guidelines and evidence.
            """
        }
    ]

    if image_data:
        user_content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
        })
    
    messages.append({"role": "user", "content": user_content})

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.2,
            max_tokens=600,
            response_format={"type": "json_object"}
        )

        return response.choices[0].message.content

    except Exception as e:
        fallback = {
            "action": "negotiation",
            "reasoning": f"Fallback due to error: {str(e)}",
            "legal_citations": ["General Consumer Rights"],
            "reply": "I am reviewing your request. Please ensure all communication is in writing.",
            "risk_assessment": "medium",
            "harassment_type": ["Unknown"],
            "suggested_next_step": "Wait for system recovery"
        }
        return json.dumps(fallback)