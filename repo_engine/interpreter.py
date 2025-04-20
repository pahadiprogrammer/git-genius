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

    elif action == "status":
        current = repo_state["current_branch"]
        print(f"\n🔎 Repo Status:")
        print(f"🔀 Branch: {current}")
        print(f"📥 Staged files: {repo_state['staging_area'] or 'None'}")

        history = repo_state["branches"][current]
        if not history:
            print("📜 No commits yet.")
        else:
            print(f"✅ Last Commit: {history[-1]['message']}")
            print(f"   ↪ Files: {history[-1]['files']}")

    elif action == "merge_branch":
        source_branch = command.get("source")
        current = repo_state["current_branch"]

        if source_branch not in repo_state["branches"]:
            print(f"❌ Branch '{source_branch}' does not exist.")
            return repo_state

        source_commits = repo_state["branches"][source_branch]
        current_commits = repo_state["branches"][current]

        # Find commits in source not already in current
        to_merge = [c for c in source_commits if c not in current_commits]

        if not to_merge:
            print(f"⚖️ Branch '{source_branch}' is already merged into '{current}'")
            return repo_state

        # Detect conflicts from latest commit in each branch
        source_last = source_commits[-1]["files"] if source_commits else []
        current_last = current_commits[-1]["files"] if current_commits else []

        conflicts = list(set(source_last) & set(current_last))

        if conflicts:
            print(f"❌ Merge conflict detected on files: {conflicts}")
            print("🛠️ Please resolve conflicts manually before merging.")
            return repo_state

        # No conflict, proceed with merge
        repo_state["branches"][current].extend(to_merge)
        print(f"🔀 Merged {len(to_merge)} commits from '{source_branch}' into '{current}'")

        return repo_state
    
    elif action == "help":
        print("\n🧠 Available Natural Language Commands:")
        print("- create new branch <branch_name> from <existing_branch>")
        print("- switch to branch <branch_name>")
        print("- add file <filename> to staging")
        print("- commit changes with message \"<message>\"")
        print("- show commit history")
        print("- show status")
        print("- merge branch <branch_name> into current")
        print("- show all commands (this one!)")

    else:
        print("⚠️ Unknown action:", action)

    return repo_state
