export type ChainVestResult = {
  decision?: string;
  final_score?: number;
  decision_reasoning?: {
    summary?: string;
    threshold_context?: string;
    score_breakdown?: {
      overall_score?: number;
      financial_score?: number | string | null;
      unit_score?: number | string | null;
      business_score?: number | string | null;
    };
    highlights?: string[];
    concerns?: string[];
  };
  risk_scores?: Record<string, number | string | null | undefined>;
  business_result?: {
    sector?: string;
    sector_score?: number;
    scalability_score?: number;
    market_score?: number;
    moat_score?: number;
    traction_score?: number;
    business_score?: number;
    flags?: string[];
  };
  mcp_result?: {
    decision?: string;
    score?: number;
    financial_score?: number;
    business_score?: number;
    scalability_score?: number;
    market_score?: number;
    moat_score?: number;
    sector_score?: number;
    sector?: string;
    audit?: {
      on_chain?: boolean;
      details?: {
        status?: string;
      };
    };
    deployment?: {
      source?: string;
      contract_address?: string | null;
      status?: string;
    };
  };
  tx_hashes?: string[];
  logs?: string[];
};
