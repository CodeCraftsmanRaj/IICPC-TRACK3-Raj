import { motion } from 'framer-motion';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { PieChartIcon, BarChart3 } from 'lucide-react';
import type { ThreatDistribution } from '@/types';

interface RiskChartsProps {
  distribution: ThreatDistribution[];
  topThreats: { name: string; count: number }[];
}

const COLORS = ['hsl(0, 72%, 51%)', 'hsl(38, 92%, 50%)', 'hsl(48, 96%, 53%)', 'hsl(199, 89%, 48%)'];

export function RiskCharts({ distribution, topThreats }: RiskChartsProps) {
  const total = distribution.reduce((acc, item) => acc + item.value, 0);

  return (
    <div className="space-y-6">
      {/* Donut Chart */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.5 }}
        className="rounded-xl border border-border bg-card p-4"
      >
        <div className="mb-4 flex items-center gap-2">
          <PieChartIcon className="h-5 w-5 text-primary" />
          <h3 className="font-semibold text-foreground">Risk Distribution</h3>
        </div>
        
        <div className="h-48">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={distribution}
                cx="50%"
                cy="50%"
                innerRadius={50}
                outerRadius={70}
                paddingAngle={2}
                dataKey="value"
              >
                {distribution.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-4 grid grid-cols-2 gap-2">
          {distribution.map((item, index) => (
            <div key={item.name} className="flex items-center gap-2">
              <div 
                className="h-3 w-3 rounded-full" 
                style={{ backgroundColor: COLORS[index % COLORS.length] }}
              />
              <span className="text-xs text-muted-foreground">{item.name}</span>
              <span className="ml-auto font-mono text-xs font-medium text-foreground">
                {Math.round((item.value / total) * 100)}%
              </span>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Bar Chart */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.6 }}
        className="rounded-xl border border-border bg-card p-4"
      >
        <div className="mb-4 flex items-center gap-2">
          <BarChart3 className="h-5 w-5 text-primary" />
          <h3 className="font-semibold text-foreground">Top Threats</h3>
        </div>
        
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={topThreats} layout="vertical" margin={{ left: 10, right: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(217, 33%, 17%)" />
              <XAxis type="number" stroke="hsl(215, 20%, 65%)" fontSize={12} />
              <YAxis 
                type="category" 
                dataKey="name" 
                stroke="hsl(215, 20%, 65%)" 
                fontSize={11}
                width={70}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'hsl(222, 47%, 8%)', 
                  border: '1px solid hsl(217, 33%, 17%)',
                  borderRadius: '8px',
                  color: 'hsl(210, 40%, 98%)'
                }}
              />
              <Bar 
                dataKey="count" 
                fill="hsl(199, 89%, 48%)" 
                radius={[0, 4, 4, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>
    </div>
  );
}
