from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# ✅ import your agent controller
from agent.workflow import run_agent

app = FastAPI()


# ✅ VERY IMPORTANT (for Next.js later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Request schema
class InputSchema(BaseModel):
    mode: str
    revenue: float
    burn: float
    cash: float


# ✅ Root route (so "/" not empty)
@app.get("/")
def root():
    return {"status": "ChainVest API running"}


# ✅ MAIN ENDPOINT
@app.post("/analyze")
def analyze(data: InputSchema):
    try:
        print("\n===== NEW REQUEST =====")
        print("INPUT:", data)

        # ✅ Build state EXACTLY like your workflow expects
        state = {
            "mode": data.mode,
            "revenue": [data.revenue] * 12,
            "burn": [data.burn] * 12,
            "cash": data.cash,
            "tool_results": {},
            "decision": None,
            "finished": False,
            "next_step": None,
            "logs": [],
            "tx_hashes": []
        }

        # ✅ Run agent (correct way)
        result = run_agent(state)

        print("RESULT:", result)

        return result

    except Exception as e:
        import traceback
        traceback.print_exc()

        return {
            "status": "error",
            "message": str(e)
        }