import os
from azure.identity import ManagedIdentityCredential
from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv("AZURE_CLIENT_ID")
credential = ManagedIdentityCredential(client_id=client_id)
token = credential.get_token("https://cognitiveservices.azure.com/.default").token

print(f"export AZURE_OPENAI_AD_TOKEN={token}")
