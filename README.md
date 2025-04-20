# MediHelp
MediHelp is an AI chatbot for medical providers to use to turn medical notes into formatted medical reports. It is locally hosted to ensure security and utilizes DeepSeek, an open source LLM.

# Login PIN: 0000

# Instructions:

## Local Hosting

### Required software:

#### Python:

Python: https://www.python.org

Ensure that python is properly installed by opening the terminal and typing "python". If the command line does not change as shown below, python is not properly installed and the program will not work:

![](https://prepbytes-misc-images.s3.ap-south-1.amazonaws.com/assets/1682490438283-download%20%2840%29.png)

Image credit: https://prepbytes-misc-images.s3.ap-south-1.amazonaws.com/assets/1682490438283-download%20%2840%29.png

#### Ollama:

Download Ollama from here: https://ollama.com

Install the set up normally, you will know ollama is properly installed when the "ollama" command is recognized in the terminal

### Running Medihelp:

Once python and ollama are properly downloaded, you are good to run Medihelp.

1. Download repo as ZIP file.
2. Extract to folder of choice.
3. Run start.bat

If you have pip installed, the startup script will download all the necessary python libraries to run the program, it will also install the most lightweight deepseek model to use.

Once everything is downloaded and verified installed by the start script, it will then start the flask server and Medihelp app.

### If startup script does not work:

1. Open terminal
2. Run the following command: python -m pip install flask flask-cors flask-ngrok requests pandas ollama streamlit
3. Run: ollama pull deepseek-r1:1.5b
4. Open new terminal in the medihelp folder (or navigate to it)
5. Run: python middlewaredeepseek.py
6. Open a second terminal in the Medihelp folder
7. Run: python -m streamlit run middlewareTest.py --server.headless false --theme.base dark

### If Neither options work:

Use the Azure hosted alternative below as a last resort if starting manually does not work. Due to budget constraints, the azure machine running an instance of Medihelp does not have a GPU, therefore performance will be very slow.

## Azure Hosted Alternative:
There is also an azure hosted alternative for demonstration purposes in case the code is not running on your machine. Please note performance will be slower than running a local host on a GPU machine:
https://ladlad5-ds-440-middlewaretestremote-sk8ifn.streamlit.app/






# Sources: 
* Dataset from Huggingface: https://huggingface.co/datasets/jung1230/patient_info_and_summary
* Ollama Github: https://github.com/ollama/ollama-python
* Python DeepSeek Tutorial: https://youtu.be/72Ef65B65JA?si=TSfQj5pqaaogT1rF
* Soap Notes Information: https://www.ncbi.nlm.nih.gov/books/NBK482263/

