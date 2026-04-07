import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Shield, AlertTriangle, Activity } from "lucide-react";

interface EnvironmentStatePanelProps {
  state: any;
}

const EnvironmentStatePanel = ({ state }: EnvironmentStatePanelProps) => {
  if (!state) return (
    <Card className="rounded-2xl shadow-md flex items-center justify-center min-h-[350px] border-dashed border-2">
      <div className="text-center p-6 space-y-3">
        <Activity className="h-10 w-10 text-muted-foreground/20 mx-auto animate-pulse" />
        <p className="text-sm text-muted-foreground italic">Awaiting AI Environment Analysis...</p>
      </div>
    </Card>
  );

  const getHarassmentColor = (level: string) => {
    const l = level.toLowerCase();
    if (l === "critical") return "bg-red-500 hover:bg-red-600";
    if (l === "high") return "bg-orange-500 hover:bg-orange-600";
    if (l === "medium") return "bg-yellow-500 hover:bg-yellow-600";
    return "bg-green-500 hover:bg-green-600";
  };

  const getStressColor = (val: number) => {
    if (val > 0.8) return "bg-red-500";
    if (val > 0.5) return "bg-orange-500";
    return "bg-green-500";
  };

  return (
    <Card className="rounded-2xl shadow-md border-primary/10 overflow-hidden">
      <CardHeader className="pb-3 border-b border-border/50 bg-muted/30">
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          <Shield className="h-5 w-5 text-primary" />
          Environment State
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6 pt-5">
        <div className="flex justify-between items-center bg-muted/20 p-3 rounded-xl border border-border/50">
          <span className="text-sm font-medium">Harassment Level</span>
          <Badge className={`${getHarassmentColor(state.harassment_level)} capitalize px-3 py-1`}>
            {state.harassment_level}
          </Badge>
        </div>

        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm font-medium">Recorded User Stress</span>
            <div className="flex items-center gap-1.5">
              <span className={`text-xs font-bold ${(state.user_stress > 0.7) ? 'text-red-500' : 'text-primary'}`}>
                {(state.user_stress * 100).toFixed(0)}%
              </span>
            </div>
          </div>
          <Progress value={state.user_stress * 100} className="h-2" />
        </div>

        <div className="space-y-2.5">
          <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">Case Lifecycle</span>
          <div className="flex flex-wrap gap-2">
            {["pre-legal", "notices-sent", "litigation", "arbitration", "resolved"].map((stage) => (
              <Badge 
                key={stage} 
                variant={state.legal_stage === stage ? "default" : "outline"}
                className={`capitalize text-[9px] py-0.5 px-2.5 transition-all ${state.legal_stage === stage ? "scale-105 shadow-sm ring-1 ring-primary/20" : "text-muted-foreground/40 border-muted"}`}
              >
                {stage.replace("-", " ")}
              </Badge>
            ))}
          </div>
        </div>

        <div className="pt-4 border-t border-border/50 flex items-center gap-4">
          <div className="flex-1 space-y-1">
             <div className="flex justify-between items-center">
                <span className="text-[10px] font-medium text-muted-foreground">Compliance Score</span>
                <span className="text-[10px] font-bold text-green-600">{(state.compliance_score * 100).toFixed(0)}%</span>
             </div>
             <Progress value={state.compliance_score * 100} className="h-1 bg-green-100" />
          </div>
          <div className="flex flex-col items-end">
            <span className="text-[10px] font-medium text-muted-foreground">Steps</span>
            <span className="text-sm font-bold">{state.steps}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default EnvironmentStatePanel;
