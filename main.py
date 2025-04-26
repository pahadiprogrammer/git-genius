from llm_interface.parser import parse_command
from repo_engine.interpreter import execute_command
from repo_engine.interpreter import load_repo_state, save_repo_state

if __name__ == '__main__':
    repo_state = repo_state = load_repo_state()

    print("Welcome to Git Genius 🚀")
    while True:
        cmd = input("🗣️ Enter a command (or 'exit'): ")
        if cmd.strip().lower() == "exit":
            break

        parsed = parse_command(cmd)
        if parsed:
            repo_state = execute_command(parsed, repo_state)
            save_repo_state(repo_state)
        else:
            print("🤖 Couldn't understand command.")
