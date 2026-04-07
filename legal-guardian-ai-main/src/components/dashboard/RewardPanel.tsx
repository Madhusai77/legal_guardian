import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Trophy, Star, Target } from "lucide-react";
import { Progress } from "@/components/ui/progress";

interface RewardPanelProps {
  state: any;
}

const RewardPanel = ({ state }: RewardPanelProps) => {
  if (!state) return (
    <Card className="rounded-2xl shadow-md border-primary/10 overflow-hidden flex items-center justify-center p-6 h-full min-h-[140px]">
      <div className="text-center space-y-1">
        <Star className="h-6 w-6 text-muted-foreground/20 mx-auto" />
        <p className="text-[10px] text-muted-foreground italic">Reward metrics will calculate after analysis</p>
      </div>
    </Card>
  );

  const calculateTotalReward = () => {
    // Simulated cumulative reward for current dashboard view
    return (state.compliance_score * 0.4) + (state.resolution_status === "resolved" ? 0.6 : 0.1);
  };

  const totalReward = calculateTotalReward();

  return (
    <Card className="rounded-2xl shadow-md border-primary/10 overflow-hidden h-full">
      <CardHeader className="pb-3 border-b border-border/50 bg-green-50/10">
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          <Trophy className="h-5 w-5 text-yellow-500 fill-yellow-500/10" />
          System Reward & Scoring
        </CardTitle>
      </CardHeader>
      <CardContent className="pt-4 flex flex-col justify-center h-[calc(100%-60px)]">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1.5 border-r border-border/50">
             <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest flex items-center gap-1">
                <Star className="h-3 w-3 text-yellow-500" /> Current Step Reward
             </span>
             <div className="text-2xl font-black text-foreground">
               {totalReward.toFixed(2)}
               <span className="text-sm font-medium text-muted-foreground ml-1">/ 1.00</span>
             </div>
          </div>
          <div className="space-y-1.5 pl-2">
             <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest flex items-center gap-1">
                <Target className="h-3 w-3 text-primary" /> Target
             </span>
             <Badge variant="outline" className="text-[10px] bg-green-50 text-green-700 border-green-200">
                Optimal Resolution
             </Badge>
          </div>
        </div>
        <div className="mt-4 space-y-2">
          <div className="flex justify-between text-[10px] font-medium text-muted-foreground px-0.5">
             <span>Progression to Goal</span>
             <span>{(totalReward * 100).toFixed(0)}%</span>
          </div>
          <Progress value={totalReward * 100} className="h-1.5" />
        </div>
      </CardContent>
    </Card>
  );
};

export default RewardPanel;
