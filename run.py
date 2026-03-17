import os, sys, subprocess, time, webbrowser

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    backend, frontend, venv = [os.path.join(root, x) for x in ["backend", "frontend", ".venv"]]
    
    win = os.name == "nt"
    py = os.path.join(venv, "Scripts", "python.exe") if win else os.path.join(venv, "bin", "python")
    pip = os.path.join(venv, "Scripts", "pip.exe") if win else os.path.join(venv, "bin", "pip")
    npm = "npm.cmd" if win else "npm"

    print("Initializing AutoDocThinker...")
    
    if not os.path.exists(venv):
        subprocess.run([sys.executable, "-m", "venv", venv], check=True)
        
    subprocess.run([pip, "install", "-r", os.path.join(backend, "requirements.txt")], check=True)

    if not os.path.exists(os.path.join(frontend, "node_modules")):
        subprocess.run([npm, "install"], cwd=frontend, shell=True, check=True)

    print("Starting services...")
    
    env = {**os.environ, "PYTHONPATH": backend}
    be = subprocess.Popen([py, "run.py"], cwd=backend, env=env)
    fe = subprocess.Popen([npm, "run", "dev"], cwd=frontend, shell=True)

    url = "http://localhost:5173"
    print(f"\nRunning! UI: {url}\nPress Ctrl+C to stop.")
    
    time.sleep(2)
    webbrowser.open(url)

    try:
        while be.poll() is None and fe.poll() is None:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        for p in [be, fe]: p.terminate()
        print("Stopped.")

if __name__ == "__main__":
    main()
