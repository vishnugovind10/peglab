import { Bar, BarChart, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import type { TimeseriesData } from "../../types";
import { buildChartRows } from "./chartUtils";

interface SupplyFlowChartProps {
  primary: TimeseriesData;
  secondary?: TimeseriesData;
}

function SupplyFlowChart({ primary, secondary }: SupplyFlowChartProps) {
  const rows = buildChartRows(primary, secondary);

  return (
    <div className="panel p-5">
      <div className="mb-5">
        <h3 className="text-lg font-semibold text-slate-950">Supply Flow</h3>
        <p className="mt-1 text-sm text-slate-600">
          {secondary
            ? "Supply paths overlaid for both designs under the same scenario."
            : "Mint, redeem, and liquidation volumes for the active design."}
        </p>
      </div>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          {secondary ? (
            <LineChart data={rows}>
              <XAxis dataKey="step" tick={{ fill: "#64748b", fontSize: 12 }} />
              <YAxis tick={{ fill: "#64748b", fontSize: 12 }} />
              <Tooltip />
              <Line dataKey="supplyA" stroke="#0f172a" dot={false} strokeWidth={2.5} />
              <Line dataKey="supplyB" stroke="#dc2626" dot={false} strokeWidth={2.5} />
            </LineChart>
          ) : (
            <BarChart data={rows}>
              <XAxis dataKey="step" tick={{ fill: "#64748b", fontSize: 12 }} />
              <YAxis tick={{ fill: "#64748b", fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="mintVolume" stackId="flow" fill="#14b8a6" radius={[4, 4, 0, 0]} />
              <Bar dataKey="redeemVolume" stackId="flow" fill="#fb7185" radius={[4, 4, 0, 0]} />
              <Bar dataKey="liquidationVolume" stackId="flow" fill="#f59e0b" radius={[4, 4, 0, 0]} />
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default SupplyFlowChart;
