
import queue
import tkinter as tk
from tkinter import messagebox, ttk

from screens.ping import PingPanel
from screens.stats import StatsPanel

from services.stats import StatsServices
from services.ping import PingServices


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("PyPing v1.0.2")
        self.root.geometry("900x750")
        self.root.minsize(750, 650)
        self.root.configure(bg="#0b1020")

        self.events = queue.Queue()
        self.ping_service = PingServices()
        self.stats_service = StatsServices()
        self.running = False

        self._configure_style()
        self._build_ui()

        self.root.after(100, self._process_events)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TCombobox",
            fieldbackground="#111a2e",
            background="#1e293b",
            foreground="#f8fafc",
            arrowcolor="#f8fafc",
        )

    def _build_ui(self):
        header = tk.Frame(self.root, bg="#0b1020")
        header.pack(fill="x", padx=24, pady=(20, 12))

        tk.Label(
            header,
            text="PyPing",
            bg="#0b1020",
            fg="#f8fafc",
            font=("Segoe UI", 26, "bold"),
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Testeur de connectivité réseau · v1.0.1",
            bg="#0b1020",
            fg="#94a3b8",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(3, 0))

        controls = tk.Frame(
            self.root,
            bg="#111a2e",
            padx=16,
            pady=16,
        )
        controls.pack(fill="x", padx=24, pady=8)

        tk.Label(
            controls,
            text="Hôte ou adresse IP",
            bg="#111a2e",
            fg="#cbd5e1",
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=0, sticky="w")

        self.host_var = tk.StringVar(value="google.com")
        self.host_entry = tk.Entry(
            controls,
            textvariable=self.host_var,
            bg="#0b1020",
            fg="#f8fafc",
            insertbackground="#f8fafc",
            relief="flat",
            font=("Segoe UI", 11),
        )
        self.host_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            ipady=8,
            padx=(0, 12),
            pady=(6, 0),
        )

        tk.Label(
            controls,
            text="Intervalle",
            bg="#111a2e",
            fg="#cbd5e1",
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=1, sticky="w")

        self.interval_var = tk.StringVar(value="1")
        self.interval_box = ttk.Combobox(
            controls,
            textvariable=self.interval_var,
            values=("1", "2", "5", "10"),
            state="readonly",
            width=7,
        )
        self.interval_box.grid(
            row=1,
            column=1,
            sticky="ew",
            ipady=4,
            pady=(6, 0),
        )

        self.start_btn = tk.Button(
            controls,
            text="Démarrer",
            command=self.start_ping,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            padx=14,
            pady=8,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )
        self.start_btn.grid(
            row=1,
            column=2,
            padx=(12, 6),
            pady=(6, 0),
        )

        self.stop_btn = tk.Button(
            controls,
            text="Arrêter",
            command=self.stop_ping,
            state="disabled",
            bg="#334155",
            fg="#e2e8f0",
            activebackground="#475569",
            activeforeground="#e2e8f0",
            relief="flat",
            padx=14,
            pady=8,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )
        self.stop_btn.grid(row=1, column=3, pady=(6, 0))
        controls.columnconfigure(0, weight=1)

        tk.Label(
            self.root,
            text="RÉSULTAT DU PING",
            bg="#0b1020",
            fg="#94a3b8",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=24, pady=(10, 4))

        self.ping_panel = PingPanel(self.root)
        self.ping_panel.pack(fill="x", padx=24, pady=(0, 8))

        tk.Label(
            self.root,
            text="STATISTIQUES RÉSEAU",
            bg="#0b1020",
            fg="#94a3b8",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=24, pady=(8, 4))

        self.stats_panel = StatsPanel(self.root)
        self.stats_panel.pack(
            fill="x",
            padx=20,
            pady=(0, 12),
        )

        self.status_var = tk.StringVar(value="Prêt")
        tk.Label(
            self.root,
            textvariable=self.status_var,
            bg="#111a2e",
            fg="#94a3b8",
            anchor="w",
            padx=24,
            pady=8,
            font=("Segoe UI", 9),
        ).pack(fill="x", side="bottom")

    def start_ping(self):
        host = self.host_var.get().strip()

        if not host or any(char.isspace() for char in host):
            messagebox.showerror(
                "Hôte invalide",
                "Saisis un nom de domaine ou une adresse IP.",
            )
            return

        try:
            interval = float(self.interval_var.get())
        except ValueError:
            messagebox.showerror(
                "Intervalle invalide",
                "Choisis un intervalle valide.",
            )
            return

        if self.running:
            return

        self.stats_service.reset()
        self.stats_panel.reset()
        self.ping_panel.reset()

        started = self.ping_service.start(
            host,
            interval,
            self.events.put,
        )

        if not started:
            messagebox.showwarning(
                "Test en cours",
                "Un test réseau est déjà en cours.",
            )
            return

        self.running = True
        self.host_entry.configure(state="disabled")
        self.interval_box.configure(state="disabled")
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.status_var.set(f"Ping en cours vers {host}")

    def stop_ping(self):
        if self.running:
            self.ping_service.stop()
            self.stop_btn.configure(state="disabled")
            self.status_var.set("Arrêt du ping…")

    def _process_events(self):
        try:
            while True:
                event = self.events.get_nowait()

                if event.get("type") == "stopped":
                    self._handle_stopped(event)
                    continue

                self.stats_service.add_result(event)
                self.stats_panel.update_stats(
                    self.stats_service.get_stats()
                )
                self.ping_panel.update_result(event)

                latency = event.get("latency")
                latency_text = (
                    f"{latency:.2f} ms"
                    if latency is not None
                    else "Latence indisponible"
                )

                self.status_var.set(
                    f'{event["message"]} — {latency_text}'
                )

        except queue.Empty:
            pass

        try:
            if self.root.winfo_exists():
                self.root.after(100, self._process_events)
        except tk.TclError:
            pass

    def _handle_stopped(self, event=None):
        self.running = False
        self.host_entry.configure(state="normal")
        self.interval_box.configure(state="readonly")
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")

        if event and event.get("reason") == "inactive":
            self.ping_panel.result_label.configure(
                text="Hôte inactif — aucune réponse après 3 tentatives",
                fg="#fca5a5",
            )
            self.status_var.set("Test arrêté : hôte inactif")
        else:
            self.status_var.set("Ping arrêté")

    def _on_close(self):
        self.ping_service.stop()
        self.root.destroy()
