import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, ReferenceLine } from 'recharts';
import type { RiskTrend } from '@/types';

interface TelemetryGraphProps {
  data: RiskTrend[];
}

function formatTime(timestamp: string): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('en-US', { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: false 
  });
}

export function TelemetryGraph({ data }: TelemetryGraphProps) {
  const formattedData = data.map(item => ({
    ...item,
    time: formatTime(item.timestamp),
  }));

  return (
    <div className="h-48">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={formattedData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="riskGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="hsl(199, 89%, 48%)" stopOpacity={0.3} />
              <stop offset="95%" stopColor="hsl(199, 89%, 48%)" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(217, 33%, 17%)" />
          <XAxis 
            dataKey="time" 
            stroke="hsl(215, 20%, 65%)" 
            fontSize={10}
            interval="preserveStartEnd"
          />
          <YAxis 
            domain={[0, 100]} 
            stroke="hsl(215, 20%, 65%)" 
            fontSize={10}
            ticks={[0, 25, 50, 75, 100]}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: 'hsl(222, 47%, 8%)', 
              border: '1px solid hsl(217, 33%, 17%)',
              borderRadius: '8px',
              color: 'hsl(210, 40%, 98%)'
            }}
            labelStyle={{ color: 'hsl(215, 20%, 65%)' }}
          />
          <ReferenceLine y={75} stroke="hsl(0, 72%, 51%)" strokeDasharray="5 5" />
          <ReferenceLine y={50} stroke="hsl(38, 92%, 50%)" strokeDasharray="5 5" />
          <Line 
            type="monotone" 
            dataKey="risk_score" 
            stroke="hsl(199, 89%, 48%)" 
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4, fill: 'hsl(199, 89%, 48%)' }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
