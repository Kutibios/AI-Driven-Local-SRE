import ollama
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console
from rich.panel import Panel

console = Console()

class AdvancedLogHandler(FileSystemEventHandler):
    def __init__(self):
        # Spam filter
        self.last_seen_errors = {}
        self.spam_window = 60  # wait for same error.

    def on_modified(self, event):
        # watch all .log files
        if not event.is_directory and event.src_path.endswith(".log"):
            filename = os.path.basename(event.src_path)
            try:
                with open(event.src_path, "r") as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        #  Just error and critical
                        if last_line and ("ERROR" in last_line.upper() or "CRITICAL" in last_line.upper()):
                            self.process_with_spam_filter(last_line, filename)
            except Exception as e:
                console.print(f"[dim red]Error reading file {filename}: {e}[/dim red]")

    def process_with_spam_filter(self, log_line, filename):
        current_time = time.time()
        
        # SPAM controll
        if log_line in self.last_seen_errors:
            time_diff = current_time - self.last_seen_errors[log_line]
            if time_diff < self.spam_window:
                # just warning (AI does not working)
                console.print(f"[dim] Spam Filter: Similar error from {filename} ignored (Wait {int(self.spam_window - time_diff)}s)[/dim]")
                return

        # pass filter , send to AI
        self.last_seen_errors[log_line] = current_time
        self.analyze_with_ai(log_line, filename)

    def analyze_with_ai(self, log_line, source_file):
        console.print(Panel(f"[bold cyan]Source File:[/bold cyan] {source_file}\n[bold yellow]Error Detected:[/bold yellow]\n{log_line}", title="🔎 Monitoring"))
        
        try:
            # say AI that which files have errors  
            response = ollama.chat(model='tinyllama', messages=[
                {'role': 'system', 'content': f'You are a professional DevOps Assistant. This error comes from {source_file}. Explain very briefly and provide a technical solution.'},
                {'role': 'user', 'content': log_line},
            ])
            
            ai_comment = response['message']['content']
            
            # 1. to terminal
            console.print(Panel(f"[bold green]AI Analysis (Context: {source_file}):[/bold green]\n{ai_comment}", title="🤖 TinyLlama AI"))
            
            # 2. save to file
            self.save_to_report(log_line, ai_comment, source_file)
            
        except Exception as e:
            console.print(f"[bold red]AI Analysis Error:[/bold red] {e}")

    def save_to_report(self, log_line, ai_comment, source_file):
        report_dir = "reports"
        report_file = os.path.join(report_dir, "solutions.txt")
        
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
            
        with open(report_file, "a", encoding="utf-8") as f:
            f.write(f"{'='*60}\n")
            f.write(f"DATE      : {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"SOURCE    : {source_file}\n") #  say  which files errors came from
            f.write(f"LOG ENTRY : {log_line}\n")
            f.write(f"SOLUTION  : {ai_comment.strip()}\n")
            f.write(f"{'='*60}\n\n")
        
        console.print(f"[dim] Analysis archived in {report_file}[/dim]")

if __name__ == "__main__":
    for folder in ["logs", "reports"]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # create test log or control 
    if not os.path.exists("logs/test.log"):
        with open("logs/test.log", "w") as f: f.write("")

    event_handler = AdvancedLogHandler()
    observer = Observer()
    # just watch this file (have error) with this recursive thing
    observer.schedule(event_handler, path="logs/", recursive=False)
    
    console.print(Panel("[bold green]🚀 Advanced AI Log Analysis & Reporting Started[/bold green]\n[italic]Watching ALL .log files in logs/ directory...[/italic]"))
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        console.print("\n[bold red]Shutting down the system...[/bold red]")
    observer.join()