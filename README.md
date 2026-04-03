# OpenCode Sandbox Killer

A web UI for viewing and deleting sandbox entries in the OpenCode SQLite database.

## What it does

- Lists all projects and their sandbox directories from the `opencode.db` database
- Delete individual sandbox entries (removes database entry AND deletes the directory from disk)
- Clear all sandboxes for a project at once
- Browse and select different database files

## Prerequisites

- Python 3.8+

## Installation

```bash
# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running

```bash
python app.py
```

Then open http://localhost:5000 in your browser.

## Usage

1. The tool loads `opencode.db` from the project directory by default
2. Use **Browse** to select a different database file, or paste the path manually
3. Click **Load** to switch databases
4. Each project shows its sandbox directories as tags
5. Click the red **x** on a sandbox to delete it (directory + database entry)
6. Click **Clear All** to delete every sandbox for a project

## Warning

Deleting a sandbox permanently removes the directory from disk. This cannot be undone.
