import os
import sys
import subprocess
import time
import shlex
import shutil
try:
    import readline
except ImportError:
    readline = None

class SauronCLI:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.backend_process = None
        self.frontend_process = None
        self.backend_status = "🔴 Offline"
        self.frontend_status = "🔴 Offline"
        self.is_service_mode = self.check_service(8000)
        
        if readline:
            readline.set_completer_delims(' \t\n;')
            readline.parse_and_bind("tab: complete")
            readline.set_completer(self.completer)

    def completer(self, text, state):
        buffer = readline.get_line_buffer()
        parts = shlex.split(buffer)
        if not parts or (len(parts) == 1 and not buffer.endswith(' ')):
            options = [cmd for cmd in ['ls', 'cd', 'pwd', 'run', 'clear', 'help', 'exit', 'status'] if cmd.startswith(text)]
        else:
            cmd = parts[0].lower()
            if cmd in ['cd', 'run', 'ls']:
                try:
                    items = os.listdir(self.current_dir)
                    options = []
                    for item in items:
                        if item.startswith(text):
                            path = os.path.join(self.current_dir, item)
                            if os.path.isdir(path):
                                options.append(item + '/')
                            elif cmd == 'run' and item.endswith('.py'):
                                options.append(item)
                            elif cmd == 'ls':
                                options.append(item)
                except Exception:
                    options = []
            else:
                options = []
        if state < len(options):
            return options[state]
        return None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def check_service(self, port):
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(('127.0.0.1', port)) == 0

    def start_services(self):
        if self.is_service_mode:
            self.backend_status = "🟢 Running (Background Service)"
            self.frontend_status = "🟢 Running (Background Service)"
            return True

        self.clear_screen()
        print("\033[1;95m👁️  SAURON SYSTEM INITIALIZATION\033[0m")
        print("=" * 60)

        # 1. Backend
        if self.check_service(8000):
            self.backend_status = "🟢 Running (External)"
        else:
            print("[\033[94mINFO\033[0m] Starting Backend (FastAPI)...")
            base_dir = os.path.dirname(os.path.abspath(__file__))
            backend_path = os.path.join(base_dir, 'backend', 'api.py')
            backend_log = open(os.path.join(base_dir, 'backend.log'), 'w')
            self.backend_process = subprocess.Popen(
                [sys.executable, "-u", backend_path],
                stdout=backend_log, stderr=backend_log, env=os.environ.copy(), cwd=base_dir
            )
            for _ in range(10):
                time.sleep(1)
                if self.check_service(8000):
                    self.backend_status = "🟢 Running"
                    break
            else:
                print("\033[91m❌ ERROR: Backend failed to start on port 8000.\033[0m")
                return False

        # 2. Interface (Development Mode)
        if self.check_service(5173):
            self.frontend_status = "🟢 Running (External)"
        else:
            # If backend is running and serving dist, we can skip dev interface
            if self.check_service(8000) and os.path.exists(os.path.join(os.path.dirname(__file__), 'interface', 'dist')):
                self.frontend_status = "🟢 Active (Served by Backend)"
            else:
                print("[\033[94mINFO\033[0m] Starting Interface (Vite Dev)...")
                interface_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'interface')
                interface_log = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'interface.log'), 'w')
                npm_cmd = shutil.which('npm')
                if not npm_cmd:
                    print("\033[91m❌ ERROR: 'npm' not found.\033[0m")
                    return False
                self.frontend_process = subprocess.Popen(
                    [npm_cmd, "run", "dev", "--", "--port", "5173", "--host", "127.0.0.1"],
                    cwd=interface_dir, stdout=interface_log, stderr=interface_log, env=os.environ.copy()
                )
                for _ in range(30):
                    time.sleep(1)
                    if self.check_service(5173):
                        self.frontend_status = "🟢 Running (Dev)"
                        break
                else:
                    print("\033[91m❌ ERROR: Interface failed to start on port 5173.\033[0m")
                    return False

        print("\n\033[92m✅ All systems operational.\033[0m")
        print("-" * 60)
        print(f"Backend:   {self.backend_status}")
        print(f"Interface: {self.frontend_status}")
        print("-" * 60)
        time.sleep(1)
        return True
