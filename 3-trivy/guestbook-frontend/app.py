from flask import Flask, render_template, request, jsonify
import redis
import os

app = Flask(__name__)

redis_host = os.getenv('DB_HOST', 'redis')
redis_port = int(os.getenv('DB_PORT', 6379))
redis_password = os.getenv('DB_PASSWORD', '')
pod_name = os.getenv('HOSTNAME', 'local-dev')

# Per-pod counter (resets if pod restarts)
local_counter = 0

def get_redis_client():
    return redis.Redis(
        host=redis_host,
        port=redis_port,
        password=redis_password or None,
        db=0,
        socket_connect_timeout=1,
        socket_timeout=1,
        decode_responses=True
    )

def check_redis():
    try:
        r = get_redis_client()
        r.ping()
        return True, None
    except redis.exceptions.RedisError as e:
        return False, str(e)

@app.get("/healthz")
def healthz():
    return jsonify(status="ok"), 200

@app.get("/readyz")
def readyz():
    ok, err = check_redis()
    if ok:
        return jsonify(status="ready", redis="ok"), 200
    return jsonify(status="not-ready", redis="unavailable", error=err), 503

@app.route("/", methods=["GET", "POST"])
def index():
    global local_counter
    local_counter += 1

    redis_ok, redis_error = check_redis()
    messages = []

    global_counter = None
    if redis_ok:
        try:
            # global counter across all pods (stored in Redis)
            global_counter = get_redis_client().incr("page_hits")
        except redis.exceptions.RedisError as e:
            redis_ok = False
            redis_error = str(e)
            global_counter = None

    if request.method == "POST":
        message = request.form.get("message", "").strip()
        if message and redis_ok:
            try:
                get_redis_client().lpush("messages", message)
            except redis.exceptions.RedisError as e:
                redis_ok = False
                redis_error = str(e)

    if redis_ok:
        try:
            messages = get_redis_client().lrange("messages", 0, -1)
        except redis.exceptions.RedisError as e:
            redis_ok = False
            redis_error = str(e)

    return render_template(
        "index.html",
        messages=messages,
        redis_ok=redis_ok,
        redis_error=redis_error,
        redis_host=redis_host,
        pod_name=pod_name,
        local_counter=local_counter,
        global_counter=global_counter
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

