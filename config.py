from os import getenv

from dotenv import load_dotenv

load_dotenv()

chat_service_url = getenv("CHAT_SERVICE_URL")
auth_service_url = getenv("AUTH_SERVICE_URL")
redis_url = getenv("REDIS_URL")


if not chat_service_url or auth_service_url or redis_url:
    pass