def run_training(self, script_name):
    script_path = os.path.join(self.current_dir, script_name)
    if not os.path.exists(script_path):
        print(f"\033[91m❌ Error: File '{script_name}' not found.\033[0m")
        return
    print(f"\n\033[1;95m🚀 LAUNCHING BACKGROUND-READY TRAINING\033[0m: \033[94m{script_name}\033[0m")
    # Update path to find the 'sauron_monitor' package
    sdk_base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'sdk'))
    env = os.environ.copy()
    env["PYTHONPATH"] = sdk_base_path + os.pathsep + env.get("PYTHONPATH", "")
    try:
        process = subprocess.Popen([sys.executable, "-u", script_path], env=env, stdout=sys.stdout, stderr=sys.stderr)
        process.wait()
    except KeyboardInterrupt:
...
            print("\n\033[93m🛑 Training interrupted.\033[0m")
        except Exception as e:
            print(f"\n\033[91m❌ Execution error: {e}\033[0m")

    def shell(self):
        if not self.start_services():
            return
        self.clear_screen()
        print("\033[1;95m👁️  SAURON INTERACTIVE SHELL\033[0m")
        if self.is_service_mode:
            print("\033[90mConnected to Sauron Background Service\033[0m")
        print("Type 'help' for available commands or use Ctrl+C to quit.")
        print("-" * 60)
        while True:
            try:
                dir_name = os.path.basename(self.current_dir) or "/"
                prompt = f"\033[1;95mSAURON\033[0m [\033[94m{dir_name}\033[0m] > "
                raw_input = input(prompt).strip()
                if not raw_input: continue
                parts = shlex.split(raw_input)
                cmd = parts[0].lower()
                args = parts[1:]
                if cmd in ['q', 'exit', 'quit']: break
                elif cmd == 'help':
                    print("\n\033[1mSAURON COMMAND REFERENCE\033[0m")
                    print("  ls, cd, pwd, run <file.py>, status, clear, exit")
                elif cmd == 'ls':
                    try:
                        items = os.listdir(self.current_dir)
                        for item in sorted(items):
                            path = os.path.join(self.current_dir, item)
                            color = "\033[94m" if os.path.isdir(path) else "\033[92m" if item.endswith('.py') else ""
                            print(f"{color}{item}{'/' if os.path.isdir(path) else ''}\033[0m")
                    except Exception as e: print(f"Error: {e}")
                elif cmd == 'cd':
                    target = os.path.abspath(os.path.join(self.current_dir, args[0] if args else os.path.expanduser("~")))
                    if os.path.isdir(target): self.current_dir = target
                    else: print(f"cd: no such directory: {args[0]}")
                elif cmd == 'pwd': print(self.current_dir)
                elif cmd == 'run':
                    if not args: print("Usage: run <script.py>")
                    else: self.run_training(args[0])
                elif cmd == 'status':
                    print(f"\nBackend:   {self.backend_status}")
                    print(f"Interface: {self.frontend_status} -> http://127.0.0.1:8000")
                elif cmd == 'clear':
                    self.clear_screen()
                    print("\033[1;95m👁️  SAURON INTERACTIVE SHELL\033[0m")
                    print("-" * 60)
                else: print(f"Sauron: command not found: {cmd}")
            except (EOFError, KeyboardInterrupt):
                print("\n\033[93mExiting Sauron Shell...\033[0m")
                break

    def cleanup(self):
        if not self.is_service_mode:
            print("\n\033[90mCleaning up session services...\033[0m")
            if self.backend_process: self.backend_process.terminate()
            if self.frontend_process: self.frontend_process.terminate()
        print("\033[95mEye of Sauron closed.\033[0m")

if __name__ == "__main__":
    cli = SauronCLI()
    try: cli.shell()
    finally: cli.cleanup()
