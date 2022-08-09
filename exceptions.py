class UnknownPayload(Exception):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    def __str__(self) -> str:
        return f"Unknown payload for user with id {self.user_id}"
