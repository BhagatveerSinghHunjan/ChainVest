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


# ✅ Root test route (so "/" not empty)
@app.get("/")
def root():
    return {"status": "ChainVest API running"}


# ✅ MAIN ENDPOINT
@app.post("/analyze")
def analyze(data: InputSchema):
    try:
        print("\n===== NEW REQUEST =====")
        print("INPUT:", data)

        # ✅ Convert API input → agent format
        result = run_agent(
    data.mode,
    [data.revenue] * 12,
    [data.burn] * 12,
    data.cash,
)

        print("RESULT:", result)

        return result

    except Exception as e:
        import traceback
        traceback.print_exc()

        return {
            "status": "error",
            "message": str(e)
        }