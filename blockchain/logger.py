import hashlib
import json
import uuid
from datetime import datetime


# =========================
# HASH ENGINE
# =========================
def hash_data(data):
    """Convert any data → SHA256 hash"""
    if data is None:
        return None
    serialized = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(serialized).hexdigest()


# =========================
# FULL STAGE-5 LOGGER
# =========================
def log_to_chain(state, step_name, input_data=None, output_data=None):

    input_hash = hash_data(input_data)
    output_hash = hash_data(output_data)
    state_hash = hash_data(state)

    tx_hash = f"0x{uuid.uuid4().hex[:16]}"
    timestamp = datetime.now().isoformat()

    log_entry = {
        "timestamp": timestamp,
        "step": step_name,
        "input_hash": input_hash,
        "output_hash": output_hash,
        "state_hash": state_hash,
        "tx_hash": tx_hash,
    }

    if "logs" not in state:
        state["logs"] = []

    if "tx_hashes" not in state:
        state["tx_hashes"] = []

    state["logs"].append(log_entry)
    state["tx_hashes"].append(tx_hash)

    return state