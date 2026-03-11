type Props = { result: any };

export default function RiskDashboard({ result }: Props) {
  if (!result) return null;

  const scores = result.risk_scores || {};
  const mcp = result.mcp_result || null;
  const audit = mcp?.audit || null;
  const auditDetails = audit?.details || null;

  const boolLabel = (value: unknown) => {
    if (value === true) return "YES";
    if (value === false) return "NO";
    return "N/A";
  };

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
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
        <Card title="Growth Score" value={scores.growth_score} />
        <Card title="Runway Score" value={scores.runway_score} />
        <Card title="Volatility Score" value={scores.volatility_score} />
      </div>

      {/* 🔥 MCP SECTION */}
      {mcp && (
        <div className="mt-6 p-4 rounded-lg border border-indigo-200 bg-indigo-50">
          <h3 className="text-md font-semibold text-indigo-900 mb-2">
            Weil MCP Structured Evaluation
          </h3>

          <div className="grid grid-cols-2 gap-4">
            <Card title="MCP Decision" value={mcp.decision} />
            <Card title="MCP Score" value={mcp.score} />
          </div>

          <div className="grid grid-cols-2 md:grid-cols-2 gap-4 mt-4">
            <Card title="On-Chain Audit" value={boolLabel(audit?.on_chain)} />
            <Card
              title="Tx Status"
              value={auditDetails?.status || "N/A"}
            />
          </div>
        </div>
      )}
    </div>
  );
}
