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
  const business = result.business_result || null;

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
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <DashboardCard title="Growth Score" value={scores.growth_score} />
        <DashboardCard title="Runway Score" value={scores.runway_score} />
        <DashboardCard title="Volatility Score" value={scores.volatility_score} />
        <DashboardCard title="Business Score" value={scores.business_score} />
      </div>

      {business && (
        <div className="mt-6 rounded-lg border border-emerald-200 bg-emerald-50 p-4">
          <h3 className="mb-2 text-md font-semibold text-emerald-900">
            Business Quality Assessment
          </h3>
          <div className="grid grid-cols-2 gap-4 md:grid-cols-5">
            <DashboardCard title="Sector" value={business.sector} />
            <DashboardCard title="Scalability" value={business.scalability_score} />
            <DashboardCard title="Market" value={business.market_score} />
            <DashboardCard title="Moat" value={business.moat_score} />
            <DashboardCard title="Traction" value={business.traction_score} />
          </div>
        </div>
      )}

      {/* 🔥 MCP SECTION */}
      {mcp && (
        <div className="mt-6 p-4 rounded-lg border border-indigo-200 bg-indigo-50">
          <h3 className="text-md font-semibold text-indigo-900 mb-2">
            Weil MCP Structured Evaluation
          </h3>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <DashboardCard title="MCP Decision" value={mcp.decision} />
            <DashboardCard title="MCP Score" value={mcp.score} />
            <DashboardCard title="MCP Financial" value={mcp.financial_score} />
            <DashboardCard title="MCP Business" value={mcp.business_score} />
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
