import json

from common.database.session import redis_client


def get_cache(key):
    """ Получить данные из кэша по ключу. """
    cached_value = redis_client.get(key)
    if cached_value:
        return json.loads(cached_value)

    return None

def set_cache(key, value, expire=600):
    """ Сериализовать данные в JSON и сохранить в кэш с определённым временем жизни (expire в секундах). """
    redis_client.set(key, json.dumps(value), ex=expire)