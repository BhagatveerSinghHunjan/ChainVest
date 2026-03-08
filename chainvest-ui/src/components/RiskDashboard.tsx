type Props = { result: any };

export default function RiskDashboard({ result }: Props) {
  if (!result) return null;

  const Card = ({ title, value }: any) => (
    <div className="p-4 rounded-lg border border-gray-200 bg-white">
      <p className="text-sm text-gray-600">{title}</p>
      <p className="text-xl font-semibold text-gray-900">{value ?? "N/A"}</p>
    </div>
  );

  return (
    <div>
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Risk Overview</h2>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card title="Decision" value={result.decision} />
        <Card title="Overall Score" value={result.risk_scores?.overall_score} />
        <Card title="Market Risk" value={result.llm_explanation?.market_risk_score} />
        <Card title="Founder Risk" value={result.llm_explanation?.founder_risk_score} />
      </div>
    </div>
  );
}