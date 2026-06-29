import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import type { TimeseriesData } from "../../types";
import { buildChartRows } from "./chartUtils";

interface ReservesChartProps {
  primary: TimeseriesData;
  secondary?: TimeseriesData;
}

function ReservesChart({ primary, secondary }: ReservesChartProps) {
  const rows = buildChartRows(primary, secondary);

  return (
    <div className="panel p-5">
      <div className="mb-5">
        <h3 className="text-lg font-semibold text-slate-950">Reserves</h3>
        <p className="mt-1 text-sm text-slate-600">Accessible reserve value after shocks, redemptions, and liquidations.</p>
      </div>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={rows}>
            <XAxis dataKey="step" tick={{ fill: "#64748b", fontSize: 12 }} />
            <YAxis tick={{ fill: "#64748b", fontSize: 12 }} />
            <Tooltip />
            <Area dataKey="reservesA" stroke="#0f766e" fill="#99f6e4" fillOpacity={0.45} />
            {secondary ? <Area dataKey="reservesB" stroke="#7c3aed" fill="#ddd6fe" fillOpacity={0.35} /> : null}
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default ReservesChart;
