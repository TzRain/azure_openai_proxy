import os
from azure.identity import ManagedIdentityCredential, AzureCliCredential, ChainedTokenCredential, get_bearer_token_provider

_credential = ChainedTokenCredential(
    ManagedIdentityCredential(client_id=os.getenv("AZURE_CLIENT_ID")),
    AzureCliCredential(),
)

_token_provider = get_bearer_token_provider(_credential, "https://cognitiveservices.azure.com/.default")

async def get_token() -> str:
    return _token_provider()
