import os
import textwrap
from openai import OpenAI
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY") or "dummy-key"
BASE_URL = "http://localhost:7860" # Local docker bound port
BENCHMARK = "debt-harassment-legal-ai"

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

def run_task(scenario_name: str, task_name: str):
    # One [START] line at episode begin
    print(f"[START] task={task_name} env={BENCHMARK} model={MODEL_NAME}", flush=True)
    
    rewards = []
    success = False
    score = 0.0
    steps_taken = 0
    error_msg = "null"

    try:
        # Reset the environment
        res = requests.post(f"{BASE_URL}/reset", params={"scenario": scenario_name}, json={"scenario": scenario_name}, timeout=15)
        res.raise_for_status()
        state_data = res.json()
        
        current_state_info = state_data.get('state', {})
        last_message = state_data.get('message', 'Initiating interaction...')

        for step in range(1, 11): # Up to 10 steps to resolve
            prompt = f"State details: {current_state_info}. Last message from lender: {last_message}. What is your legal/negotiation response? Output a single action string."

            # Call LLM
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}]
            )

            action_str = response.choices[0].message.content.replace('\n', ' ').strip()
            
            # Execute Step via HTTP
            step_res = requests.post(f"{BASE_URL}/step", params={"action": action_str}, json={"action": action_str}, timeout=15)
            step_res.raise_for_status()
            result = step_res.json()

            reward = result.get('reward', 0.0)
            done = result.get('done', False)
            rewards.append(reward)
            steps_taken = step
            
            error_val = "null"
            if "error" in result:
                error_val = str(result["error"])

            print(f"[STEP] step={step} action={action_str} reward={reward:.2f} done={str(done).lower()} error={error_val}", flush=True)
            
            if done:
                obs = result.get('observation', {})
                current_state_info = obs.get('state', {})
                # Check actual success status from environment state
                if current_state_info.get("resolution_status") == "resolved":
                    success = True
                break
                
            obs = result.get('observation', {})
            current_state_info = obs.get('state', {})
            last_message = obs.get('message', '')

    except Exception as e:
        error_msg = str(e).replace('\n', ' ')
        print(f"[STEP] step={steps_taken+1} action=error reward=0.00 done=true error={error_msg}", flush=True)
        # We append a 0.0 reward for the failed step to ensure arrays map correctly
        rewards.append(0.00)
    
    finally:
        # One [END] line after env.close(), always emitted
        if steps_taken == 0:
            steps_taken = 1
            
        score = sum(rewards) / steps_taken
        rewards_str = ",".join(f"{r:.2f}" for r in rewards) if rewards else "0.00"
        
        print(f"[END] success={str(success).lower()} steps={steps_taken} score={score:.2f} rewards={rewards_str}", flush=True)

if __name__ == "__main__":
    # We loop over the 3 tasks required by OpenEnv
    run_task("easy", "harassment-mitigation")
    run_task("medium", "legal-escalation-control")
    run_task("hard", "debt-settlement")