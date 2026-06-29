interface MetricsCardProps {
  label: string;
  value: string;
  tone?: "neutral" | "good" | "warning";
}

const toneClasses = {
  neutral: "bg-slate-950 text-white",
  good: "bg-teal-600 text-white",
  warning: "bg-amber-400 text-slate-950",
};

function MetricsCard({ label, value, tone = "neutral" }: MetricsCardProps) {
  return (
    <div className={`rounded-[1.5rem] p-5 shadow-[0_18px_40px_rgba(15,23,42,0.08)] ${toneClasses[tone]}`}>
      <p className="text-sm uppercase tracking-[0.18em] opacity-75">{label}</p>
      <p className="mt-3 text-3xl font-semibold">{value}</p>
    </div>
  );
}

export default MetricsCard;
