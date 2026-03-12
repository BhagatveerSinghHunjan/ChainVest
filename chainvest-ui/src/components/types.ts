export type ChainVestResult = {
  decision?: string;
  final_score?: number;
  risk_scores?: Record<string, number | string | null | undefined>;
  llm_trace?: {
    provider?: string | null;
    reason?: string | null;
    error?: string | null;
  } | null;
  mcp_result?: {
    decision?: string;
    score?: number;
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
