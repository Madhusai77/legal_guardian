import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Brain, FileText, ChevronRight, AlertCircle, Scale } from "lucide-react";

interface AIDecisionPanelProps {
  decision: any;
}

const AIDecisionPanel = ({ decision }: AIDecisionPanelProps) => {
  if (!decision) return (
    <Card className="rounded-2xl shadow-md flex items-center justify-center min-h-[350px] border-dashed border-2">
      <div className="text-center p-6 space-y-3">
        <Brain className="h-10 w-10 text-muted-foreground/20 mx-auto animate-pulse" />
        <p className="text-sm text-muted-foreground italic">AI Decision pending analysis...</p>
      </div>
    </Card>
  );

  const riskColors = {
    low: "text-green-600 bg-green-50",
    medium: "text-orange-600 bg-orange-50",
    high: "text-red-600 bg-red-50"
  };

  return (
    <Card className="rounded-2xl shadow-md border-primary/10 overflow-hidden h-full">
      <CardHeader className="pb-3 border-b border-border/50 bg-primary/5">
        <div className="flex justify-between items-center w-full">
          <CardTitle className="text-lg font-semibold flex items-center gap-2">
            <Brain className="h-5 w-5 text-primary" />
            AI Decision
          </CardTitle>
          <Badge variant="secondary" className={`${riskColors[decision.risk_assessment || 'medium']} capitalize border-none`}>
            {decision.risk_assessment} Risk
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-4 pt-4 h-[calc(100%-60px)]">
        <div className="space-y-1.5">
          <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest flex items-center gap-1.5">
             <Scale className="h-3 w-3" /> Selected Legal Action
          </span>
          <Badge className="bg-primary text-white text-xs px-3 py-1 capitalize">
            {decision.action.replace("_", " ")}
          </Badge>
        </div>

        <div className="space-y-2">
          <span className="text-xs font-bold text-muted-foreground">Legal Reasoning (Plain English)</span>
          <ScrollArea className="h-24 rounded-lg bg-muted/20 border border-border/50 p-3">
            <p className="text-xs leading-relaxed text-muted-foreground">
              {decision.reasoning}
            </p>
          </ScrollArea>
        </div>

        <div className="space-y-2">
          <span className="text-xs font-bold text-muted-foreground">Generated Reply</span>
          <ScrollArea className="h-32 rounded-lg bg-blue-50/50 border border-blue-200/50 p-3 italic">
            <p className="text-xs text-blue-900 leading-relaxed font-serif">
              "{decision.reply}"
            </p>
          </ScrollArea>
          <Button variant="ghost" size="sm" className="w-full text-[10px] h-6 text-primary hover:text-primary/80">
             Copy suggested reply
          </Button>
        </div>

        <div className="border-t border-border/50 pt-3">
          <div className="flex flex-wrap gap-2">
            {decision.legal_citations?.map((cite, idx) => (
              <Badge key={idx} variant="secondary" className="bg-muted text-muted-foreground text-[9px] py-0 px-2 flex items-center gap-1">
                <FileText className="h-2.5 w-2.5" />
                {cite}
              </Badge>
            ))}
          </div>
        </div>

        <div className="bg-primary/5 p-3 rounded-lg border border-primary/10 flex items-start gap-2">
           <ChevronRight className="h-3 w-3 text-primary mt-0.5 shrink-0" />
           <div className="space-y-0.5">
              <span className="text-[10px] font-bold text-primary uppercase">Next Suggested Step</span>
              <p className="text-[10px] text-muted-foreground leading-tight">{decision.suggested_next_step}</p>
           </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default AIDecisionPanel;
