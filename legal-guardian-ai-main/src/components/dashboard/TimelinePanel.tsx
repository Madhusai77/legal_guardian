import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { History, CheckCircle2, AlertCircle, Clock } from "lucide-react";

interface TimelinePanelProps {
  history: any[];
}

const TimelinePanel = ({ history }: TimelinePanelProps) => {
  return (
    <Card className="rounded-2xl shadow-md border-primary/10 overflow-hidden">
      <CardHeader className="pb-3 border-b border-border/50 bg-muted/50">
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          <History className="h-5 w-5 text-primary" />
          Interactive Legal Timeline
        </CardTitle>
      </CardHeader>
      <CardContent className="pt-4 pb-6 overflow-x-auto">
        <div className="flex gap-4 min-w-[600px] py-4 relative">
          <div className="absolute top-1/2 left-0 w-full h-0.5 bg-border -translate-y-1/2 z-0" />
          
          {history.length > 0 ? (
            history.map((step, idx) => (
              <div key={idx} className="relative z-10 w-48 shrink-0 bg-background rounded-xl border border-border shadow-sm p-3 space-y-2 hover:border-primary/30 transition-all cursor-default">
                <div className="flex justify-between items-center">
                  <Badge variant="outline" className="text-[10px] font-bold">Step {step.step}</Badge>
                   {idx === history.length - 1 ? (
                     <div className="h-2 w-2 rounded-full bg-primary animate-ping" />
                   ) : (
                     <CheckCircle2 className="h-4 w-4 text-green-500" />
                   )}
                </div>
                <div className="space-y-1">
                   <div className="flex items-center gap-1.5 text-[10px] font-bold text-primary uppercase">
                      AI: {step.ai?.action || "analysis"}
                   </div>
                   <p className="text-[9px] text-muted-foreground line-clamp-2 italic leading-relaxed">
                     "{step.ai?.reasoning || "Initial state analysis complete."}"
                   </p>
                </div>
                <div className="pt-2 border-t border-border/40">
                   <div className="flex items-center gap-1.5 text-[9px] font-bold text-destructive uppercase">
                      Lender Response
                   </div>
                   <p className="text-[9px] text-muted-foreground line-clamp-1 italic">
                     {step.lender || "Awaiting response..."}
                   </p>
                </div>
              </div>
            ))
          ) : (
            <div className="w-full flex items-center justify-center p-8 space-x-3">
              <Clock className="h-5 w-5 text-muted-foreground/30" />
              <p className="text-sm text-muted-foreground italic">Interactive timeline will populate during analysis steps</p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default TimelinePanel;
