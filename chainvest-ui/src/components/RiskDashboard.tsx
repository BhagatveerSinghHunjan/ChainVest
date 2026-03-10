type Props = { result: any };

export default function RiskDashboard({ result }: Props) {
  if (!result) return null;

  const scores = result.risk_scores || {};

  const Card = ({ title, value }: any) => (
    <div className="p-4 rounded-lg border border-gray-200 bg-white">
      <p className="text-sm text-gray-600">{title}</p>
      <p className="text-xl font-semibold text-gray-900">
        {value !== undefined && value !== null ? value : "N/A"}
      </p>
    </div>
  );

  return (
    <div>
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        Risk Overview
      </h2>

      {/* TOP ROW */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <Card title="Decision" value={result.decision} />
        <Card title="Overall Score" value={scores.overall_score} />
        <Card title="Financial Score" value={scores.financial_score} />
        <Card title="Unit Score" value={scores.unit_score} />
      </div>

      {/* SECOND ROW */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        <Card title="Growth Score" value={scores.growth_score} />
        <Card title="Runway Score" value={scores.runway_score} />
        <Card title="Volatility Score" value={scores.volatility_score} />
      </div>
    </div>
  );
}