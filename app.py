from flask import Flask, request, jsonify, render_template, redirect, url_for
import serpapi
import os
from dotenv import load_dotenv

app = Flask(__name__, template_folder="templates", static_folder="static")
load_dotenv()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/authenticate", methods=["POST"])
def authenticate():
    # Here you would implement login or registration logic
    # For now, let's assume the user is successfully authenticated
    # Redirect to the chatbot page
    return redirect(url_for('chatbot'))

@app.route("/search", methods=["POST"])
def search():
    query = request.json["query"]
    results = perform_search(query)
    return jsonify(results)

def perform_search(query):
    serpapi_key = os.getenv("serpapi_key")  # Replace with your actual SerpApi key
    params = {
        "q": query,
        "engine": "google",
        "api_key": serpapi_key,
        "google_domain": "google.com",
        "tbm": "shop",  # Restrict results to shopping
    }

    response = serpapi.search(params)
    results = []

    for result in response.get("shopping_results", []):
        product = result.get("title", "")
        price = result.get("price", "")
        url = result.get("link", "")
        results.append({"product": product, "price": price, "url": url})

    return results

@app.route("/chatbot", methods=["GET"])
def chatbot():
    return render_template("chatbot.html")

if __name__ == "__main__":
    app.run(debug=True)