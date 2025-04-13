#!pip install flask flask-cors requests flask-ngrok

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_ngrok import run_with_ngrok  # Enables Flask to work in Google Colab
import requests
from ollama import chat
from ollama import ChatResponse
import re
import sys
import logging
import pandas as pd

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
CORS(app)
#run_with_ngrok(app)  # Use ngrok to create a public URL

@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        print(data[1])
        patientDB = pd.read_csv('Patient Summary.csv')
        patientDB["Patient ID"] = patientDB.index
        patient_id = data[1]
        patient_name = patientDB.loc[patientDB['Patient ID'] == int(patient_id), 'Name'].values[0]
        patient_age = patientDB.loc[patientDB['Patient ID'] == int(patient_id), 'Age'].values[0]
        patient_summary = patientDB.loc[patientDB['Patient ID'] == int(patient_id), 'Patient Progress Summary'].values[0]
         #deep_think allows for background thinking to be visible
        #system_prompt helps LLM better fit use case
        response: ChatResponse = chat(model = "deepseek-r1:1.5b", messages =[
            {'role' : 'system', 'content' : "You are an assistant to medical professionals to help turn patient notes into medical reports. This is the only task you can perform. The first thing you must do is determine if the input from the user is medical notes. If they are not medical notes then the best response is to say 'I do not understand. Please only enter medical notes. See the help page if you need help.' If you determined that they are not medical notes there is no need to think any further about your reponse. If and only if you determined that the text is medical notes, resepond with a medical report. All of the reports should follow the SOAP notes outline. The first heading in the medical report should be Subjective, which includes the subheadings cheif complaint, history of present illness, patient history, review of systems, and current medications/allergies. The second heading is Objective, which includes objective data found during the paitent visit like vital signs, findings during physical exams, lab/diagnostic data, and imaging results. The third heading is Assessment, which includes the subheadings Problem, listing diagnosis from most important to least important, and Differential Diagnosis, which lsits the possible diagnosis based on likelihood and includes the reason that the patient is believed to have the diagnosis. The fourth heading is Plan, which includes any notes of further treatment or actions that need to be taken. Please only use the information provided for the medical report. Please only include the medical report in your response."}, #refers to system_prompt above
            {'role' : 'user', 'content' : f"Use the following as context for the user's query:\n patient name: {patient_name}\n patient age: {patient_age}\n patient medical issue summary: {patient_summary}\n user query:{data[0]}"} #user input (input_content) instead of just hard code "why is the sky blue"
        ])
        response_text = response['message']['content']
        think_texts = re.findall(r"<think>(.*?)</think>", response_text, flags=re.DOTALL) #extracts deep_think
        think_texts = "\n\n".join(think_texts).strip() 
        clean_response = re.sub(r"<think>.*?</think>", '', response_text, flags = re.DOTALL).strip() #just finding response without think text
        patientDB.loc[patientDB['Patient ID'] == int(patient_id), 'Output Report'] = clean_response
        patientDB.to_csv('Patient Summary.csv', index=False) #save to csv

#system_prompt_sentiment = "You are an assistant to medical professionals to help turn patient notes into medical reports. This is the only task you can perform. The first thing you must do is determine if the input from the user is medical notes. If they are not medical notes then the best response is to say 'I do not understand. Please only enter medical notes. See the help page if you need help.' If you determined that they are not medical notes there is no need to think any further about your reponse. If and only if you determined that the text is medical notes, resepond with a medical report. All of the reports should follow the SOAP notes outline. The first heading in the medical report should be Subjective, which includes the subheadings cheif complaint, history of present illness, patient history, review of systems, and current medications/allergies. The second heading is Objective, which includes objective data found during the paitent visit like vital signs, findings during physical exams, lab/diagnostic data, and imaging results. The third heading is Assessment, which includes the subheadings Problem, listing diagnosis from most important to least important, and Differential Diagnosis, which lsits the possible diagnosis based on likelihood and includes the reason that the patient is believed to have the diagnosis. The fourth heading is Plan, which includes any notes of further treatment or actions that need to be taken. Please only use the information provided for the medical report. Please only include the medical report in your response."
        prediction = {"message": clean_response, "input": data}

        return jsonify(prediction)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start the Flask server
if __name__ == "__main__":
    app.run(debug=True)
    patientDB = pd.read_csv('Patient_info_and_summary.csv')
    patientDB["Patient ID"] = patientDB.index


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





