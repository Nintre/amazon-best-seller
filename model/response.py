class Response:
    def __init__(self, code: int = 0, payload: any = None, exception: Exception = None):
        self.code = code
        self.payload = payload
        self.exception = exception

    def failed_with_code(self, code: int):
        self.code = code

    def failed_with_exception(self, exception: Exception):
        self.code = 7
        self.exception = exception

    def failed_with_msg(self, msg: str):
        self.code = 7
        self.exception = Exception(msg)

    def ok_with_detail(self, data):
        self.payload = data

    def failed(self):
        self.code = 7