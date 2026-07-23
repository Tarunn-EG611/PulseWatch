# PulseWatch — Linux Commands Reference

A running log of every Linux/bash command used while building PulseWatch, organized by phase, with a one-line explanation of what each does.

---

## WSL & System Setup

| Command | What it does |
|---|---|
| `wsl --install -d Ubuntu` | Installs WSL2 with Ubuntu (run in Windows PowerShell) |
| `sudo apt update` | Refreshes the list of available packages from repositories |
| `sudo apt install python3 python3-venv python3-pip git -y` | Installs Python, venv module, pip, and Git |
| `python3 --version` | Shows installed Python version |
| `pip3 --version` | Shows installed pip version |
| `git --version` | Shows installed Git version |
| `which -a code` | Lists all locations where the `code` command exists |
| `hash -r` | Clears the shell's cached command locations |

## Navigation & Folders

| Command | What it does |
|---|---|
| `mkdir ~/PulseWatch && cd ~/PulseWatch` | Creates the project folder and moves into it |
| `pwd` | Prints your current directory path |
| `cd PulseWatch` / `cd ~/PulseWatch` | Moves into the PulseWatch folder |
| `ls` | Lists files/folders in the current directory |
| `ls -la` | Lists all files/folders, including hidden ones, with details |
| `ls -R` | Lists files/folders recursively (all subfolders too) |
| `mkdir -p src/log_reader src/monitor ...` | Creates multiple nested folders at once |
| `touch file.txt` | Creates an empty file instantly |

## VS Code

| Command | What it does |
|---|---|
| `code .` | Opens the current folder in VS Code (connected to WSL) |

## Virtual Environment

| Command | What it does |
|---|---|
| `sudo apt install python3.14-venv` | Installs the venv module for your specific Python version |
| `python3 -m venv .venv` | Creates a virtual environment folder named `.venv` |
| `source .venv/bin/activate` | Activates the virtual environment for the current terminal |

## Editing Files

| Command | What it does |
|---|---|
| `nano filename` | Opens a file in the nano text editor (creates it if it doesn't exist) |
| `cat filename` | Prints a file's full contents to the terminal |
| `cat filename \| grep alias` | Prints only lines containing "alias" from a file |

## Bash Config

| Command | What it does |
|---|---|
| `alias code="path"` | Creates a shortcut so `code` always points to a specific program |
| `source ~/.bashrc` | Reloads your shell config so new aliases/settings take effect |
| `alias code` | Shows what the `code` alias currently points to |

## Python Packages

| Command | What it does |
|---|---|
| `pip install package_name` | Installs a Python package into the active environment |
| `pip freeze > requirements.txt` | Saves a list of installed packages + versions into a file |

## Git & GitHub

| Command | What it does |
|---|---|
| `git init` | Turns the current folder into a Git repository |
| `git config --global user.name "Name"` | Sets your Git identity (name) for all repos |
| `git config --global user.email "email"` | Sets your Git identity (email) for all repos |
| `git status` | Shows what's staged, changed, or untracked |
| `git add .` | Stages all changed/new files for commit |
| `git commit -m "message"` | Saves a snapshot of staged changes with a description |
| `git branch -M main` | Renames the current branch to `main` |
| `git remote add origin URL` | Links your local repo to a GitHub repository |
| `git remote -v` | Shows the URLs your repo is connected to |
| `git push -u origin main` | Uploads commits to GitHub and links local/remote branches |
| `git push` | Uploads new commits (after the initial `-u` push) |
| `git log` | Shows commit history |
| `git config --global credential.helper store` | Saves login credentials so you're not prompted every push |

## Syslog Permissions & Exploration

| Command | What it does |
|---|---|
| `ls -la /var/log/syslog` | Checks the syslog file's permissions and ownership |
| `groups` | Lists which groups your user belongs to |
| `sudo usermod -aG adm $USER` | Adds your user to the `adm` group (grants syslog read access) |
| `tail -20 /var/log/syslog` | Shows the last 20 lines of the syslog file |
| `tail -f /var/log/syslog` | Streams new syslog lines live as they're written |

## Testing / Triggering Activity

| Command | What it does |
|---|---|
| `sudo apt update` | Triggers real package-related system activity/logs |
| `logger -p user.warning "message"` | Manually writes a test line directly into syslog |

## Running PulseWatch Scripts

| Command | What it does |
|---|---|
| `python3 src/log_reader/syslog_reader.py` | Runs the real-time syslog reader/parser |
| `python3 src/monitor/system_monitor.py` | Runs the CPU/RAM/disk monitor |
| `python3 src/monitor/service_checker.py` | Runs the service up/down health checker |
