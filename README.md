# TeleWhisper EVO
EVOlution of TeleWhisper

Open-sourced due to a lack of sufficient retribution.

## 1. How to run it

### 1.1 Setting the environment
For local testing, just install python and the requirements with:
```bash
pip install -r requirements.txt
```

If you want to run it with Docker, **make sure you have it installed as well**.

### 1.2 Setting the variables
The setup variables are set up via an `env.ini` file in the project root directory. Contents must be as this:
```ini
[Telegram]
# Obtained from Telegram Developer console
api_id=<API_ID>
api_hash=<API_HASH>

# Obtained from @BotFather Telegram bot
bot_token=<BOT_TOKEN>

[Database]
host=<DB_HOST>
database=<DB_NAME>
port=<DB_PORT>
username=<DB_USER>
password=<DB_USER_PASSWORD>

# ATM, MANDATORY
[OpenAI]
api_key=<OPENAI_API_KEY>

# OPTIONAL. You can remove this 'Local' Section if you don't want to install and use local whisper model
[Local]
use_local_whisper=True
# Select a model size from the official openai/whisper github repo
model_size=small

# MANDATORY
[DeepL]
api_key=<DEEPL_API_KEY>

# MANDATORY
[FireworksAI]
api_key=<FIREWORKSAI_API_KEY>
url=<SERVICE_URL>

# MANDATORY
[RunPod]
api_key=<RUNPOD_API_KEY>
# RunPod URL must be a FasterWhisper serverless instance or pod
url=<SERVICE_URL>

# MANDATORY
[Downloads]
# VPS Host and port must be accessible from the outside (make sure you have a firewall and a reverse proxy properly configured)
host=<VPS_HOST>
port=<VPS_PORT>
```

### 1.3 Run it
### 1.3.1 Locally
```bash
python main.py
```
or install uvicorn and run it with
```bash
python -m uvicorn main:app
```

### 1.3.2 Dockerized
```bash
docker build -t <image_name> .
docker run -d -p <host>:<download_port> <image_name>
```

## 2. How it works
Here's more or less the structure:
![image](https://github.com/user-attachments/assets/58a7da47-f6d5-4c4e-aa07-b42c61fe4fb7)

This happens when the user sends a file:
![image](https://github.com/user-attachments/assets/cb32e22d-851a-48f8-9884-499021d2e6f9)

## License
All the code here is under the CC BY-NC License.
Any use of this code must not be commercial unless with explicit permission.

![image](https://github.com/user-attachments/assets/f3debc6e-dc79-49fa-bbc6-e0d40b3413c1)
