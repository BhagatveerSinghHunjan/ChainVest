from __future__ import annotations

import asyncio
import json
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Any, Optional

try:
    from weil_wallet import PrivateKey, Wallet, WeilClient

    WEIL_WALLET_AVAILABLE = True
except Exception:
    PrivateKey = Wallet = WeilClient = None  # type: ignore[assignment]
    WEIL_WALLET_AVAILABLE = False

try:
    from fastmcp import FastMCP
except Exception:
    FastMCP = None  # type: ignore[assignment]

try:
    from weil_ai.mcp import secured, weil_middleware
except Exception:
    secured = None  # type: ignore[assignment]
    weil_middleware = None  # type: ignore[assignment]


def _safe_float(value: Any, *, minimum: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        parsed = minimum
    return max(parsed, minimum)


def _score_startup(revenue: float, burn: float, cash: float) -> dict[str, Any]:
    score = (revenue / (burn + 1.0)) * (cash / 10000.0)

    if score > 5:
        decision = "APPROVE"
    elif score > 2:
        decision = "REVIEW"
    else:
        decision = "REJECT"

    return {"decision": decision, "score": round(score, 2)}


def _resolve_private_key_path() -> Optional[str]:
    candidates = [
        os.getenv("WEIL_PRIVATE_KEY_PATH"),
        os.getenv("WEIL_PRIVATE_KEY_FILE"),
        os.path.join(os.getcwd(), "private_key.wc"),
        os.path.join(os.path.dirname(__file__), "private_key.wc"),
    ]

    for path in candidates:
        if path and os.path.isfile(path):
            return path
    return None


def _run_sync(coro):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    # If already inside an event loop, run in a worker thread.
    with ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(asyncio.run, coro).result()


async def _audit_on_weil(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    if not WEIL_WALLET_AVAILABLE:
        return None

    key_path = _resolve_private_key_path()
    if not key_path:
        return None

    sentinel_host = os.getenv("WEIL_SENTINEL_HOST")
    verify_tls = os.getenv("WEIL_SENTINEL_VERIFY", "true").lower() not in {
        "0",
        "false",
        "no",
    }

    try:
        pk = PrivateKey.from_file(key_path)
        wallet = Wallet(pk)

        kwargs = {"verify": verify_tls}
        if sentinel_host:
            kwargs["sentinel_host"] = sentinel_host

        async with WeilClient(wallet, **kwargs) as client:
            tx = await client.audit(json.dumps(payload))
            return {
                "status": str(getattr(tx, "status", "UNKNOWN")),
                "block_height": getattr(tx, "block_height", None),
                "batch_id": getattr(tx, "batch_id", None),
                "tx_idx": getattr(tx, "tx_idx", None),
                "creation_time": getattr(tx, "creation_time", None),
                "txn_result": getattr(tx, "txn_result", None),
            }
    except Exception as exc:
        return {"error": str(exc)}


def evaluate_startup(revenue: float, burn: float, cash: float) -> dict[str, Any]:
    revenue = _safe_float(revenue)
    burn = _safe_float(burn)
    cash = _safe_float(cash)

    result = _score_startup(revenue, burn, cash)
    payload = {
        "source": "chainvest",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {"revenue": revenue, "burn": burn, "cash": cash},
        "evaluation": result,
    }

    result["audit"] = {
        "enabled": WEIL_WALLET_AVAILABLE,
        "key_found": _resolve_private_key_path() is not None,
        "on_chain": False,
    }

    onchain = _run_sync(_audit_on_weil(payload))
    if onchain:
        result["audit"]["on_chain"] = "error" not in onchain
        result["audit"]["details"] = onchain

    return result


def create_mcp_app():
    if FastMCP is None:
        raise RuntimeError("fastmcp is not installed. Install it to run ChainVest MCP.")

    mcp = FastMCP("chainvest-mcp")
    secured_service = os.getenv("WEIL_MCP_SERVICE_NAME")

    if secured is not None and secured_service:

        @mcp.tool()
        @secured(secured_service)
        async def evaluate_startup_tool(revenue: float, burn: float, cash: float) -> str:
            return json.dumps(evaluate_startup(revenue, burn, cash))

    else:

        @mcp.tool()
        async def evaluate_startup_tool(revenue: float, burn: float, cash: float) -> str:
            return json.dumps(evaluate_startup(revenue, burn, cash))

    app = mcp.http_app(transport="streamable-http")
    if weil_middleware is not None:
        app.add_middleware(weil_middleware())
    return app


__all__ = ["create_mcp_app", "evaluate_startup"]


if __name__ == "__main__":
    import uvicorn

    app = create_mcp_app()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("MCP_PORT", "8001")))

