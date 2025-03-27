#!pip install flask flask-cors requests flask-ngrok

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_ngrok import run_with_ngrok  # Enables Flask to work in Google Colab
import requests
from ollama import chat
from ollama import ChatResponse
import re

app = Flask(__name__)
CORS(app)
#run_with_ngrok(app)  # Use ngrok to create a public URL

@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        # Placeholder: You can integrate PyTorch/TensorFlow model here
        response: ChatResponse = chat(model='deepseek-r1:1.5b', messages=[
            {'role' : 'system', 'content' : f"you are Medihelp. A chatbot created to help medical personnel edit and create medical reports for patients."},
    {
        'role': 'user',
        'content': data
    },
        ])
        response_text = response['message']['content']
        think_texts = re.findall(r"<think>(.*?)</think>", response_text, flags=re.DOTALL) #extracts deep_think
        think_texts = "\n\n".join(think_texts).strip() 
        clean_response = re.sub(r"<think>.*?</think>", '', response_text, flags = re.DOTALL).strip()
        prediction = {"message": clean_response, "input": data}

        return jsonify(prediction)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start the Flask server
if __name__ == "__main__":
    app.run()


### Need to run code above first to get link


'''fetch("https://xxxxx.ngrok.io/api/predict", {  #// Use the ngrok URL
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({ userInput: "Test data" }),
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error("Error:", error));'''





