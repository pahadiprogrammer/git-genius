from llm_interface.parser import parse_command

if __name__ == '__main__':
    print("Welcome to Git Genius 🚀")
    while True:
        cmd = input("🗣️ Enter a command (or 'exit'): ")
        if cmd == "exit":
            break
        result = parse_command(cmd)
        print("🧠 Parsed:", result)
