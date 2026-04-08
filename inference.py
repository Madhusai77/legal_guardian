import os
from openai import OpenAI
import requests

BASE_URL = "http://localhost:7860"

# OpenAI Client using standard OpenEnv injected variables
client = OpenAI(
    base_url=os.getenv("API_BASE_URL", "https://api.openai.com/v1"),
    api_key=os.getenv("HF_TOKEN", "dummy-key")
)

def run_task(scenario_name: str):
    print("[START]")
    try:
        # Reset the environment
        res = requests.post(f"{BASE_URL}/reset", json={"scenario": scenario_name})
        state = res.json()
        
        current_state_info = state.get('state', {})
        last_message = state.get('message', 'Initiating interaction...')

        for step in range(1, 11): # Up to 10 steps to resolve
            prompt = f"State details: {current_state_info}. Last message from lender: {last_message}. What is your legal/negotiation response? Keep it professional."

            response = client.chat.completions.create(
                model=os.getenv("MODEL_NAME", "gpt-3.5-turbo"),
                messages=[{"role": "user", "content": prompt}]
            )

            action = response.choices[0].message.content

            # Derive formal action_type for backend typing
            action_type = "negotiation"
            lower_msg = action.lower()
            if "cease" in lower_msg or "notice" in lower_msg:
                action_type = "legal_notice"
            elif "complaint" in lower_msg:
                action_type = "complaint"
            elif "settle" in lower_msg:
                action_type = "settlement"

            # Execute Step via HTTP
            result = requests.post(f"{BASE_URL}/step", json={
                "action_type": action_type,
                "content": action
            }).json()

            reward = result.get('reward', 0.0)
            print(f"[STEP] action={action_type} reward={reward:.2f}")
            
            if result.get('done'):
                break
                
            obs = result.get('observation', {})
            current_state_info = obs.get('state', {})
            last_message = obs.get('message', '')

    except Exception as e:
        print(f"Error during inference: {e}")
        
    print("[END]")

if __name__ == "__main__":
    # We loop over the 3 tasks required by OpenEnv
    for scenario in ["easy", "medium", "hard"]:
        run_task(scenario)