ChainVest

Blockchain-Verified AI Financial Due Diligence Engine

Stage 1 - Deterministic Financial Core

Implemented:

Structured financial input schemas (Pydantic)
Financial Trend Analyzer
Unit Economics Engine
Local testing harness

Next:

Projection Engine
Loan Risk Engine
Scoring Layer
Agentic orchestration (LangGraph)
Weilchain integration

Stage 2 - Structured Workflow & AI Explanation Layer

Implemented:

Streamlit-based financial input interface
Backend workflow layer connecting financial core to UI
Deterministic decision generation (Runway → Risk Classification)
AI explanation engine (OpenAI integration)
Structured step-by-step execution logging (simulated transaction hashes)
Modular separation of UI, logic, and logging

Next:

Replace linear workflow with agent-based orchestration
Introduce state-driven execution model
Add conditional branching logic
Prepare blockchain logging layer for integration

Stage 3 - Agentic Orchestration & Blockchain Audit Architecture

Implemented:

State-driven architecture for multi-step execution
LangGraph-based agent workflow
Planner node for explicit control logic
Tool execution layer (Financial Tool + Risk Tool)
Conditional execution loop with termination logic
Dedicated blockchain logger module (Weilchain-ready)
Step-level logging for:

Planner decisions

Tool executions

Final decision generation
Structured storage of transaction hashes inside state

Next:

Replace simulated logger with real Weilchain Python SDK
Expand tool set (Projection Engine, Loan Risk Engine)
Add VC Evaluation mode
Add Business Loan mode
Add weighted scoring and aggregation layer
Deploy on-chain audit verification interface
