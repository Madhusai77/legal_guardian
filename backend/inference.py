import os
import textwrap
import asyncio
from typing import List
from openai import OpenAI

# Required Environment Variables
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")
API_KEY = os.environ.get("HF_TOKEN") or os.environ.get("OPENAI_API_KEY") or "dummy-key"
TEMPERATURE = 0.7
MAX_TOKENS = 150
MAX_STEPS = 10
BENCHMARK = "debt-harassment-legal-ai"
SYSTEM_PROMPT = "You are a legal AI agent aiming to mitigate debt harassment. Act professionally and effectively."

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

def build_user_prompt(step: int, last_message: str, last_reward: float, history: List[str]) -> str:
    history_block = "\n".join(history[-4:]) if history else "None"
    return textwrap.dedent(
        f"""
        Step: {step}
        Observation message: {last_message!r}
        Last reward: {last_reward:.2f}
        History:
        {history_block}
        Send your next legal action or negotiation message.
        """
    ).strip()

def get_model_message(client: OpenAI, step: int, last_message: str, last_reward: float, history: List[str]) -> str:
    user_prompt = build_user_prompt(step, last_message, last_reward, history)
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=False,
        )
        text = (completion.choices[0].message.content or "").strip()
        return text if text else "negotiation"
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return "I will attempt to negotiate a fair outcome."

async def run_scenario(client, scenario_name, task_name):
    # Instantiate the local environment directly
    from environment.debt_env import DebtEnv
    from models.schemas import Action
    
    env = DebtEnv()
    
    history: List[str] = []
    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=task_name, env=BENCHMARK, model=MODEL_NAME)
    
    try:
        obs = env.reset(scenario_name)
        last_message = obs.message
        last_reward = 0.0
        
        for step in range(1, MAX_STEPS + 1):
            if env._check_done():
                break

            message = get_model_message(client, step, last_message, last_reward, history)
            
            action_type = "negotiation"
            lower_msg = message.lower()
            if "cease" in lower_msg or "notice" in lower_msg or "legal" in lower_msg:
                action_type = "legal_notice"
            elif "complaint" in lower_msg or "regulator" in lower_msg:
                action_type = "complaint"
            elif "settle" in lower_msg:
                action_type = "settlement"
                
            action = Action(action_type=action_type, content=message)
            
            result = env.step(action)
            obs = result.observation
            reward = result.reward
            done = result.done

            rewards.append(reward)
            steps_taken = step
            last_message = obs.message
            last_reward = reward
            
            history.append(f"Action: {action_type} - {message}")
            history.append(f"Env: {last_message}")
            
            # STDOUT logging required format
            print(f"[STEP] step={step} reward={reward:.2f} done={str(done).lower()}", flush=True)
            
            if done:
                success = obs.state.resolution_status == "resolved"
                break
                
        # Grading logic can be handled centrally via OpenEnv, but for inference local validation we do:
        # average reward for score as baseline.
        score = sum(rewards) / max(1, steps_taken)
        log_end(success, steps_taken, score, rewards)
        
    except Exception as e:
        print(f"[DEBUG] Error running scenario {scenario_name}: {e}", flush=True)
        log_end(success=False, steps=steps_taken, score=0.0, rewards=rewards)
        
async def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    
    # Sequentially run the 3 required OpenEnv tasks
    await run_scenario(client, "easy", "Harassment Mitigation")
    await run_scenario(client, "medium", "Legal Escalation Control")
    await run_scenario(client, "hard", "Debt Settlement")

if __name__ == "__main__":
    asyncio.run(main())