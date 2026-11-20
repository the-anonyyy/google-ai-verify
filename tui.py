from __future__ import annotations
# Google Ai Kit™ - TUI Dashboard
# Anony · t.me/CracKz_Hubb
import os
import sys
import subprocess
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Button, Label, RichLog, Static
from textual.worker import Worker, WorkerState
import ultra0

class GoogleAiKit(App):
    CSS = """
    Screen { background: $surface-darken-1; }
    #main-container { padding: 1; }
    .action-btn { width: 100%; margin-bottom: 1; }
    #log-panel { height: 1fr; border: solid $primary; margin-top: 1; }
    .status-label { margin-bottom: 1; color: $text-muted; }
    """
    
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="main-container"):
            yield Static("Google Ai Kit™ - Any Google Subscription Unlocked", classes="status-label")
            yield Static("Channel: https://t.me/CracKz_Hubb", classes="status-label")
            with Horizontal():
                with Vertical():
                    yield Button("Check Device & Offers", id="btn-check", variant="primary", classes="action-btn")
                    yield Button("Run Step 2 (12M)", id="btn-step2", variant="success", classes="action-btn")
                    yield Button("Run Step 3 (+6M)", id="btn-step3", variant="success", classes="action-btn")
                    yield Button("Run Step 4 (+6M)", id="btn-step4", variant="success", classes="action-btn")
                with Vertical():
                    yield Button("Environment (Step 0)", id="btn-env", variant="default", classes="action-btn")
                    yield Button("List Offers (Step 1)", id="btn-list", variant="default", classes="action-btn")
                    yield Button("Stop", id="btn-stop", variant="error", classes="action-btn")
            yield RichLog(id="log-panel", highlight=True, markup=True)
        yield Footer()

    def on_mount(self) -> None:
        self.log_msg("Ready. Ensure MuMuPlayer is running with ADB & Root enabled.")

    def log_msg(self, msg: str, color: str = "white") -> None:
        log = self.query_one("#log-panel", RichLog)
        log.write(f"[{color}]{msg}[/{color}]")

    def run_engine(self, args: list) -> None:
        self.log_msg(f"Running: ultra0.py {' '.join(args)}", "cyan")
        
        def _worker():
            try:
                cmd = [sys.executable, "ultra0.py"] + args
                process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
                )
                for line in process.stdout:
                    self.call_from_thread(self.log_msg, line.strip())
                process.wait()
                self.call_from_thread(self.log_msg, "Process finished.", "green")
            except Exception as e:
                self.call_from_thread(self.log_msg, f"Error: {e}", "red")

        self.run_worker(_worker, thread=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "btn-check":
            self.run_engine(["--check"])
        elif btn_id == "btn-list":
            self.run_engine(["--list", "--account", "current@device", "--no-add", "--force", "--plan", "pro12"])
        elif btn_id == "btn-step2":
            self.run_engine(["--account", "current@device", "--no-add", "--force", "--plan", "pro12"])
        elif btn_id == "btn-step3":
            self.run_engine(["--account", "current@device", "--no-add", "--force", "--stack", "--plan", "pro6"])
        elif btn_id == "btn-step4":
            self.run_engine(["--account", "current@device", "--no-add", "--force", "--stack", "--plan", "pro6b"])
        elif btn_id == "btn-env":
            self.run_engine(["--check"])
        elif btn_id == "btn-stop":
            self.log_msg("Stop signal sent (waiting for process to terminate).", "yellow")
            # Stop logic handled by engine exit

if __name__ == "__main__":
    app = GoogleAiKit()
    app.run()