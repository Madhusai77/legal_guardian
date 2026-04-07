import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { User, MessageSquare } from "lucide-react";

interface LenderResponsePanelProps {
  response: string | null;
}

const LenderResponsePanel = ({ response }: LenderResponsePanelProps) => {
  return (
    <Card className="rounded-2xl shadow-md border-primary/10 overflow-hidden">
      <CardHeader className="pb-3 border-b border-border/50 bg-destructive/5">
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          <User className="h-5 w-5 text-destructive" />
          Lender / Collection Agent Response
        </CardTitle>
      </CardHeader>
      <CardContent className="pt-4 pb-6 min-h-[140px] flex items-center justify-center">
        {response ? (
          <div className="flex gap-4 p-4 rounded-2xl bg-muted/20 border border-border/40 relative max-w-full">
            <MessageSquare className="h-5 w-5 text-destructive mt-1 shrink-0" />
            <div className="space-y-2">
              <span className="text-[10px] font-bold text-destructive uppercase tracking-widest leading-none">Last Message Received</span>
              <p className="text-sm italic leading-relaxed text-foreground/80">
                "{response}"
              </p>
            </div>
            <Badge variant="outline" className="absolute -top-3 right-4 bg-background text-[9px] px-2 py-0">Verified Adaptive Response</Badge>
          </div>
        ) : (
          <div className="text-center space-y-2">
            <User className="h-8 w-8 text-muted-foreground/20 mx-auto" />
            <p className="text-xs text-muted-foreground italic">Awaiting lender reaction to AI strategy...</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default LenderResponsePanel;
