from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
import json
import os
import shutil

app = Flask(__name__)
app.secret_key = os.urandom(24)


def get_db_path():
    return session.get("db_path")


def get_db():
    db_path = get_db_path()
    if not db_path or not os.path.exists(db_path):
        return None
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    db_path = get_db_path()
    db_selected = db_path is not None
    db_exists = db_selected and os.path.exists(db_path)

    projects_data = []
    if db_exists:
        conn = get_db()
        if conn:
            try:
                projects = conn.execute("SELECT * FROM project").fetchall()
                for project in projects:
                    sandboxes = json.loads(project["sandboxes"]) if project["sandboxes"] else []
                    projects_data.append({
                        "id": project["id"],
                        "name": project["name"] or project["id"],
                        "worktree": project["worktree"],
                        "sandboxes": sandboxes,
                    })
            except Exception:
                pass
            finally:
                conn.close()

    return render_template("index.html", projects=projects_data, db_path=db_path or "", db_selected=db_selected, db_exists=db_exists)


@app.route("/set_db", methods=["POST"])
def set_db():
    db_path = request.form.get("db_path", "").strip()
    if db_path:
        session["db_path"] = db_path
    return redirect(url_for("index"))


@app.route("/browse", methods=["GET"])
def browse():
    path = request.args.get("path", "")
    if not path or not os.path.exists(path):
        path = os.path.expanduser("~")

    entries = []
    try:
        for entry in sorted(os.listdir(path), key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower())):
            full_path = os.path.join(path, entry)
            entries.append({
                "name": entry,
                "path": full_path,
                "is_dir": os.path.isdir(full_path),
                "is_db": entry.endswith((".db", ".sqlite", ".sqlite3")),
            })
    except PermissionError:
        pass

    return jsonify({
        "current_path": path,
        "parent_path": os.path.dirname(path) if path != os.path.dirname(path) else None,
        "entries": entries,
    })


@app.route("/delete_sandbox", methods=["POST"])
def delete_sandbox():
    project_id = request.form.get("project_id")
    sandbox_value = request.form.get("sandbox")

    if not project_id or sandbox_value is None:
        return "Missing required fields", 400

    conn = get_db()
    project = conn.execute("SELECT sandboxes FROM project WHERE id = ?", (project_id,)).fetchone()

    if not project:
        conn.close()
        return "Project not found", 404

    sandboxes = json.loads(project["sandboxes"]) if project["sandboxes"] else []

    sandbox_path = None
    try:
        sandbox_index = int(sandbox_value)
        if 0 <= sandbox_index < len(sandboxes):
            sandbox_path = sandboxes.pop(sandbox_index)
    except ValueError:
        if sandbox_value in sandboxes:
            sandbox_path = sandbox_value
            sandboxes.remove(sandbox_value)

    conn.execute(
        "UPDATE project SET sandboxes = ? WHERE id = ?",
        (json.dumps(sandboxes), project_id)
    )
    conn.commit()
    conn.close()

    if sandbox_path and os.path.exists(sandbox_path):
        shutil.rmtree(sandbox_path)

    return redirect(url_for("index"))


@app.route("/clear_sandboxes/<project_id>", methods=["POST"])
def clear_sandboxes(project_id):
    conn = get_db()
    project = conn.execute("SELECT sandboxes FROM project WHERE id = ?", (project_id,)).fetchone()

    if project:
        sandboxes = json.loads(project["sandboxes"]) if project["sandboxes"] else []
        for sandbox_path in sandboxes:
            if os.path.exists(sandbox_path):
                shutil.rmtree(sandbox_path)

    conn.execute(
        "UPDATE project SET sandboxes = ? WHERE id = ?",
        (json.dumps([]), project_id)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
