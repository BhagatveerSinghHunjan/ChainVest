import type { ReactNode } from "react";

import type { ChainVestResult } from "@/components/types";

type Props = { result: ChainVestResult };

function DashboardCard({
  title,
  value,
}: {
  title: string;
  value: ReactNode;
}) {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4">
      <p className="text-sm text-gray-600">{title}</p>
      <p className="text-xl font-semibold text-gray-900">
        {value !== undefined && value !== null && value !== "" ? value : "N/A"}
      </p>
    </div>
  );
}

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

  return (
    <div>
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        Risk Overview
      </h2>

      {/* TOP ROW */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <DashboardCard title="Decision" value={result.decision} />
        <DashboardCard title="Overall Score" value={scores.overall_score} />
        <DashboardCard title="Financial Score" value={scores.financial_score} />
        <DashboardCard title="Unit Score" value={scores.unit_score} />
      </div>

      {/* SECOND ROW */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
        <DashboardCard title="Growth Score" value={scores.growth_score} />
        <DashboardCard title="Runway Score" value={scores.runway_score} />
        <DashboardCard title="Volatility Score" value={scores.volatility_score} />
      </div>

      {/* 🔥 MCP SECTION */}
      {mcp && (
        <div className="mt-6 p-4 rounded-lg border border-indigo-200 bg-indigo-50">
          <h3 className="text-md font-semibold text-indigo-900 mb-2">
            Weil MCP Structured Evaluation
          </h3>

          <div className="grid grid-cols-2 gap-4">
            <DashboardCard title="MCP Decision" value={mcp.decision} />
            <DashboardCard title="MCP Score" value={mcp.score} />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
            <DashboardCard title="On-Chain Audit" value={boolLabel(audit?.on_chain)} />
            <DashboardCard title="Audit Status" value={auditDetails?.status || "N/A"} />
          </div>
        </div>
      )}
    </div>
  );
}
