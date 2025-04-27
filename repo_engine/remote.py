import json
import os

REMOTE_VCS_STATE_FILE = ".remote_vcs_state.json"

def load_remote_repo():
    if os.path.exists(REMOTE_VCS_STATE_FILE):
        with open(REMOTE_VCS_STATE_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "branches": {}
        }

def save_remote_repo(remote_repo):
    with open(REMOTE_VCS_STATE_FILE, "w") as f:
        json.dump(remote_repo, f, indent=4)

def init_remote_repo():
    if not os.path.exists(REMOTE_VCS_STATE_FILE):
        save_remote_repo({
            "branches": {}
        })
