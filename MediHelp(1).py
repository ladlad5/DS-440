#!/usr/bin/env python
# coding: utf-8

# In[5]:


import sys
get_ipython().system('{sys.executable} -m pip install ollama')


# In[7]:


# source: ollama github, https://github.com/ollama/ollama-python
from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='deepseek-r1:1.5b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)


# In[9]:


# source: Python DeepSeek Tutorial, https://youtu.be/72Ef65B65JA?si=TSfQj5pqaaogT1rF
import re
#function for application 
def ask_MediHelp(input_content, system_prompt, deep_think = True, print_log = True): 
    #deep_think allows for background thinking to be visible
    #system_prompt helps LLM better fit use case
    response: ChatResponse = chat(model = "deepseek-r1:1.5b", messages =[
        {'role' : 'system', 'content' : system_prompt}, #refers to system_prompt above
        {'role' : 'user', 'content' : input_content} #user input (input_content) instead of just hard code "why is the sky blue"
    ])
    response_text = response['message']['content']
    if print_log: print(response_text) 
    think_texts = re.findall(r"<think>(.*?)</think>", response_text, flags=re.DOTALL) #extracts deep_think
    think_texts = "\n\n".join(think_texts).strip() 
    clean_response = re.sub(r"<think>.*?</think>", '', response_text, flags = re.DOTALL).strip() #just finding response without think text 

    return clean_response if not deep_think else (clean_response, think_texts)


# In[11]:


import pandas as pd
#source: huggingface, https://huggingface.co/datasets/jung1230/patient_info_and_summary
medical_notes_data = pd.read_csv("hf://datasets/jung1230/patient_info_and_summary/Patient_info_and_summary.csv").head()
medical_notes_data["Patient ID"] = medical_notes_data.index
medical_notes_data


# In[43]:


#Source for Soap Notes: https://www.ncbi.nlm.nih.gov/books/NBK482263/
#system_prompt_sentiment = "You will be provided with patient information and notes on their treatment and progress. You are tasked with taking the notes and formatting them into a medical report. The format of your responses should be consistent between responses. The format should follow the SOAP notes outline. The first heading in the medical report should be Subjective, which includes the subheadings cheif complaint, history of present illness, patient history, review of systems, and current medications/allergies. The second heading is Objective, which includes objective data found during the paitent visit like vital signs, findings during physical exams, lab/diagnostic data, and imaging results. The third heading is Assessment, which includes the subheadings Problem, listing diagnosis from most important to least important, and Differential Diagnosis, which lsits the possible diagnosis based on likelihood and includes the reason that the patient is believed to have the diagnosis. The fourth heading is Plan, which includes any notes of further treatment or actions that need to be taken. Please only use the information provided for the medical report. Please only include the medical report in your response."
system_prompt_sentiment = "You are an assistant to medical professionals to help turn patient notes into medical reports. This is the only task you can perform. The first thing you must do is determine if the input from the user is medical notes. If they are not medical notes then the best response is to say 'I do not understand. Please only enter medical notes. See the help page if you need help.' If you determined that they are not medical notes there is no need to think any further about your reponse. If and only if you determined that the text is medical notes, resepond with a medical report. All of the reports should follow the SOAP notes outline. The first heading in the medical report should be Subjective, which includes the subheadings cheif complaint, history of present illness, patient history, review of systems, and current medications/allergies. The second heading is Objective, which includes objective data found during the paitent visit like vital signs, findings during physical exams, lab/diagnostic data, and imaging results. The third heading is Assessment, which includes the subheadings Problem, listing diagnosis from most important to least important, and Differential Diagnosis, which lsits the possible diagnosis based on likelihood and includes the reason that the patient is believed to have the diagnosis. The fourth heading is Plan, which includes any notes of further treatment or actions that need to be taken. Please only use the information provided for the medical report. Please only include the medical report in your response."
#The response should include a heading staing the patient name, age, and date of birth.


# In[15]:


#testing how it will work through UI when given anticipated medical notes
#print(medical_notes_data["Patient Progress Summary"][0])
ask_MediHelp("A 17-year-old, nonparous girl presented with a one-month history of noticeable pelvic mass and was diagnosed to have a left ovarian tumour in 2007 with a raised serum CA-125 of 350 IU/L. Other tumour markers were not performed due to financial constraint. An intraoperative frozen section revealed immature teratoma and she underwent fertility sparing surgery. A staging laparotomy with left salpingo-oophorectomy, peritoneal cytology, pelvic lymph nodes sampling, and infracolic omentectomy was performed. Postoperative histology report revealed mature teratoma with focal area of immature teratoma of the left ovary. There was no malignant cell infiltration to the omentum or lymph nodes. Histology revealed immature teratoma grade I, FIGO stage 1a. Despite being advised for close surveillance, she defaulted followup after 6 months postoperative. One year later, she presented with lower abdominal discomfort and resought medical advice. She developed radiological recurrence of pelvic mass with a raised serum CA-125 of 180 IU/L following which she completed 6 courses of systemic chemotherapy (carboplatin-paclitaxel). After chemotherapy, the tumour marker normalised (<35 IU/L) but the pelvic mass progressively increased in size. CT scan of the abdomen and pelvis revealed presence of bilateral large adnexal masses with infiltration into uterus and also possibly to the sigmoid colon. Growing teratoma syndrome was suspected. She underwent staging laparotomy and complete excision of the tumour. Full bilateral pelvic lymphadenectomy was done. Postoperative CT scan of the abdomen and pelvis showed no residual disease. Histology of excised mass revealed mature teratoma with no presence of immature cells. The patient remained with no recurrence at the time of this report, which is 8 months after the second operation for GTS.", system_prompt_sentiment)


