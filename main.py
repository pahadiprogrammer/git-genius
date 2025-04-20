from llm_interface.parser import parse_command
from repo_engine.interpreter import execute_command

if __name__ == '__main__':
    repo_state = {
        "branches": {
            "main": []
        },
        "current_branch": "main",
        "staging_area": {},  # ← was a list, now a dict
        "merge_conflicts": []
    }
    print("Welcome to Git Genius 🚀")
    while True:
        cmd = input("🗣️ Enter a command (or 'exit'): ")
        if cmd.strip().lower() == "exit":
            break

        parsed = parse_command(cmd)
        if parsed:
            repo_state = execute_command(parsed, repo_state)
        else:
            print("🤖 Couldn't understand command.")
