import os
import subprocess
from maya import cmds


MODULE_NAME = 'takRenamer'
MODULE_PATH = __file__.split(MODULE_NAME, 1)[0] + MODULE_NAME
CREATE_NO_WINDOW = 0x08000000


def checkVersion():
    if isOutdated(MODULE_PATH):
        result = cmds.confirmDialog(
            title=MODULE_NAME,
            message="New version is detected. Do you want to update?",
            button=['Yes','No'],
            defaultButton='Yes',
            cancelButton='No',
            dismissString='No'
        )

        if 'Yes' == result:
            update()
    else:
        cmds.confirmDialog(title=MODULE_NAME, message='You have latest version.\nEnjoy!')


def isOutdated(repo_path):
    # Navigate to the specific repository
    os.chdir(repo_path)

    try:
        # Fetch the latest commits from the remote repository
        subprocess.run(["git", "fetch"], check=True, creationflags=CREATE_NO_WINDOW)

        # Get the local and remote HEAD commit hashes
        local_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], creationflags=CREATE_NO_WINDOW).strip()
        remote_commit = subprocess.check_output(["git", "rev-parse", "@{u}"], creationflags=CREATE_NO_WINDOW).strip()

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
        subprocess.run(["git", "pull"], check=True, creationflags=CREATE_NO_WINDOW)
        print("Update is done successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to update: {}".format(e))
