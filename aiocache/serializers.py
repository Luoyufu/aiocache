from aiocache.log import logger


try:
    import ujson as json
except ImportError:
    logger.warning("ujson module not found, usin json")
    import json

try:
    import cPickle as pickle
except ImportError:
    logger.warning("cPickle module not found, using pickle")
    import pickle


class DefaultSerializer:
    """
    Dummy serializer that returns the same value passed both in serialize and
    deserialize methods.

    Supports only str values. If you want to store other python types, coerce them
    to str or use ``PickleSerializer``/``JsonSerializer``.
    """
    encoding = 'utf-8'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dumps(self, value):
        if not isinstance(value, str):
            raise TypeError(
                "DefaultSerializer only supports str types, for other types"
                " check PickleSerializer or JsonSerializer")
        return value

    def loads(self, value):
        return value


class PickleSerializer(DefaultSerializer):
    """
    Transform data to bytes using pickle.dumps and pickle.loads to retrieve it back.
    """
    encoding = None

    def dumps(self, value):
        """
        Serialize the received value using ``pickle.dumps``.

        :param value: obj
        :returns: bytes
        """
        return pickle.dumps(value)

    def loads(self, value):
        """
        Deserialize value using ``pickle.loads``.

        :param value: bytes
        :returns: obj
        """
        if value is None:
            return None
        return pickle.loads(value)


class JsonSerializer(DefaultSerializer):
    """
    Transform data to json string with json.dumps and json.loads to retrieve it back.
    """

    def dumps(self, value):
        """
        Serialize the received value using ``json.dumps``.

        :param value: dict
        :returns: str
        """
        return json.dumps(value)

    def loads(self, value):
        """
        Deserialize value using ``json.loads``.

        :param value: str
        :returns: dict
        """
        if value is None:
            return None
        return json.loads(value)
