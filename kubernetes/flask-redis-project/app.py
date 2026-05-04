from flask import Flask
from redis import Redis
import os

app = Flask(__name__)
redis = Redis(
    host=os.environ.get('REDIS_HOST', 'redis-service'),
    port=int(os.environ.get('REDIS_PORT', 6379)),
    password=os.environ.get('REDIS_PASSWORD', ''),
    decode_responses=True
)

@app.route('/')
def index():
    count = redis.incr('hits')
    return f'This page has been visited {count} times.\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)