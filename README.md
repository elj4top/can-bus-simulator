# CAN Bus Simulator

A Python simulation of a vehicle's CAN (Controller Area Network) bus, demonstrating how multiple independent ECUs share one network and communicate using arbitration IDs — built as part of a 5-project automotive diagnostics portfolio.

## What it does
- Simulates two independent vehicle modules: an Engine Control Unit (sending RPM) and a Transmission Control Unit (sending vehicle speed)
- Both modules send on a shared virtual CAN bus, each on its own arbitration ID
- A listener decodes both message types using a data-driven signal reference (`dbc_reference.py`), inspired by how real automotive DBC files document CAN signals

## Files
- `can_demo.py` — runs the full simulation: two sender threads (engine, transmission) and one listener thread, all sharing a virtual CAN bus
- `dbc_reference.py` — a simplified signal reference documenting what each arbitration ID means and how to decode its payload (name, sender, byte range, scale, unit)

## Usage
```bash
pip install python-can
python can_demo.py
```

## Design notes
This started as two separate scripts (a sender and a listener), which revealed that `python-can`'s virtual bus backend doesn't share state across separate OS processes by default. The fix was consolidating sender and listener logic into one script using threads, so all nodes reliably share the same in-memory virtual bus — a good example of a real constraint discovered through building, not assumed upfront.

## Status
Core simulation complete: multi-node communication, ID-based message filtering, data-driven decoding. Next: additional simulated modules (ABS, body control) to more fully represent a real vehicle's CAN topology.

## Part of
Automotive Technology & Diagnostics Portfolio — built toward automotive ECU/diagnostics specialization.
