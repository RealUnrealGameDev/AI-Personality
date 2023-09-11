# AI-With-Personality

This AI uses the Llama algorithm to give a personality to the GGML models.
The AI has the ability to use basic emojis as well as text to interact with the User.
There is a config file that we can setup to describe the personality of the AI as well as changing some of the variables for the AI.
The AI is meant to work over the internet on a server and being connected to by a client.

# How to Setup
Step 1: Clone the Repo into a folder

Step 2: Download The Model from Google Drive: https://drive.google.com/drive/folders/15vE8kIPO6qF1M0kLiallWwUZSG4BMaRS?usp=drive_link

Step 3: Install the `requirements.txt` with `pip install requirements.txt`

Step 4: Open the config file and change `PERSONA_NAME` to the name of the personality

Step 5: Change `PERSONA_DESC` to the description of the personality in second person

Step 6: Open the `server.py` file and change the `SERVER` variable to the public IP of the server machine (Private IP if running on LAN network)

Step 7: Open the `client.py` file the change the `SERVER` variable to the public IP of the server machine (Private IP if running on LAN network)

Step 8: Run `server.py`

Step 9: Run `client.py` or `gui.py`(EXPERIMENTAL) and Enjoy!
# Examples
Server:

![Screenshot 2023-09-03 192913](https://github.com/RealUnrealGameDev/AI-Personality/assets/67384349/ec9bf52e-f737-4100-9947-9d5133b68ecb)

Client:

![Screenshot 2023-09-03 192923](https://github.com/RealUnrealGameDev/AI-Personality/assets/67384349/5ee9bbd9-2b80-4462-8bf1-e3abdc04d7fe)
