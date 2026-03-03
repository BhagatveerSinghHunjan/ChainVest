import uuid
import datetime


def log_step(state, step_name):

    tx_hash = f"0x{uuid.uuid4().hex[:16]}"
    timestamp = datetime.datetime.now().isoformat()

    if "logs" not in state:
        state["logs"] = []

    if "tx_hashes" not in state:
        state["tx_hashes"] = []

    state["logs"].append({
        "timestamp": timestamp,
        "step": step_name,
        "tx_hash": tx_hash
    })

    state["tx_hashes"].append(tx_hash)

    return state