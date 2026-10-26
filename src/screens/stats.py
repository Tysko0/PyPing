import tkinter as tk

class StatsPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0b1020")

        self.labels = {}

        cards = [
            ("sent", "ENVOYÉS"),
            ("received", "REÇUS"),
            ("lost", "PERDUS"),
            ("loss_percent", "PERTES"),
            ("min_latency", "LATENCE MIN."),
            ("avg_latency", "LATENCE MOY."),
            ("max_latency", "LATENCE MAX."),
        ]

        for index, (key, title) in enumerate(cards):
            card = tk.Frame(
                self,
                bg="#111a2e",
                padx=12,
                pady=12,
            )
            card.grid(
                row=index // 4,
                column=index % 4,
                sticky="nsew",
                padx=4,
                pady=4,
            )

            tk.Label(
                card,
                text=title,
                bg="#111a2e",
                fg="#94a3b8",
                font=("Segoe UI", 8, "bold"),
            ).pack(anchor="w")

            label = tk.Label(
                card,
                text="0" if key in ("sent", "received", "lost")
                else "—",
                bg="#111a2e",
                fg="#f8fafc",
                font=("Segoe UI", 15, "bold"),
            )
            label.pack(anchor="w", pady=(5, 0))

            self.labels[key] = label

        for column in range(4):
            self.columnconfigure(column, weight=1)

    def update_stats(self, stats):
        for key in ("sent", "received", "lost"):
            self.labels[key].configure(text=str(stats[key]))

        self.labels["loss_percent"].configure(text=f'{stats["loss_percent"]:.1f}%')

        for key in ("min_latency", "avg_latency", "max_latency"):
            value = stats[key]
            self.labels[key].configure(text=f"{value:.2f} ms" if value is not None else "—")

    def reset(self):
        self.update_stats({
            "sent": 0,
            "received": 0,
            "lost": 0,
            "loss_percent": 0,
            "min_latency": None,
            "avg_latency": None,
            "max_latency": None,
        })