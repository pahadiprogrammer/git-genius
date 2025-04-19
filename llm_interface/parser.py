import re
from typing import Dict, Optional

def parse_command(command: str) -> Optional[Dict]:
    command = command.lower().strip()

    # Pattern: Create a new branch from main called feature/login
    match = re.match(r"create a new branch from (\w+) called ([\w/-]+)", command)
    if match:
        return {
            "action": "create_branch",
            "from": match.group(1),
            "name": match.group(2)
        }

    # Pattern: Commit changes with message 'Initial commit'
    match = re.match(r"commit changes with message ['\"](.+)['\"]", command)
    if match:
        return {
            "action": "commit",
            "message": match.group(1)
        }
    
    # 3. Switch to branch dev
    match = re.match(r"switch to branch ([\w/-]+)", command)
    if match:
        return {
            "action": "switch_branch",
            "name": match.group(1)
        }
    
    # 4. Show commit history
    if "show commit history" in command:
        return {
            "action": "show_history"
        }
    
    # 5. Create a new repo named my-repo
    match = re.match(r"create a new repo named ([\w-]+)", command)
    if match:
        return {
            "action": "create_repo",
            "name": match.group(1)
        }

    # Extend here with more patterns later
    return None
