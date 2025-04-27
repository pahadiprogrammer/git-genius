import re
from typing import Dict, Optional

def parse_command(command: str) -> Optional[Dict]:
    command = command.lower().strip()

    # Pattern: Create a new branch from main called feature/login
    match = re.match(r"create new branch ([\w/-]+) from (\w+)", command)
    if match:
        return {
            "action": "create_branch",
            "from": match.group(2),
            "name": match.group(1)
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
    
    # 5. Create a new repo named <my-repo>
    match = re.match(r"create a new repo named ([\w-]+)", command)
    if match:
        return {
            "action": "create_repo",
            "name": match.group(1)
        }
    
    # 6. Add file to staging
    match = re.match(r"add file ([\w.\-_/]+) to staging", command)
    if match:
        return {
            "action": "stage_file",
            "file": match.group(1)
        }
    
    # 7. Merge branch <feature/login> into current
    match = re.match(r"merge branch ([\w/\-]+) into current", command)
    if match:
        return {
            "action": "merge_branch",
            "source": match.group(1)
        }
    
    # 8. Show status
    if command.strip().lower() == "show status":
        return {
            "action": "status"
        }
    
    # 9. Show all commands
    if command.strip().lower() == "show all commands":
        return {
            "action": "help"
        }
    
    # 10. View current branch files
    if command.strip() == "view files":
        return {
            "action": "view_files"
        }
    
    # 11. Edit file
    match = re.match(r"edit file ([\w.\-_/]+)", command)
    if match:
        return {
            "action": "edit_file",
            "file": match.group(1)
        }

    # 12. Delete file
    match = re.match(r"delete file ([\w.\-_/]+)", command)
    if match:
        return {
            "action": "delete_file",
            "file": match.group(1)
        }

    # 13. View file
    match = re.match(r"view file ([\w.\-_/]+)", command)
    if match:
        return {
            "action": "view_file",
            "file": match.group(1)
        }
    
    # 14. Tag commit as v1.0
    match = re.match(r"tag commit as ([\w.\-]+)", command)
    if match:
        return {
            "action": "tag_commit",
            "tag": match.group(1)
        }

    # 15. List all tags
    if command.strip() == "list all tags":
        return {
            "action": "list_tags"
        }

    # 16. Checkout tag <v1.0>
    match = re.match(r"checkout tag ([\w.\-]+)", command)
    if match:
        return {
            "action": "checkout_tag",
            "tag": match.group(1)
        }
    
    # 17. Show current branch
    match = re.match(r"show current branch", command)
    if match:
        return {
            "action": "current_branch"
        }
    
    # 18. Show activity log
    if command.strip() == "show activity log":
        return {
            "action": "show_log"
        }
    
    # 19. Push branch <branch-name> to remote
    match = re.match(r"push branch ([\w/-]+) to remote", command)
    if match:
        return {
            "action": "push_to_remote",
            "branch": match.group(1)
        }

    # Extend here with more patterns later
    return None
