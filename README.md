# Git Genius 🧠✨

A Git-like local repository management system powered by LLMs.  
This tool allows users to interact with a repo through natural language instructions such as:

> "Create a new branch called `feature/login` from `main`"

## Features
- Natural language to Git command translation using LLMs
- Local repo management (branches, commits, logs, etc.)
- Future plan: Backup to S3
- Command parser with testable architecture

## Project Structure
```
git-genius/
├── llm_interface/
├── repo_engine/
├── tests/
├── examples/
└── main.py
```

## How to Run
```bash
python main.py
```

## License
MIT
