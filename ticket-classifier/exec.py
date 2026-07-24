import sys
import subprocess

def main():
    args = sys.argv[1:]
    # Log the received arguments to a debug file
    with open("c:\\Users\\Meyyarivu\\OneDrive\\Desktop\\AIML Intern\\ticket-classifier\\exec_debug.txt", "w", encoding="utf-8") as f:
        f.write(f"Argv: {args}\n")
    
    # We expect something like: ['-Command', 'echo "Hello"']
    # Let's find if '-Command' or '-c' is in the arguments.
    cmd_to_run = None
    for i, arg in enumerate(args):
        if arg.lower() in ('-command', '-c') and i + 1 < len(args):
            cmd_to_run = args[i + 1]
            break
    
    if cmd_to_run is None:
        # Fallback: join all args except known flags, or run the last arg
        cmd_to_run = " ".join(args)
        
    with open("c:\\Users\\Meyyarivu\\OneDrive\\Desktop\\AIML Intern\\ticket-classifier\\exec_debug.txt", "a", encoding="utf-8") as f:
        f.write(f"Command to run: {cmd_to_run}\n")
        
    try:
        # Run command via shell (cmd.exe on Windows)
        res = subprocess.run(cmd_to_run, shell=True, capture_output=True, text=True)
        # Write stdout and stderr back
        sys.stdout.write(res.stdout)
        sys.stderr.write(res.stderr)
        sys.exit(res.returncode)
    except Exception as e:
        sys.stderr.write(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
