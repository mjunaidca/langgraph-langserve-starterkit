from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

# Custom GPTs
JWT_API_KEY = config("JWT_API_KEY", cast=Secret, default="secret")

OPENAI_API_KEY = config("OPENAI_API_KEY", cast=Secret, default="")
LANGCHAIN_TRACING_V2 = "false"
LANGCHAIN_API_KEY = ''
LANGCHAIN_ENDPOINT = "https://api.smith.langchain.com"
LANGCHAIN_PROJECT = ''
LANGFUSE_PUBLIC_KEY = ''
LANGFUSE_SECRET_KEY = ''
LANGFUSE_HOST = "https://us.cloud.langfuse.com"  # for US data region
