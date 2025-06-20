from src.db.manager import DatabaseManager


class BaseService:
    db: DatabaseManager | None

    def __init__(self, db: DatabaseManager | None = None) -> None:
        self.db = db