# In[19]:


#testing how it will work if given unanticipated prompt
ask_MediHelp("Tell me how to bake a pie.", system_prompt_sentiment)


# In[21]:


#testing how it will work if given unanticipated prompt
#adjusting prompt so it knows how to respond to unrelated prompt
#system_prompt_sentiment = "You will be provided with text. First check if the information given is medical notes. If it is not medical notes, respond with the following statement found in single quotations: 'I don't understand. Please only enter medical notes you wish to be turned into a medical report. If you need help, information is avalible on the help page.' If the text is medical notes, you will use the notes given and the following information to format a medical report. The format of your report should be consistent between responses. The format should follow the SOAP notes outline. The first heading in the medical report should be Subjective, which includes the subheadings cheif complaint, history of present illness, patient history, review of systems, and current medications/allergies. The second heading is Objective, which includes objective data found during the paitent visit like vital signs, findings during physical exams, lab/diagnostic data, and imaging results. The third heading is Assessment, which includes the subheadings Problem, listing diagnosis from most important to least important, and Differential Diagnosis, which lsits the possible diagnosis based on likelihood and includes the reason that the patient is believed to have the diagnosis. The fourth heading is Plan, which includes any notes of further treatment or actions that need to be taken."

ask_MediHelp("Tell me how to bake a pie.", system_prompt_sentiment)


# In[25]:


#making a new column with the medical reports created with deepseek and a collumn with the background thinking
medical_notes_data[['MediHelp_generated_medical_report', 'MediHelp_deep_think']] =  medical_notes_data['Patient Progress Summary'].apply(lambda row: ask_MediHelp(row, system_prompt_sentiment)).apply(pd.Series)


# In[55]:


#testing how it will work if asked to give out patient information.
#prompt engineering
#print(medical_notes_data["Patient Progress Summary"][2])

#system_prompt_sentiment = "You are an assistant to medical professionals to help turn patient notes into medical reports. First determine if the input from the user is medical notes. If they are not medical notes then repond by saying 'I do not understand. Please only enter medical notes. See the help page if you need help.' Second, if you determined that the text is medical notes, resepond with a medical report. all of the reports should follow the SOAP notes outline. The first heading in the medical report should be Subjective, which includes the subheadings cheif complaint, history of present illness, patient history, review of systems, and current medications/allergies. The second heading is Objective, which includes objective data found during the paitent visit like vital signs, findings during physical exams, lab/diagnostic data, and imaging results. The third heading is Assessment, which includes the subheadings Problem, listing diagnosis from most important to least important, and Differential Diagnosis, which lsits the possible diagnosis based on likelihood and includes the reason that the patient is believed to have the diagnosis. The fourth heading is Plan, which includes any notes of further treatment or actions that need to be taken. Please only use the information provided for the medical report. Please only include the medical report in your response."

ask_MediHelp("how tall are koalas", system_prompt_sentiment)


# In[51]:


#prompt engineering
ask_MediHelp("how do cars work", system_prompt_sentiment)


# In[49]:


#system_prompt_sentiment = "You are an assistant to medical professionals to help turn patient notes into medical reports. First determine if the input from the user is medical notes. If they are not medical notes then repond by saying 'I do not understand. Please only enter medical notes. See the help page if you need help.' If you determined that they are not medical notes there is no need to think any further about your reponse. Second, if you determined that the text is medical notes, resepond with a medical report. all of the reports should follow the SOAP notes outline. The first heading in the medical report should be Subjective, which includes the subheadings cheif complaint, history of present illness, patient history, review of systems, and current medications/allergies. The second heading is Objective, which includes objective data found during the paitent visit like vital signs, findings during physical exams, lab/diagnostic data, and imaging results. The third heading is Assessment, which includes the subheadings Problem, listing diagnosis from most important to least important, and Differential Diagnosis, which lsits the possible diagnosis based on likelihood and includes the reason that the patient is believed to have the diagnosis. The fourth heading is Plan, which includes any notes of further treatment or actions that need to be taken. Please only use the information provided for the medical report. Please only include the medical report in your response."
ask_MediHelp("how do planes work", system_prompt_sentiment)


# In[45]:


#system_prompt_sentiment = "You are an assistant to medical professionals to help turn patient notes into medical reports. This is the only task you can perform. The first thing you must do is determine if the input from the user is medical notes. If they are not medical notes then the best response is to say 'I do not understand. Please only enter medical notes. See the help page if you need help.' If you determined that they are not medical notes there is no need to think any further about your reponse. If and only if you determined that the text is medical notes, resepond with a medical report. All of the reports should follow the SOAP notes outline. The first heading in the medical report should be Subjective, which includes the subheadings cheif complaint, history of present illness, patient history, review of systems, and current medications/allergies. The second heading is Objective, which includes objective data found during the paitent visit like vital signs, findings during physical exams, lab/diagnostic data, and imaging results. The third heading is Assessment, which includes the subheadings Problem, listing diagnosis from most important to least important, and Differential Diagnosis, which lsits the possible diagnosis based on likelihood and includes the reason that the patient is believed to have the diagnosis. The fourth heading is Plan, which includes any notes of further treatment or actions that need to be taken. Please only use the information provided for the medical report. Please only include the medical report in your response."
ask_MediHelp("how do trains work", system_prompt_sentiment)


# In[ ]:


pd.set_option('display.max_colwidth', None)
medical_notes_data


# In[21]:


#medical report for first row
print(medical_notes_data['MediHelp_generated_medical_report'][0])


# In[23]:


#checking consistency between reports: Some common headings, look at training it to be more consistent in layout and including heading with paitent info
print(medical_notes_data['MediHelp_generated_medical_report'][1])


# In[ ]:




