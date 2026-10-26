class StatsServices:
    def __init__(self):
        self.reset();

    def reset(self):
        self.sent = 0
        self.received = 0
        self.latencies = []

    def add_result(self, event):
        self.sent += 1

        if event["success"]:
            self.received += 1

            if event["latency"] is not None:
                self.latencies.append(event["latency"])

    def get_stats(self):
        lost = self.sent - self.received

        return {
            "sent": self.sent,
            "received": self.received,
            "lost": lost,
            "loss_percent": (lost / self.sent * 100 if self.sent else 0),
            "min_latency": (min(self.latencies) if self.latencies else None),
            "avg_latency": (sum(self.latencies) / len(self.latencies) if self.latencies else None),
            "max_latency": (max(self.latencies) if self.latencies else None)
        }