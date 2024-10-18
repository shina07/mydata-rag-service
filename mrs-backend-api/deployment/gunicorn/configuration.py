bind = "0.0.0.0:8080"

workers = 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 180

BASE_DIR = "/app"
pythonpath = BASE_DIR + "/src"
chdir = BASE_DIR
