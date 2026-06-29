import { Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import type { TimeseriesData } from "../../types";
import { buildChartRows } from "./chartUtils";

interface CollateralRatioChartProps {
  primary: TimeseriesData;
  secondary?: TimeseriesData;
}

function CollateralRatioChart({ primary, secondary }: CollateralRatioChartProps) {
  const rows = buildChartRows(primary, secondary);

  return (
    <div className="panel p-5">
      <div className="mb-5">
        <h3 className="text-lg font-semibold text-slate-950">Collateral Ratio</h3>
        <p className="mt-1 text-sm text-slate-600">Coverage buffer over time, with parity shown as a reference line.</p>
      </div>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={rows}>
            <XAxis dataKey="step" tick={{ fill: "#64748b", fontSize: 12 }} />
            <YAxis tick={{ fill: "#64748b", fontSize: 12 }} />
            <Tooltip />
            <ReferenceLine y={1} stroke="#fb7185" strokeDasharray="4 4" />
            <Line dataKey="collateralRatioA" stroke="#1d4ed8" dot={false} strokeWidth={2.5} />
            {secondary ? <Line dataKey="collateralRatioB" stroke="#f97316" dot={false} strokeWidth={2.5} /> : null}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default CollateralRatioChart;
