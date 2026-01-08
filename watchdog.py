import subprocess
import time
import os

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "server.py")
HEARTBEAT_FILE = os.path.join(os.path.dirname(__file__), "heartbeat.txt")
CHECK_INTERVAL = 5        # seconds
FREEZE_THRESHOLD = 10     # seconds without heartbeat considered frozen

def start_app():
    return subprocess.Popen([os.sys.executable, SCRIPT_PATH])

def main():
    print("[Watchdog] Starting Medimind...")
    proc = start_app()

    try:
        while True:
            time.sleep(CHECK_INTERVAL)

            # Check if process crashed
            if proc.poll() is not None:
                print("[Watchdog] Medimind stopped unexpectedly. Restarting...")
                proc = start_app()
                continue

            # Check heartbeat
            if os.path.exists(HEARTBEAT_FILE):
                with open(HEARTBEAT_FILE, "r") as f:
                    last_beat = float(f.read().strip())
                if time.time() - last_beat > FREEZE_THRESHOLD:
                    print("[Watchdog] Freeze detected. Restarting Medimind...")
                    proc.terminate()
                    proc.wait()
                    proc = start_app()
            else:
                print("[Watchdog] No heartbeat file found. Restarting Medimind...")
                proc.terminate()
                proc.wait()
                proc = start_app()

    except KeyboardInterrupt:
        print("[Watchdog] Exiting. Terminating Medimind.")
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    main()
