import json
from typing import List, Dict, Any

class EvalReport:
    def __init__(self, session_id: str, scenario: str):
        self.session_id = session_id
        self.scenario = scenario
        self.metrics = {
            "total_steps": 0,
            "final_reward": 0.0,
            "harassment_reduction": 0.0,
            "compliance_improvement": 0.0,
            "resolution_success": False
        }

    def generate(self, final_state: Any, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        self.metrics["total_steps"] = final_state.steps
        self.metrics["final_reward"] = sum([h.get("reward", 0) for h in history]) / len(history) if history else 0
        self.metrics["resolution_success"] = final_state.resolution_status == "resolved"
        self.metrics["compliance_improvement"] = final_state.compliance_score - 0.5
        
        report = {
            "session_id": self.session_id,
            "scenario": self.scenario,
            "performance_metrics": self.metrics,
            "status": "COMPLETED" if self.metrics["resolution_success"] else "FAILED",
            "summary": f"Task {self.scenario} finished in {self.metrics['total_steps']} steps with {self.metrics['final_reward']:.2f} average reward."
        }
        return report

def save_report(report: Dict[str, Any], path: str):
    with open(path, "w") as f:
        json.dump(report, f, indent=2)