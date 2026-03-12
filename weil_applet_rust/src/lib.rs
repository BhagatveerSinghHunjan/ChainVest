use serde::{Deserialize, Serialize};
use weil_macros::{constructor, query, smart_contract, WeilType};

trait ChainVestMCP {
    fn new() -> Result<Self, String>
    where
        Self: Sized;

    async fn evaluate_startup(&self, revenue: f64, burn: f64, cash: f64) -> StartupEvaluation;
    fn tools(&self) -> String;
    fn prompts(&self) -> String;
}

#[derive(Serialize, Deserialize, WeilType)]
pub struct StartupEvaluation {
    pub decision: String,
    pub score: f64,
}

#[derive(Serialize, Deserialize, WeilType, Default)]
pub struct ChainVestMCPContractState {}

fn clamp_non_negative(value: f64) -> f64 {
    if value.is_finite() && value > 0.0 {
        value
    } else {
        0.0
    }
}

fn score_startup(revenue: f64, burn: f64, cash: f64) -> StartupEvaluation {
    let revenue = clamp_non_negative(revenue);
    let burn = clamp_non_negative(burn);
    let cash = clamp_non_negative(cash);

    let score = (revenue / (burn + 1.0)) * (cash / 10_000.0);
    let decision = if score > 5.0 {
        "APPROVE"
    } else if score > 2.0 {
        "REVIEW"
    } else {
        "REJECT"
    };

    StartupEvaluation {
        decision: decision.to_string(),
        score: (score * 100.0).round() / 100.0,
    }
}

#[smart_contract]
impl ChainVestMCP for ChainVestMCPContractState {
    #[constructor]
    fn new() -> Result<Self, String>
    where
        Self: Sized,
    {
        Ok(Self::default())
    }

    #[query]
    async fn evaluate_startup(&self, revenue: f64, burn: f64, cash: f64) -> StartupEvaluation {
        score_startup(revenue, burn, cash)
    }

    #[query]
    fn tools(&self) -> String {
        r#"[
  {
    "type": "function",
    "function": {
      "name": "evaluate_startup",
      "description": "Evaluate startup health from latest revenue, burn, and cash snapshot.\n",
      "parameters": {
        "type": "object",
        "properties": {
          "revenue": {
            "type": "number",
            "description": "latest recurring or monthly revenue\n"
          },
          "burn": {
            "type": "number",
            "description": "current monthly burn rate\n"
          },
          "cash": {
            "type": "number",
            "description": "current cash reserves\n"
          }
        },
        "required": [
          "revenue",
          "burn",
          "cash"
        ]
      }
    }
  }
]"#
        .to_string()
    }

    #[query]
    fn prompts(&self) -> String {
        r#"{
  "prompts": []
}"#
        .to_string()
    }
}
