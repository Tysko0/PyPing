import tkinter as tk

class PingPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#111a2e", padx=24, pady=24)

        tk.Label(
            self,
            text="Résultat du ping",
            bg="#111a2e",
            fg="#94a3b8",
            font=("Segoe UI", 10),
        ).pack(anchor="w")

        self.result_label = tk.Label(
            self,
            text="En attente d'un test",
            bg="#111a2e",
            fg="#f8fafc",
            font=("Segoe UI", 20, "bold"),
            wraplength=650,
        )
        self.result_label.pack(anchor="w", pady=(12, 8))

        self.latency_label = tk.Label(
            self,
            text="Latence : —",
            bg="#111a2e",
            fg="#cbd5e1",
            font=("Segoe UI", 12),
        )
        self.latency_label.pack(anchor="w")

    def update_result(self, event):
        if event.get("type") == "stopped":
            return

        if event["success"]:
            self.result_label.configure(text="Connexion réussie", fg="#86efac")
        else:
            self.result_label.configure(text=event["message"], fg="#fca5a5")

        latency = event["latency"]
        self.latency_label.configure(text=(f"Latence : {latency:.2f} ms" if latency is not None else "Latence : indisponible"))

    def reset(self):
        self.result_label.configure(text="En attente d'un test", fg="#f8fafc")
        self.latency_label.configure(text="Latence : —")