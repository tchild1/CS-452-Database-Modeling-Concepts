# initialize Redis connection settings
REDIS_HOST = "redis-12451.c92.us-east-1-3.ec2.redns.redis-cloud.com"
REDIS_PORT = 12451  # <-- likely need to change this too!
REDIS_PASSWORD = "nfHwOqM8l2FbrngijezO0B2WSFuQkKq8"
REDIS_DB = 0

# initialize constants used to control image spatial dimensions and
# data type
IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224
IMAGE_CHANS = 3
IMAGE_DTYPE = "float32"

# initialize constants used for server queuing
IMAGE_QUEUE = "image_queue"
BATCH_SIZE = 32
SERVER_SLEEP = 0.25
CLIENT_SLEEP = 0.25
