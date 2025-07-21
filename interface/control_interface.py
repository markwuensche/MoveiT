import queue

def run_interface(in_queue, out_queue, base_speed=1.0):
    """Translate classifier results into tunnel movement speed."""
    speed = base_speed
    while True:
        try:
            command = in_queue.get(timeout=1.0)
        except queue.Empty:
            continue

        if command == 'speed_up':
            speed += 0.1
        elif command == 'slow_down':
            speed = max(0.1, speed - 0.1)

        out_queue.put(speed)
