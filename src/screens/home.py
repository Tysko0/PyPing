import queue
import tkinter as tk
from tkinter import messagebox, ttk

from screens.ping import PingPanel
from services.ping import PingServices


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("PyPing")
        self.root.geometry("760x480")
        self.root.minsize(600, 420)
        self.root.configure(bg="#0b1020")

        self.events = queue.Queue()
        self.ping_service = PingServices()
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
        header.pack(fill="x", padx=28, pady=(28, 20))

        tk.Label(
            header,
            text="PyPing",
            bg="#0b1020",
            fg="#f8fafc",
            font=("Segoe UI", 28, "bold"),
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Outil de test de connectivité réseau",
            bg="#0b1020",
            fg="#94a3b8",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))

        panel = tk.Frame(
            self.root,
            bg="#111a2e",
            padx=20,
            pady=20,
        )
        panel.pack(fill="x", padx=28, pady=(0, 16))

        tk.Label(
            panel,
            text="Hôte ou adresse IP",
            bg="#111a2e",
            fg="#cbd5e1",
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=0, sticky="w")

        self.host_var = tk.StringVar(value="google.com")

        self.host_entry = tk.Entry(
            panel,
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
            ipady=9,
            padx=(0, 16),
            pady=(8, 0),
        )

        tk.Label(
            panel,
            text="Intervalle",
            bg="#111a2e",
            fg="#cbd5e1",
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=1, sticky="w")

        self.interval_var = tk.StringVar(value="1")

        self.interval_box = ttk.Combobox(
            panel,
            textvariable=self.interval_var,
            values=("1", "2", "5", "10"),
            state="readonly",
            width=8,
        )
        self.interval_box.grid(
            row=1,
            column=1,
            sticky="ew",
            ipady=5,
            pady=(8, 0),
        )

        self.start_btn = tk.Button(
            panel,
            text="Démarrer",
            command=self.start_ping,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=9,
            cursor="hand2",
        )
        self.start_btn.grid(
            row=1,
            column=2,
            padx=(16, 8),
            pady=(8, 0),
        )

        self.stop_btn = tk.Button(
            panel,
            text="Arrêter",
            command=self.stop_ping,
            state="disabled",
            bg="#334155",
            fg="#e2e8f0",
            activebackground="#475569",
            activeforeground="#e2e8f0",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=9,
            cursor="hand2",
        )
        self.stop_btn.grid(row=1, column=3, pady=(8, 0))

        panel.columnconfigure(0, weight=1)

        self.ping_panel = PingPanel(self.root)
        self.ping_panel.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=(0, 16),
        )

        self.status_var = tk.StringVar(value="Prêt")

        tk.Label(
            self.root,
            textvariable=self.status_var,
            bg="#111a2e",
            fg="#94a3b8",
            anchor="w",
            padx=28,
            pady=10,
            font=("Segoe UI", 9),
        ).pack(fill="x", side="bottom")

    def start_ping(self):
        host = self.host_var.get().strip()

        if not host or any(char.isspace() for char in host):
            messagebox.showerror(
                "Hôte invalide",
                "Saisis un nom de domaine ou une adresse IP valide.",
            )
            return

        interval = float(self.interval_var.get())

        if not self.ping_service.start(host, interval, self.events.put):
            messagebox.showwarning(
                "Test en cours",
                "Un test est déjà en cours.",
            )
            return

        self.running = True
        self.host_entry.configure(state="disabled")
        self.interval_box.configure(state="disabled")
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")

        self.ping_panel.reset()
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
                    self._handle_stopped()
                else:
                    self.ping_panel.update_result(event)

        except queue.Empty:
            pass

        if self.root.winfo_exists():
            self.root.after(100, self._process_events)

    def _handle_stopped(self):
        self.running = False
        self.host_entry.configure(state="normal")
        self.interval_box.configure(state="readonly")
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_var.set("Ping arrêté")

    def _on_close(self):
        self.ping_service.stop()
        self.root.destroy()