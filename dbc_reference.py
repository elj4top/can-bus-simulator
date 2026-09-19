# Simplified CAN signal reference — same purpose as a real .dbc file:
# documents what each arbitration ID means and how to decode its payload.

CAN_SIGNALS = {
    0x0C0: {
        "name": "Engine RPM",
        "sender": "Engine Control Unit",
        "byte_range": (0, 2),       # bytes 0-1 hold this value
        "scale": 4,                 # raw_value / scale = real RPM
        "unit": "rpm",
    },
    0x0B0: {
        "name": "Vehicle Speed",
        "sender": "Transmission Control Unit",
        "byte_range": (0, 2),
        "scale": 10,                # raw_value / scale = real km/h
        "unit": "km/h",
    },
}

def describe(arbitration_id):
    signal = CAN_SIGNALS.get(arbitration_id)
    if signal is None:
        return f"Unknown ID 0x{arbitration_id:X} — not in reference"
    return (f"0x{arbitration_id:X}: {signal['name']} "
            f"(from {signal['sender']}, unit: {signal['unit']})")

def decode(arbitration_id, data):
    signal = CAN_SIGNALS.get(arbitration_id)
    if signal is None:
        return None
    start, end = signal["byte_range"]
    raw = int.from_bytes(data[start:end], byteorder="big")
    return raw / signal["scale"]
