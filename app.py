import os
import redis
from dotenv import load_dotenv

load_dotenv()
red = redis.Redis(
    host='redis-12339.c1.asia-northeast1-1.gce.cloud.redislabs.com',
    port=12339,
    password=os.dotenv('PASSWORD_REDIS') # пароль от Redis
)