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
        
        # Configure readline if available
        if readline:
            readline.set_completer_delims(' \t\n;')
            readline.parse_and_bind("tab: complete")
            readline.set_completer(self.completer)

    def completer(self, text, state):
        buffer = readline.get_line_buffer()
        parts = shlex.split(buffer)
        
        # Determine if we are completing a command or an argument
        if not parts or (len(parts) == 1 and not buffer.endswith(' ')):
            # Complete commands
            options = [cmd for cmd in ['ls', 'cd', 'pwd', 'run', 'clear', 'help', 'exit', 'status'] if cmd.startswith(text)]
        else:
            # Complete files/directories for commands that take them
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
        else:
            return None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def check_service(self, port):
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            return s.connect_ex(('127.0.0.1', port)) == 0

    def start_services(self):
        self.clear_screen()
        print("\033[1;95m👁️  SAURON SYSTEM INITIALIZATION\033[0m")
        print("=" * 60)

        # 1. Backend check/start
        if self.check_service(8000):
            self.backend_status = "🟢 Running (External)"
        else:
            print("[\033[94mINFO\033[0m] Starting Backend (FastAPI)...")
            # Use absolute path to avoid any ambiguity after the rename
            base_dir = os.path.dirname(os.path.abspath(__file__))
            backend_path = os.path.join(base_dir, 'backend', 'api.py')
            
            # Use unbuffered output and log everything
            backend_log = open(os.path.join(base_dir, 'backend.log'), 'w')
            
            # Force 127.0.0.1 in the startup env
            env = os.environ.copy()
            
            self.backend_process = subprocess.Popen(
                [sys.executable, "-u", backend_path],
                stdout=backend_log,
                stderr=backend_log,
                env=env,
                cwd=base_dir
            )
            
            # Increased wait time and more frequent checks
            print("Waiting for backend to be ready...")
            for i in range(15):
                time.sleep(1)
                if self.check_service(8000):
                    self.backend_status = "🟢 Running"
                    break
            else:
                print(f"\033[91m❌ ERROR: Backend failed to start on port 8000.\033[0m")
                print(f"Path searched: {backend_path}")
                print("Check 'backend.log' for details.")
                return False

        # 2. Frontend check/start
        if self.check_service(5173):
            self.frontend_status = "🟢 Running (External)"
        else:
            print("[\033[94mINFO\033[0m] Starting Interface (Vite)...")
            interface_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'interface')
            
            interface_log = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'interface.log'), 'w')
            
            npm_cmd = shutil.which('npm')
            if not npm_cmd:
                print("\033[91m❌ ERROR: 'npm' command not found.\033[0m")
                return False

            self.frontend_process = subprocess.Popen(
                [npm_cmd, "run", "dev", "--", "--port", "5173", "--host", "127.0.0.1"],
                cwd=interface_dir,
                stdout=interface_log,
                stderr=interface_log,
                env=os.environ.copy()
            )
            
            print("Waiting for interface to be ready (up to 30s)...")
            for _ in range(30):
                time.sleep(1)
                if self.check_service(5173):
                    self.frontend_status = "🟢 Running"
                    break
            else:
                print("\033[91m❌ ERROR: Interface failed to start on port 5173.\033[0m")
                print("Check 'interface.log' for details.")
                return False

        print("\n\033[92m✅ All systems operational.\033[0m")
        print("-" * 60)
        print(f"Backend:   {self.backend_status}")
        print(f"Interface: {self.frontend_status} -> http://127.0.0.1:5173")
        print("-" * 60)
        time.sleep(1)
        return True

    def run_training(self, script_name):
        script_path = os.path.join(self.current_dir, script_name)
        if not os.path.exists(script_path):
            print(f"\033[91m❌ Error: File '{script_name}' not found in current directory.\033[0m")
            return
        
        print(f"\n\033[1;95m🚀 LAUNCHING TRAINING\033[0m: \033[94m{script_name}\033[0m")
        print("\033[90m" + "=" * 60 + "\033[0m")
        
        sdk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'sdk'))
        env = os.environ.copy()
        env["PYTHONPATH"] = sdk_path + os.pathsep + env.get("PYTHONPATH", "")
        
        try:
            process = subprocess.Popen(
                [sys.executable, "-u", script_path],
                env=env,
                stdout=sys.stdout,
                stderr=sys.stderr
            )
            process.wait()
            if process.returncode == 0:
                print(f"\n\033[92m✅ Training completed successfully.\033[0m")
            else:
                print(f"\n\033[91m❌ Training exited with error code {process.returncode}.\033[0m")
        except KeyboardInterrupt:
            print("\n\033[93m🛑 Training interrupted by user (SIGINT).\033[0m")
        except Exception as e:
            print(f"\n\033[91m❌ Execution error: {e}\033[0m")
        
        print("\033[90m" + "=" * 60 + "\033[0m")

    def shell(self):
        if not self.start_services():
            return

        self.clear_screen()
        print("\033[1;95m👁️  SAURON INTERACTIVE SHELL\033[0m")
        print("Type 'help' for available commands or use Ctrl+C to quit.")
        print("-" * 60)

        while True:
            try:
                dir_name = os.path.basename(self.current_dir) or "/"
                prompt = f"\033[1;95mSAURON\033[0m [\033[94m{dir_name}\033[0m] > "
                
                raw_input = input(prompt).strip()
                if not raw_input:
                    continue
                
                try:
                    parts = shlex.split(raw_input)
                except ValueError as e:
                    print(f"Parse error: {e}")
                    continue

                cmd = parts[0].lower()
                args = parts[1:]

                if cmd in ['q', 'exit', 'quit']:
                    break
                
                elif cmd == 'help':
                    print("\n\033[1mSAURON COMMAND REFERENCE\033[0m")
                    print("  \033[94mls\033[0m              List files in current directory")
                    print("  \033[94mcd <dir>\033[0m       Change to directory")
                    print("  \033[94mpwd\033[0m             Show current path")
                    print("  \033[94mrun <file.py>\033[0m   Execute a training script")
                    print("  \033[94mstatus\033[0m          Check service health")
                    print("  \033[94mclear\033[0m           Clear terminal")
                    print("  \033[94mexit\033[0m            Shutdown and quit")
                    print("\n\033[90mTip: Use TAB for auto-completion of commands and files.\033[0m")

                elif cmd == 'ls':
                    try:
                        target_dir = os.path.abspath(os.path.join(self.current_dir, args[0] if args else "."))
                        items = os.listdir(target_dir)
                        for item in sorted(items):
                            path = os.path.join(target_dir, item)
                            if os.path.isdir(path):
                                print(f"\033[1;94m{item}/\033[0m")
                            elif item.endswith('.py'):
                                print(f"\033[92m{item}\033[0m")
                            else:
                                print(item)
                    except Exception as e:
                        print(f"Error listing files: {e}")

                elif cmd == 'cd':
                    target = os.path.abspath(os.path.join(self.current_dir, args[0] if args else os.path.expanduser("~")))
                    if os.path.isdir(target):
                        self.current_dir = target
                    else:
                        print(f"cd: no such directory: {args[0]}")

                elif cmd == 'pwd':
                    print(self.current_dir)

                elif cmd == 'run':
                    if not args:
                        print("Usage: run <script.py>")
                    else:
                        self.run_training(args[0])

                elif cmd == 'status':
                    print(f"\nBackend:   {self.backend_status}")
                    print(f"Interface: {self.frontend_status} -> http://127.0.0.1:5173")

                elif cmd == 'clear':
                    self.clear_screen()
                    print("\033[1;95m👁️  SAURON INTERACTIVE SHELL\033[0m")
                    print("-" * 60)

                else:
                    print(f"Sauron: command not found: {cmd}. Type 'help' for assistance.")

            except EOFError:
                break
            except KeyboardInterrupt:
                print("\n\033[93mExiting Sauron...\033[0m")
                break

    def cleanup(self):
        print("\n\033[90mCleaning up services...\033[0m")
        if self.backend_process:
            self.backend_process.terminate()
        if self.frontend_process:
            self.frontend_process.terminate()
        print("\033[95mEye of Sauron closed.\033[0m")

if __name__ == "__main__":
    cli = SauronCLI()
    try:
        cli.shell()
    finally:
        cli.cleanup()
