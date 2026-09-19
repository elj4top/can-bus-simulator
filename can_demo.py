import can
import time
import random
import threading
from dbc_reference import decode, describe

ENGINE_RPM_ID = 0x0C0
VEHICLE_SPEED_ID = 0x0B0

def run_engine(bus, count=10):
    for _ in range(count):
        rpm = random.randint(750, 3000)
        raw = rpm * 4
        data = [raw >> 8, raw & 0xFF, 0, 0, 0, 0, 0, 0]
        bus.send(can.Message(arbitration_id=ENGINE_RPM_ID, data=data, is_extended_id=False))
        print(f"[Engine]       Sent RPM={rpm}  (ID=0x{ENGINE_RPM_ID:X})")
        time.sleep(0.5)

def run_transmission(bus, count=10):
    for _ in range(count):
        speed = random.uniform(0, 120)
        raw = round(speed * 10)
        data = [raw >> 8, raw & 0xFF, 0, 0, 0, 0, 0, 0]
        bus.send(can.Message(arbitration_id=VEHICLE_SPEED_ID, data=data, is_extended_id=False))
        print(f"[Transmission] Sent Speed={speed:.1f} km/h  (ID=0x{VEHICLE_SPEED_ID:X})")
        time.sleep(0.5)

def run_listener(bus, count=20):
    for _ in range(count):
        msg = bus.recv(timeout=2)
        if msg is None:
            continue
        value = decode(msg.arbitration_id, msg.data)
        if value is not None:
            print(f"    [Listener] {describe(msg.arbitration_id)} -> {value}")

if __name__ == "__main__":
    engine_bus = can.interface.Bus(channel='test', bustype='virtual')
    trans_bus = can.interface.Bus(channel='test', bustype='virtual')
    listener_bus = can.interface.Bus(channel='test', bustype='virtual')

    listener_thread = threading.Thread(target=run_listener, args=(listener_bus,))
    listener_thread.start()

    engine_thread = threading.Thread(target=run_engine, args=(engine_bus,))
    trans_thread = threading.Thread(target=run_transmission, args=(trans_bus,))
    engine_thread.start()
    trans_thread.start()

    engine_thread.join()
    trans_thread.join()
    listener_thread.join()

    engine_bus.shutdown()
    trans_bus.shutdown()
    listener_bus.shutdown()
