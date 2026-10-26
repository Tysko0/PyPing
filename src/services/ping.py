import platform, re, subprocess, threading, time

class PingServices:
    MAX_FAILURES = 3

    def __init__(self):
        self.stop_event = threading.Event()
        self.worker = None

    @staticmethod
    def extract_latency(output):
        patterns = [
            r"time[=<]\s*([\d.,]+)\s*ms",
            r"temps[=<]\s*([\d.,]+)\s*ms",
        ]

        for pattern in patterns:
            match = re.search(pattern, output, re.IGNORECASE)

            if match:
                try:
                    return float(match.group(1).replace(",", "."))
                except ValueError:
                    pass

        return None

    def start(self, host, interval, callback):
        if self.worker and self.worker.is_alive():
            return False

        self.stop_event.clear()
        self.worker = threading.Thread(
            target=self._run,
            args=(host, interval, callback),
            daemon=True,
        )
        self.worker.start()

        return True

    def _run(self, host, interval, callback):
        windows = platform.system().lower() == "windows"
        failures = 0
        reason = "stopped"

        try:
            while not self.stop_event.is_set():
                started = time.perf_counter()

                command = (
                    ["ping", "-n", "1", "-w", "1000", host]
                    if windows
                    else ["ping", "-c", "1", "-W", "1", host]
                )

                try:
                    result = subprocess.run(
                        command,
                        capture_output=True,
                        text=True,
                        errors="replace",
                        timeout=3,
                        check=False,
                    )

                    output = ((result.stdout or "") + "\n" + (result.stderr or ""))
                    success = result.returncode == 0
                    latency = (self.extract_latency(output) if success else None)

                    if success and latency is None:
                        latency = round((time.perf_counter() - started) * 1000, 2,)

                    message = ("Réponse reçue" if success else "Aucune réponse")

                except (OSError, subprocess.SubprocessError) as exc:
                    success = False
                    latency = None
                    message = f"Erreur : {type(exc).__name__}"

                callback({
                    "success": success,
                    "latency": latency,
                    "message": message,
                })

                if success:
                    failures = 0
                else:
                    failures += 1

                if failures >= self.MAX_FAILURES:
                    reason = "inactive"
                    break

                if self.stop_event.wait(interval):
                    break

        finally:
            callback({"type": "stopped", "reason": reason})

    def stop(self):
        self.stop_event.set()