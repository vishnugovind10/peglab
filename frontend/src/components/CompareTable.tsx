import type { CompareResponse } from "../types";

interface CompareTableProps {
  result: CompareResponse;
  designALabel: string;
  designBLabel: string;
}

function formatRecovery(value: number | null) {
  return value === null ? "No recovery" : `${value} steps`;
}

function CompareTable({ result, designALabel, designBLabel }: CompareTableProps) {
  const rows = [
    ["Peg stability", `${result.design_a_result.peg_stability_pct}%`, `${result.design_b_result.peg_stability_pct}%`],
    [
      "Recovery time",
      formatRecovery(result.design_a_result.recovery_time_steps),
      formatRecovery(result.design_b_result.recovery_time_steps),
    ],
    [
      "Worst drawdown",
      `${result.design_a_result.worst_drawdown_pct}%`,
      `${result.design_b_result.worst_drawdown_pct}%`,
    ],
    [
      "Final collateral ratio",
      result.design_a_result.final_collateral_ratio.toFixed(2),
      result.design_b_result.final_collateral_ratio.toFixed(2),
    ],
    ["Failure probability", result.design_a_result.failure_probability, result.design_b_result.failure_probability],
  ];

  return (
    <section className="panel overflow-hidden p-2">
      <table className="min-w-full border-separate border-spacing-0">
        <thead>
          <tr className="text-left text-sm uppercase tracking-[0.16em] text-slate-500">
            <th className="px-4 py-4">Metric</th>
            <th className="px-4 py-4">{designALabel}</th>
            <th className="px-4 py-4">{designBLabel}</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(([metric, aValue, bValue]) => (
            <tr key={metric} className="text-sm text-slate-700">
              <td className="border-t border-slate-200 px-4 py-4 font-medium text-slate-950">{metric}</td>
              <td className="border-t border-slate-200 px-4 py-4">{aValue}</td>
              <td className="border-t border-slate-200 px-4 py-4">{bValue}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

export default CompareTable;
