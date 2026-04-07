import { Upload, Loader2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useState } from "react";

interface UserInputPanelProps {
  onSubmit: (formData: FormData) => void;
  loading: boolean;
}

const UserInputPanel = ({ onSubmit, loading }: UserInputPanelProps) => {
  const [stress, setStress] = useState([0.5]);
  const [complaint, setComplaint] = useState("");
  const [loanAmount, setLoanAmount] = useState("");
  const [delayDays, setDelayDays] = useState("");
  const [lenderType, setLenderType] = useState("loan-app");
  const [file, setFile] = useState<File | null>(null);

  const handleSubmit = () => {
    const formData = new FormData();
    formData.append("complaint", complaint);
    formData.append("loan_amount", loanAmount);
    formData.append("delay_days", delayDays);
    formData.append("lender_type", lenderType);
    formData.append("stress_level", stress[0].toString());
    if (file) formData.append("evidence", file);
    
    onSubmit(formData);
  };

  return (
    <Card className="rounded-2xl shadow-md border-primary/10">
      <CardHeader className="pb-3 border-b border-border/50">
        <CardTitle className="text-lg font-semibold bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">
          User Input
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4 pt-4">
        <div className="space-y-1.5">
          <Label className="text-xs font-medium">User Complaint</Label>
          <Textarea 
            value={complaint}
            onChange={(e) => setComplaint(e.target.value)}
            placeholder="Describe the harassment incident..." 
            className="min-h-[100px] resize-none focus:ring-primary/20" 
          />
        </div>
        <div className="space-y-1.5">
          <Label className="text-xs font-medium">Upload Evidence (SMS / Call Text)</Label>
          <div className="flex items-center gap-2">
            <Input 
              type="file" 
              className="hidden" 
              id="evidence-upload"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
            <Label 
              htmlFor="evidence-upload"
              className="flex items-center w-full justify-start text-sm border border-input h-9 px-3 rounded-md hover:bg-accent cursor-pointer transition-colors"
            >
              <Upload className="mr-2 h-4 w-4 text-primary" /> 
              {file ? file.name : "Choose file..."}
            </Label>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div className="space-y-1.5">
            <Label className="text-xs font-medium">Loan Amount (₹)</Label>
            <Input 
              type="number" 
              value={loanAmount}
              onChange={(e) => setLoanAmount(e.target.value)}
              placeholder="50000" 
              className="focus:ring-primary/20"
            />
          </div>
          <div className="space-y-1.5">
            <Label className="text-xs font-medium">Delay Days</Label>
            <Input 
              type="number" 
              value={delayDays}
              onChange={(e) => setDelayDays(e.target.value)}
              placeholder="15" 
              className="focus:ring-primary/20"
            />
          </div>
        </div>
        <div className="space-y-1.5">
          <Label className="text-xs font-medium">Lender Type</Label>
          <Select value={lenderType} onValueChange={setLenderType}>
            <SelectTrigger className="focus:ring-primary/20">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="loan-app">Loan App</SelectItem>
              <SelectItem value="bank">Bank</SelectItem>
              <SelectItem value="nbfc">NBFC</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-2 pb-2">
          <div className="flex justify-between items-center">
            <Label className="text-xs font-medium">Recorded User Stress</Label>
            <span className="text-xs font-bold text-primary">{(stress[0] * 100).toFixed(0)}%</span>
          </div>
          <Slider value={stress} onValueChange={setStress} min={0} max={1} step={0.01} className="py-1" />
        </div>
        <Button 
          className="w-full font-semibold shadow-lg shadow-primary/20 transition-all active:scale-[0.98]" 
          onClick={handleSubmit}
          disabled={loading || !complaint}
        >
          {loading ? (
            <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Analyzing...</>
          ) : (
            "Analyze with AI Lawyer"
          )}
        </Button>
      </CardContent>
    </Card>
  );
};

export default UserInputPanel;
