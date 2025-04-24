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
        files = repo_state["staging_area"].copy()  # snapshot
        commit_data = {
            "message": message,
            "files": files
        }
        repo_state["branches"][current].append(commit_data)
        repo_state["staging_area"].clear()  # clear staging after commit
        print(f"✅ Committed: '{message}' with files: {files}")

    elif action == "switch_branch":
        target = command.get("name")
        if target in repo_state["branches"]:
            repo_state["current_branch"] = target
            print(f"🔁 Switched to branch: {target}")
        else:
            print(f"❌ Branch '{target}' does not exist.")

    elif action == "show_history":
        commits = repo_state["branches"][repo_state["current_branch"]]
        for i, commit in enumerate(commits, 1):
            print(f"🔖 Commit {i}: {commit['message']}")
            for fname, content in commit['files'].items():
                print(f"   📄 {fname}: {content[:30]}{'...' if len(content) > 30 else ''}")

    elif action == "create_repo":
        repo_name = command.get("name")
        print(f"📁 New repo '{repo_name}' initialized (simulated).")

    elif action == "stage_file":
        filename = command.get("file")
        content = input(f"📝 Enter content for {filename}: ")
        repo_state["staging_area"][filename] = content
        current = repo_state["current_branch"]
        
        # The file exists in working directory before we even add it to staging area
        repo_state["working_directory"].setdefault(current, {})[filename] = content
        
        print(f"📄 Staged file: {filename}")
        return repo_state

    elif action == "status":
        current = repo_state["current_branch"]
        print(f"\n🔎 Repo Status:")
        print(f"🔀 Branch: {current}")
        print(f"📥 Staged files: {repo_state['staging_area'].keys() or 'None'}")

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
    
    elif action == "view_files":
        current = repo_state["current_branch"]
        files = repo_state["working_directory"].get(current, {})
        if not files:
            print("📂 No files in working directory.")
        else:
            print(f"\n📁 Files in branch '{current}':")
            for fname, content in files.items():
                print(f"📄 {fname}: {content[:50]}{'...' if len(content) > 50 else ''}")

    elif action == "edit_file":
        filename = command.get("file")
        current = repo_state["current_branch"]
        files = repo_state["working_directory"].get(current, {})

        if filename not in files:
            print(f"❌ File '{filename}' does not exist in working directory.")
        else:
            print(f"📄 Current content of {filename}:")
            print(files[filename])
            new_content = input("📝 Enter new content: ")
            files[filename] = new_content
            repo_state["staging_area"][filename] = new_content
            print(f"✅ Updated and staged file: {filename}")

    elif action == "delete_file":
        filename = command.get("file")
        current = repo_state["current_branch"]
        files = repo_state["working_directory"].get(current, {})

        if filename not in files:
            print(f"❌ File '{filename}' not found in working directory.")
        else:
            del files[filename]
            repo_state["staging_area"][filename] = "[DELETED]"
            print(f"🗑️ Deleted '{filename}' and marked for deletion in next commit.")

    elif action == "view_file":
        filename = command.get("file")
        current = repo_state["current_branch"]
        files = repo_state["working_directory"].get(current, {})

        if filename in files:
            print(f"\n📖 Contents of '{filename}':\n")
            print(files[filename])
        else:
            print(f"❌ File '{filename}' not found in working directory.")

    elif action == "tag_commit":
        tag_name = command.get("tag")
        current = repo_state["current_branch"]
        commits = repo_state["branches"][current]

        if not commits:
            print("❌ Cannot tag: No commits on current branch.")
        else:
            # Tag the latest commit
            repo_state.setdefault("tags", {})[tag_name] = {
                "branch": current,
                "commit_index": len(commits) - 1
            }
            print(f"🏷️ Tagged latest commit as '{tag_name}'")

    elif action == "list_tags":
        tags = repo_state.get("tags", {})
        if not tags:
            print("🔖 No tags created yet.")
        else:
            print("🏷️ Tags:")
            for tag, data in tags.items():
                print(f"🔸 {tag} → Branch: {data['branch']}, Commit #{data['commit_index'] + 1}")

    elif action == "checkout_tag":
        tag = command.get("tag")
        tags = repo_state.get("tags", {})

        if tag not in tags:
            print(f"❌ Tag '{tag}' not found.")
        else:
            tag_data = tags[tag]
            branch = tag_data["branch"]
            commit_idx = tag_data["commit_index"]

            commit = repo_state["branches"][branch][commit_idx]
            print(f"\n📦 Checked out tag '{tag}' → Commit {commit_idx + 1} on branch '{branch}'")
            print(f"📜 Message: {commit['message']}")
            print("📄 Files:")
            for fname, content in commit["files"].items():
                print(f"   📄 {fname}: {content[:30]}{'...' if len(content) > 30 else ''}")

    elif action == "current_branch":
        current_branch = repo_state["current_branch"]
        print(f"🔍 Current branch: {current_branch}")

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
