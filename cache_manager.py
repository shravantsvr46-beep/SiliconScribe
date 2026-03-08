import hashlib
import json
import os

CACHE_FILE = "cache.json"


def get_cache_key(prompt):
    return hashlib.md5(prompt.encode()).hexdigest()


def load_cache(key):

    if not os.path.exists(CACHE_FILE):
        return None

    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)

    return cache.get(key)


def save_cache(key, data):

    if os.path.exists(CACHE_FILE):

        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)

    else:
        cache = {}

    cache[key] = data

    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)