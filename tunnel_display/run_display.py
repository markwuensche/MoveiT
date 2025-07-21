
import cv2
import queue
from .tunnel_module import TunnelRenderer, default_params


def run_display(speed_queue):
    """Display the tunnel stimulus controlled by movement speed."""
    params = default_params()
    renderer = TunnelRenderer(params)
    cam_z = 0.0
    speed = params['speed']
    dt = 1.0 / params['fps']
    delay = int(1000 / params['fps'])

    try:
        while True:
            try:
                speed = speed_queue.get_nowait()
            except queue.Empty:
                pass

            cam_z += speed * dt
            frame = renderer.render_frame(cam_z)
            cv2.imshow('Tunnel', frame)
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
    finally:
        renderer.release()
        cv2.destroyAllWindows()
