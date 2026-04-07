import { useState, useEffect } from "react";
import DashboardHeader from "@/components/dashboard/DashboardHeader";
import UserInputPanel from "@/components/dashboard/UserInputPanel";
import EnvironmentStatePanel from "@/components/dashboard/EnvironmentStatePanel";
import AIDecisionPanel from "@/components/dashboard/AIDecisionPanel";
import LenderResponsePanel from "@/components/dashboard/LenderResponsePanel";
import RewardPanel from "@/components/dashboard/RewardPanel";
import TimelinePanel from "@/components/dashboard/TimelinePanel";
import MiniCharts from "@/components/dashboard/MiniCharts";
import { useToast } from "@/hooks/use-toast";

const API_BASE = "http://localhost:7860";

const Index = () => {
  const [scenario, setScenario] = useState("easy");
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const [data, setData] = useState({
    state: null,
    ai_decision: null,
    lender_response: null,
    history: []
  });

  const handleAnalyze = async (formData: FormData) => {
    setLoading(true);
    formData.append("scenario", scenario);
    
    try {
      const resp = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        body: formData,
      });
      const result = await resp.json();
      
      if (result.error) throw new Error(result.error);
      
      setData(prev => ({
        ...result,
        history: [...prev.history, { step: result.state.steps, ai: result.ai_decision, lender: result.lender_response }]
      }));
      
      toast({ title: "Analysis Complete", description: "AI has evaluated the evidence based on RBI guidelines." });
    } catch (err) {
      toast({ variant: "destructive", title: "Analysis Failed", description: err.message });
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    try {
      await fetch(`${API_BASE}/reset`, { 
        method: "POST", 
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scenario }) 
      });
      setData({ state: null, ai_decision: null, lender_response: null, history: [] });
      toast({ title: "Environment Reset", description: `Scenario set to ${scenario}` });
    } catch (err) {
      toast({ variant: "destructive", title: "Reset Failed", description: err.message });
    }
  };

  const handleNextStep = async () => {
    if (!data.state) {
      toast({ variant: "destructive", title: "Error", description: "Please submit initial analysis first." });
      return;
    }
    
    setLoading(true);
    try {
      const resp = await fetch(`${API_BASE}/step`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          action_type: "negotiation", 
          content: "Proceeding to next legal step."
        }),
      });
      const result = await resp.json();
      
      if (result.error) throw new Error(result.error);
      
      setData(prev => ({
        ...prev,
        state: result.state,
        ai_decision: result.ai_decision,
        lender_response: result.lender_response,
        history: [...prev.history, { step: result.state.steps, ai: result.ai_decision, lender: result.lender_response }]
      }));
      
      toast({ title: "Next Step Complete", description: "Successfully simulated the next interaction." });
    } catch (err) {
      toast({ variant: "destructive", title: "Step Failed", description: err.message });
    } finally {
      setLoading(false);
    }
  };

  const handleRunFull = async () => {
    if (!data.state) {
      toast({ variant: "destructive", title: "Error", description: "Please submit initial analysis first." });
      return;
    }
    
    setLoading(true);
    toast({ title: "Simulation Running", description: "AI is attempting to resolve the case automatically." });
    
    try {
      // Simple loop to simulate a full run
      for (let i = 0; i < 3; i++) {
        const resp = await fetch(`${API_BASE}/step`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
            action_type: "negotiation", 
            content: "Auto-negotiation processing."
          }),
        });
        const result = await resp.json();
        if (result.error) throw new Error(result.error);
        
        setData(prev => ({
          ...prev,
          state: result.state,
          ai_decision: result.ai_decision,
          lender_response: result.lender_response,
          history: [...prev.history, { step: result.state.steps, ai: result.ai_decision, lender: result.lender_response }]
        }));
        
        if (result.state.resolution_status === "resolved") break;
        // Small delay for visual effect
        await new Promise(r => setTimeout(r, 800));
      }
      
      toast({ title: "Simulation Complete", description: "The full automated run has finished." });
    } catch (err) {
      toast({ variant: "destructive", title: "Run Failed", description: err.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background p-4 md:p-6 space-y-4">
      <DashboardHeader
        scenario={scenario}
        onScenarioChange={setScenario}
        onReset={handleReset}
        onNextStep={handleNextStep}
        onRunFull={handleRunFull}
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <UserInputPanel onSubmit={handleAnalyze} loading={loading} />
        <EnvironmentStatePanel state={data.state} />
        <AIDecisionPanel decision={data.ai_decision} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <LenderResponsePanel response={data.lender_response} />
        <RewardPanel state={data.state} />
      </div>

      <div className="space-y-4">
        <TimelinePanel history={data.history} />
        <MiniCharts history={data.history} />
      </div>
    </div>
  );
};

export default Index;
