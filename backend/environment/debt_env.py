from models.schemas import Observation, StepResult, Action, State
from environment.state_manager import init_state, update_state
from environment.reward_engine import calculate_reward
from agents.ai_lawyer import ai_agent
from agents.lender_agent import lender_agent
from db.session_repo import create_session, update_session
from db.log_repo import add_log

class DebtEnv:
    def __init__(self):
        self.current_state: State = None
        self.session_id: str = None

    def reset(self, scenario="easy") -> Observation:
        self.current_state = init_state(scenario)
        self.session_id = create_session(self.current_state)
        
        return Observation(
            state=self.current_state,
            message=f"Environment reset for {scenario} scenario",
            available_actions=["legal_notice", "negotiation", "complaint", "settlement"]
        )

    def step(self, action: Action) -> StepResult:
        if self.current_state is None:
            raise ValueError("Environment must be reset before calling step()")
            
        prev_state = self.current_state.copy(deep=True)

        # Multi-agent simulation
        ai_output = ai_agent(action, self.current_state)
        lender_output = lender_agent(self.current_state, ai_output)

        # Update environment state
        self.current_state = update_state(self.current_state, ai_output, lender_output)

        # Calculate reward
        reward = calculate_reward(prev_state, self.current_state)
        
        # Check for episode termination
        done = self._check_done()

        # Persistent storage & logging
        update_session(self.session_id, self.current_state, done)
        add_log(self.session_id, self.current_state.steps, ai_output, lender_output, reward)

        return StepResult(
            observation=Observation(
                state=self.current_state,
                message=f"Action processed. AI: {ai_output[:50]}... | Lender: {lender_output[:50]}...",
                available_actions=["legal_notice", "negotiation", "complaint", "settlement"]
            ),
            reward=reward,
            done=done,
            info={
                "session_id": self.session_id,
                "steps": self.current_state.steps
            }
        )

    def state(self) -> State:
        return self.current_state

    def _check_done(self) -> bool:
        if self.current_state.resolution_status == "resolved":
            return True
        if self.current_state.steps >= 10:
            return True
        if self.current_state.user_stress >= 1.0:
            return True
        return False