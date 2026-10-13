import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = MongoClient(
    os.getenv("MONGO_URI"),
    serverSelectionTimeoutMS=5000
)
db = client["tutedude"]
submissions = db["submissions"]
todo_items = db["todo_items"]


@app.route("/", methods=["GET", "POST"])
def home():
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        if not name or not email:
            error = "name email are required."
        else:
            try:
                client.admin.command("ping")
                submissions.insert_one({
                    "name": name,
                    "email": email
                })
                return redirect(url_for("successs"))
            except Exception:
                app.logger.exception("Submission failed")
                error = "Check MongoDB connection settings."

    return render_template("index.html", error=error)


@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/todo")
def todo():
    return render_template("todo.html")

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "JSON request body is required."
        }), 400

    item_name = data.get("itemName")
    item_description = data.get("itemDescription")

    if not isinstance(item_name, str) or not item_name.strip():
        return jsonify({"error": "itemName is required."}), 400

    if not isinstance(item_description, str) or not item_description.strip():
        return jsonify({"error": "itemDescription is required."}), 400

    try:
        client.admin.command("ping")
        result = todo_items.insert_one({
            "itemName": item_name.strip(),
            "itemDescription": item_description.strip()
        })

        return jsonify({
            "message": "item saved successfully.",
            "id": str(result.inserted_id)
        }), 201

    except Exception:
        app.logger.exception("submission failed")
        return jsonify({
            "error": "Could not save item. Check MongoDB settings."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
