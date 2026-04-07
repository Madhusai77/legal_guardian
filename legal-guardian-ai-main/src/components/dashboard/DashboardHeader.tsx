import { RotateCcw, Play, FastForward } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import RegulatoryDialog from "./RegulatoryDialog";

interface DashboardHeaderProps {
  scenario: string;
  onScenarioChange: (s: string) => void;
  onReset: () => void;
  onNextStep: () => void;
  onRunFull: () => void;
}

const scenarios = ["easy", "medium", "hard"];

const DashboardHeader = ({ scenario, onScenarioChange, onReset, onNextStep, onRunFull }: DashboardHeaderProps) => (
  <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-border/40 pb-4">
    <div className="space-y-0.5">
      <h1 className="text-xl sm:text-2xl font-black text-foreground tracking-tight bg-gradient-to-br from-foreground to-foreground/70 bg-clip-text">
        Debt Harassment Legal AI Environment
      </h1>
      <p className="text-xs sm:text-sm text-muted-foreground font-medium flex items-center gap-1.5">
        <span className="h-1.5 w-1.5 rounded-full bg-green-500 animate-pulse" />
        AI-powered legal decision simulation dashboard
      </p>
    </div>
    <div className="flex flex-wrap items-center gap-3">
      <div className="flex items-center bg-muted/30 p-1 rounded-xl border border-border/50">
        {scenarios.map((s) => (
          <Badge
            key={s}
            variant={scenario === s ? "default" : "outline"}
            className={`cursor-pointer px-3 py-1.5 capitalize text-[10px] sm:text-[11px] font-bold transition-all ${scenario === s ? "shadow-md scale-105" : "text-muted-foreground hover:bg-muted/50"}`}
            onClick={() => onScenarioChange(s)}
          >
            {s}
          </Badge>
        ))}
      </div>
      <div className="flex items-center gap-2">
        <RegulatoryDialog />
        <div className="h-6 w-px bg-border/60 mx-1 hidden sm:block" />
        <Button variant="outline" size="sm" onClick={onReset} className="text-xs font-bold h-9">
          <RotateCcw className="mr-1.5 h-3.5 w-3.5" /> Reset
        </Button>
        <Button size="sm" onClick={onNextStep} className="text-xs font-bold h-9 shadow-lg shadow-primary/20">
          <Play className="mr-1.5 h-3.5 w-3.5" /> Next Step
        </Button>
        <Button size="sm" variant="secondary" onClick={onRunFull} className="text-xs font-bold h-9">
          <FastForward className="mr-1.5 h-3.5 w-3.5" /> Run Full
        </Button>
      </div>
    </div>
  </div>
);

export default DashboardHeader;
