from utils.repository import AbstractRepository

class RequestService:
    def __init__(self, request_repo: AbstractRepository):
        self.request_repo: AbstractRepository = request_repo()
        