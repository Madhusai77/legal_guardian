from models.schemas import State
from tasks import easy_task_grader, medium_task_grader, hard_task_grader

def test_graders():
    print("Testing Graders:")
    
    # State for easy task
    s_easy = State(
        harassment_level="none",
        legal_stage="pre-legal",
        resolution_status="resolved",
        user_stress=0.0,
        steps=5,
        history=[],
        scenario="easy",
        compliance_score=0.8
    )
    print(f"Easy Grader: {easy_task_grader(s_easy)}")
    
    # State for medium task
    s_medium = State(
        harassment_level="low",
        legal_stage="litigation",
        resolution_status="unresolved",
        user_stress=0.4,
        steps=7,
        history=[],
        scenario="medium",
        compliance_score=0.9
    )
    print(f"Medium Grader: {medium_task_grader(s_medium)}")
    
    # State for hard task
    s_hard = State(
        harassment_level="none",
        legal_stage="litigation",
        resolution_status="resolved",
        user_stress=0.1,
        steps=6,
        history=[],
        scenario="hard",
        compliance_score=1.0
    )
    print(f"Hard Grader: {hard_task_grader(s_hard)}")

if __name__ == "__main__":
    test_graders()
