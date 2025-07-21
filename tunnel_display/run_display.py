import cv2
import queue
import matplotlib.pyplot as plt
from .tunnel_module import TunnelRenderer, default_params


def show_frame_matplotlib(frame):
    """Fallback: display frame using matplotlib."""
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.draw()
    plt.pause(0.001)
    plt.clf()


def run_display(speed_queue):
    """Display the tunnel stimulus controlled by movement speed."""
    params = default_params()
    renderer = TunnelRenderer(params)
    cam_z = 0.0
    speed = params['speed']
    dt = 1.0 / params['fps']
    delay = int(1000 / params['fps'])

    use_matplotlib = False

    try:
        plt.ion()  # for live matplotlib updates
        while True:
            try:
                speed = speed_queue.get_nowait()
            except queue.Empty:
                pass

            cam_z += speed * dt
            frame = renderer.render_frame(cam_z)

            if use_matplotlib:
                show_frame_matplotlib(frame)
            else:
                try:
                    cv2.imshow('Tunnel', frame)
                    if cv2.waitKey(delay) & 0xFF == ord('q'):
                        break
                except cv2.error as e:
                    print("cv2.imshow failed, switching to matplotlib fallback.")
                    use_matplotlib = True
                    show_frame_matplotlib(frame)
    finally:
        renderer.release()
        if not use_matplotlib:
            try:
                cv2.destroyAllWindows()
            except cv2.error as e:
                print("cv2.destroyAllWindows failed:", e)
