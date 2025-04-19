def execute_command(command: dict, repo_state: dict):
    action = command.get("action")

    if action == "create_branch":
        from_branch = command.get("from")
        new_branch = command.get("name")
        if from_branch in repo_state["branches"]:
            repo_state["branches"][new_branch] = list(repo_state["branches"][from_branch])
            repo_state["current_branch"] = new_branch
            print(f"✅ Created branch '{new_branch}' from '{from_branch}'")
        else:
            print(f"❌ Branch '{from_branch}' does not exist.")

    elif action == "commit":
        message = command.get("message")
        current = repo_state["current_branch"]
        files = list(repo_state["staging_area"])  # snapshot
        commit_data = {
            "message": message,
            "files": files
        }
        repo_state["branches"][current].append(commit_data)
        repo_state["staging_area"] = []  # clear staging after commit
        print(f"✅ Committed: '{message}' with files: {files}")

    elif action == "switch_branch":
        target = command.get("name")
        if target in repo_state["branches"]:
            repo_state["current_branch"] = target
            print(f"🔁 Switched to branch: {target}")
        else:
            print(f"❌ Branch '{target}' does not exist.")

    elif action == "show_history":
        current = repo_state["current_branch"]
        print(f"📜 Commit history for '{current}':")
        for i, commit in enumerate(repo_state["branches"][current]):
            print(f"  {i+1}. {commit['message']} | Files: {commit['files']}")

    elif action == "create_repo":
        repo_name = command.get("name")
        print(f"📁 New repo '{repo_name}' initialized (simulated).")

    elif action == "stage_file":
        file = command.get("file")
        if file not in repo_state["staging_area"]:
            repo_state["staging_area"].append(file)
            print(f"📥 Staged file: {file}")
        else:
            print(f"⚠️ File already staged: {file}")


    else:
        print("⚠️ Unknown action:", action)

    return repo_state
