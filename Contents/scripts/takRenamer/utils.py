import os
import subprocess
from maya import cmds


MODULE_NAME = 'takRenamer'
MODULE_PATH = __file__.split(MODULE_NAME, 1)[0] + MODULE_NAME
NO_WINDOW = 0x08000000


def isOutdated():
    # Navigate to the specific repository
    os.chdir(MODULE_PATH)

    try:
        # Fetch the latest commits from the remote repository
        subprocess.call(["git", "fetch"], creationflags=NO_WINDOW)

        # Get the local and remote HEAD commit hashes
        local_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], creationflags=NO_WINDOW).strip()
        remote_commit = subprocess.check_output(["git", "rev-parse", "@{u}"], creationflags=NO_WINDOW).strip()

        # Compare the local and remote commits
        if local_commit != remote_commit:
            return True  # Local repo is outdated

    except subprocess.CalledProcessError as e:
        print("Error: {}".format(e))
        return False

    return False  # Local repo is up-to-date


def update():
    try:
        # Pull the latest changes from the remote repository
        subprocess.call(["git", "pull"], creationflags=NO_WINDOW)
        print("Update is done successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print("Failed to update: {}".format(e))
        return False
