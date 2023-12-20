import logging
import os

from flask import Flask, jsonify, request

from embedchain import Pipeline as App

app = Flask(__name__)

os.environ["OPENAI_API_KEY"] = "sk-xxx"


@app.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    data_type = data.get("data_type")
    url_or_text = data.get("url_or_text")
    if data_type and url_or_text:
        try:
            App().add(url_or_text, data_type=data_type)
            return jsonify({"data": f"Added {data_type}: {url_or_text}"}), 200
        except Exception:
            logging.exception(f"Failed to add {data_type=}: {url_or_text=}")
            return jsonify({"error": f"Failed to add {data_type}: {url_or_text}"}), 500
    return jsonify({"error": "Invalid request. Please provide 'data_type' and 'url_or_text' in JSON format."}), 400


@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    question = data.get("question")
    if question:
        try:
            response = App().query(question)
            return jsonify({"data": response}), 200
        except Exception:
            logging.exception(f"Failed to query {question=}")
            return jsonify({"error": "An error occurred. Please try again!"}), 500
    return jsonify({"error": "Invalid request. Please provide 'question' in JSON format."}), 400


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question")
    if question:
        try:
            response = App().chat(question)
            return jsonify({"data": response}), 200
        except Exception:
            logging.exception(f"Failed to chat {question=}")
            return jsonify({"error": "An error occurred. Please try again!"}), 500
    return jsonify({"error": "Invalid request. Please provide 'question' in JSON format."}), 400


@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"