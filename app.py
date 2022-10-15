import os
import redis
from dotenv import load_dotenv

load_dotenv()

red = redis.Redis(
    host=os.getenv('HOST_REDIS'),
    port=os.getenv('PORT_REDIS'),
    password=os.getenv('PASSWORD_REDIS')
)