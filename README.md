# OpenCode Sandbox Killer

A Flask web UI for viewing and deleting sandbox entries in the OpenCode SQLite database.

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

# Install Flask
pip install flask
```

## Running

```bash
python app.py
```

Then open http://localhost:5000 in your browser.

## Usage

1. Open http://localhost:5000 in your browser
2. Click **Browse** to navigate to your `opencode.db` file, or paste the full path into the text box
3. Click **Load** (the button is disabled until a path is entered)
4. Each project shows its sandbox directories as a vertical list
5. Click the red **x** on a sandbox to delete it (directory + database entry)
6. Click **Clear All** to delete every sandbox for a project

## Warning

Deleting a sandbox permanently removes the directory from disk. This cannot be undone.
