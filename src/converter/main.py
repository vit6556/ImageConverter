import os
import sys

python_path = os.path.join(os.getcwd())
sys.path.append(python_path)
os.environ["PYTHONPATH"] = python_path

from common.database.session import redis_client


def main():
    while True:
        _, image_hash = redis_client.blpop('image_tasks', timeout=0)
        print(image_hash)

if __name__ == '__main__':
    main()