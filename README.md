ChainVest

Blockchain-Verified AI Financial Due Diligence Engine

Stage 1 - Deterministic Financial Core

Implemented:

Structured financial input schemas (Pydantic)
Financial Trend Analyzer
Unit Economics Engine
Local testing harness

Details:

Structured financial input schemas (Pydantic)

Defined validated models for financial inputs including revenue, burn rate, cash, and unit metrics

Enforced strict typing and validation rules

Prevented malformed, missing, or invalid financial data

Financial Trend Analyzer

Implemented runway calculation (cash / burn)

Generated baseline liquidity assessment

Produced structured financial metrics

Unit Economics Engine

Calculated LTV/CAC ratio

Provided early sustainability indicators

Structured deterministic output for downstream processing

Local testing harness

CLI-based execution for financial validation

Independent backend testing without UI dependency

Ensured deterministic correctness before orchestration

Next:

Projection Engine
Loan Risk Engine
Scoring Layer
Agentic orchestration (LangGraph)
Weilchain integration

Stage 2 - Structured Workflow & AI Explanation Layer

Implemented:

Streamlit-based financial input interface
Backend workflow integration layer
Deterministic decision generation
AI explanation engine (OpenAI integration)
Structured execution logging (simulated transaction hashes)
Modular separation of UI, logic, and logging

Details:

Streamlit-based financial input interface

Implemented structured user input collection

Connected frontend to backend logic

Displayed financial metrics and decisions clearly

Backend workflow integration layer

Connected Stage 1 deterministic engine to UI

Executed structured flow:
Financial Analysis → Risk Classification → Decision Generation

Maintained clean separation between UI and computation logic

Deterministic decision generation

Classified risk based on runway thresholds

Generated structured decision outputs

Preserved transparency of calculation logic

AI explanation engine (OpenAI integration)

Generated human-readable explanation of deterministic decision

Improved interpretability of financial results

Maintained separation between explanation and calculation

Structured execution logging (simulated)

Logged step-by-step workflow execution

Generated transaction-style identifiers

Prepared infrastructure for blockchain integration

Limitations at Stage 2:

Linear workflow without multi-step control loop
No conditional branching between tool executions
No explicit agent termination logic
No immutable audit logging

Next:

Replace linear workflow with state-driven agent system
Introduce planner-based execution logic
Add conditional branching using LangGraph
Design dedicated blockchain logging layer

Stage 3 - Agentic Orchestration & Blockchain Audit Architecture

Implemented:

State-driven architecture
LangGraph-based workflow orchestration
Planner node for explicit control logic
Tool execution layer (Financial Tool + Risk Tool)
Conditional multi-step execution loop
Explicit termination logic
Dedicated blockchain logger module (Weilchain-ready)
Step-level logging for planner, tools, and final decision
Structured storage of transaction hashes inside agent state

Details:

State-driven architecture

Introduced centralized state object

Stored mode, financial inputs, tool results, logs, transaction hashes, and final decision

Enabled controlled multi-step reasoning

LangGraph-based workflow orchestration

Defined nodes: Planner, Tool Executor, Finalizer

Implemented controlled state transitions

Prevented uncontrolled execution paths

Planner node

Evaluated current state

Determined next action (financial tool, risk tool, finalize)

Enforced explicit decision logic

Logged planner decisions

Tool execution layer

Financial Tool: calculated runway

Risk Tool: classified financial risk

Updated state after execution

Logged tool inputs and outputs

Conditional multi-step execution loop

Implemented planner → tool → planner loop

Continued until all required steps executed

Enabled dynamic control flow

Explicit termination logic

Finalized decision only after required tools executed

Marked state as finished

Logged final decision

Dedicated blockchain logger module

Centralized infrastructure layer for audit logging

Logged every planner decision

Logged every tool execution

Logged final decision

Generated transaction hashes (simulated)

Designed for replacement with Weilchain Python SDK

Blockchain integration design (Weilchain-ready)

Logger layer isolated from business logic

Replace simulated transaction generator with Weilchain SDK

Write planner decisions on-chain

Write tool executions on-chain

Write final decision on-chain

Store returned transaction hashes in state

System Architecture (Stage 3):

User Input
→ State Initialization
→ Planner Node
→ Tool Execution
→ Logger (Blockchain Layer)
→ Planner (loop)
→ Finalization
→ Immutable Audit Trail

Capabilities Achieved:

Deterministic financial computation
Explicit agentic workflow control
Structured tool orchestration
Conditional branching
Clear termination logic
Audit logging architecture
Blockchain-ready immutability layer

Next:

Replace simulated logger with real Weilchain SDK
Add Projection Engine
Add Loan Risk Engine
Add VC Evaluation mode
Add Business Loan mode
Add weighted scoring and aggregation layer
Deploy on-chain verification interface
