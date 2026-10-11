import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = MongoClient(os.getenv("MONGO_URI"), serverSelectionTimeoutMS=5000)
db = client["tutedude"]
submissions = db["submissions"]

@app.route("/", methods=["GET", "POST"])
def home():
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        if not name or not email:
            error = "Name and email are required."
        else:
            try:
                client.admin.command("ping")
                submissions.insert_one({"name": name, "email": email})
                return redirect(url_for("success"))
            except Exception:
                error = "Submission failed. Check MongoDB connection settings."

    return render_template("index.html", error=error)

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
