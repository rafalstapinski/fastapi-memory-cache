class Error(Exception):
    message: str

    def __init__(self):
        super().__init__(self.message)


class UnhashableArgumentsException(Error):
    message = "Could not hash coroutine arguments. Create MemoryCacheContext with the `key` argument."
