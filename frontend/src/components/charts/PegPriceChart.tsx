import { Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import type { TimeseriesData } from "../../types";
import { buildChartRows } from "./chartUtils";

interface PegPriceChartProps {
  primary: TimeseriesData;
  secondary?: TimeseriesData;
}

function PegPriceChart({ primary, secondary }: PegPriceChartProps) {
  const rows = buildChartRows(primary, secondary);

  return (
    <div className="panel p-5">
      <div className="mb-5">
        <h3 className="text-lg font-semibold text-slate-950">Peg Price</h3>
        <p className="mt-1 text-sm text-slate-600">Step-by-step peg behavior against the target line.</p>
      </div>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={rows}>
            <XAxis dataKey="step" tick={{ fill: "#64748b", fontSize: 12 }} />
            <YAxis domain={[0.4, 1.1]} tick={{ fill: "#64748b", fontSize: 12 }} />
            <Tooltip />
            <ReferenceLine y={1} stroke="#f59e0b" strokeDasharray="4 4" />
            <Line dataKey="pegPriceA" stroke="#0f172a" dot={false} strokeWidth={2.5} />
            {secondary ? <Line dataKey="pegPriceB" stroke="#0d9488" dot={false} strokeWidth={2.5} /> : null}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default PegPriceChart;
