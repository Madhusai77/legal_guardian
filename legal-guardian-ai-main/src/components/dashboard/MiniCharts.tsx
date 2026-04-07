import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { TrendingDown, TrendingUp, Activity } from "lucide-react";

interface MiniChartsProps {
  history: any[];
}

const MiniCharts = ({ history }: MiniChartsProps) => {
  // Extract stress and compliance trends from history
  const chartData = history.map((h, idx) => ({
    step: h.step || idx + 1,
    stress: (h.ai?.risk_assessment === 'high' ? 0.8 : (h.ai?.risk_assessment === 'medium' ? 0.5 : 0.2)),
    compliance: (h.ai?.legal_citations?.length || 0) * 0.2, // Proxy for compliance depth
  }));

  if (history.length < 2) return (
     <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {[1, 2].map(i => (
          <Card key={i} className="rounded-2xl shadow-md border-dashed border-2 flex items-center justify-center h-48">
            <div className="text-center opacity-20">
               <Activity className="h-6 w-6 mx-auto mb-2" />
               <p className="text-[10px] italic">Trend data pending more steps...</p>
            </div>
          </Card>
        ))}
     </div>
  );

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <Card className="rounded-2xl shadow-md border-primary/10 overflow-hidden">
        <CardHeader className="pb-2 border-b border-border/50 bg-destructive/5">
          <CardTitle className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider">
            <TrendingDown className="h-4 w-4 text-destructive" /> Risk & Stress Trend
          </CardTitle>
        </CardHeader>
        <CardContent className="pt-4">
          <ResponsiveContainer width="100%" height={150}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
              <XAxis dataKey="step" tick={{ fontSize: 10 }} stroke="hsl(var(--muted-foreground))" />
              <YAxis domain={[0, 1]} tick={{ fontSize: 10 }} stroke="hsl(var(--muted-foreground))" />
              <Tooltip 
                contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', fontSize: '10px' }}
              />
              <Line 
                type="monotone" 
                dataKey="stress" 
                stroke="hsl(var(--destructive))" 
                strokeWidth={3} 
                dot={{ r: 4, strokeWidth: 2, fill: 'white' }} 
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card className="rounded-2xl shadow-md border-primary/10 overflow-hidden">
        <CardHeader className="pb-2 border-b border-border/50 bg-primary/5">
          <CardTitle className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider">
            <TrendingUp className="h-4 w-4 text-primary" /> Regulatory Compliance Trend
          </CardTitle>
        </CardHeader>
        <CardContent className="pt-4">
          <ResponsiveContainer width="100%" height={150}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
              <XAxis dataKey="step" tick={{ fontSize: 10 }} stroke="hsl(var(--muted-foreground))" />
              <YAxis domain={[0, 1]} tick={{ fontSize: 10 }} stroke="hsl(var(--muted-foreground))" />
              <Tooltip 
                contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', fontSize: '10px' }}
              />
              <Line 
                type="monotone" 
                dataKey="compliance" 
                stroke="hsl(var(--primary))" 
                strokeWidth={3} 
                dot={{ r: 4, strokeWidth: 2, fill: 'white' }} 
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
};

export default MiniCharts;
