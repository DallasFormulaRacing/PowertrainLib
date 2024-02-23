# Git Reference Sheet
Quick 15 minute [tutorial](https://www.youtube.com/watch?v=USjZcfj8yxE&pp=ygUMaW50cm8gdG8gZ2l0):
[![tutorial](https://img.youtube.com/vi/USjZcfj8yxE/0.jpg)](https://www.youtube.com/watch?v=USjZcfj8yxE&pp=ygUMaW50cm8gdG8gZ2l0)

> **Generally a quick google search will answer any other questions you may have about git.**

## Setup
1. Install git
- Clone the repository (`git clone REPOSITORY_LINK`)

## Managing/Switching branches
- `git branch` - Check what branches are available
- `git checkout BRANCH_NAME` - Switch to branch

## Updating your local repository (your computer)
- `git fetch` - Updates remotes, generally safe to run with uncommitted work
- `git pull` - Updates everything

## Updating the remote repository (the repository on the github, requires write access)
- `git add FILE_NAME` - Adds a file to track changes (use `git add .` to track all files in the current directory) 
- `git status` - Shows  which files are being tracked
- `git commit` - Creates a "checkpoint" in the timeline
- `git push` - Pushes your changes (commits) to the remote repository
