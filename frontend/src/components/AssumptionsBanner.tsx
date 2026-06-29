interface AssumptionsBannerProps {
  assumptions: string[];
}

function AssumptionsBanner({ assumptions }: AssumptionsBannerProps) {
  return (
    <section className="panel border-l-8 border-l-amber-400 p-6">
      <div className="flex flex-col gap-3">
        <div>
          <p className="eyebrow">Simulation Assumptions</p>
          <h2 className="mt-3 text-2xl font-semibold text-slate-950">Interpret results through these simplifications.</h2>
        </div>
        <div className="grid gap-3">
          {assumptions.map((assumption) => (
            <div key={assumption} className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm leading-6 text-slate-700">
              {assumption}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default AssumptionsBanner;
