from flask import Flask, jsonify, render_template
app = Flask(__name__)
@app.route("/api")
def api():
    data = [
        {"name": "Anuj", "course": "DevOps"},
        {"name": "Harsh", "course": "Flask And MongoDb"}
    ]
    return jsonify(data)
@app.route("/")
def home():
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)
