from dataclasses import dataclass


@dataclass
class TrackerDto:
    dispute_id: str
    chat_id: int
    username: str

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        if len(value) > 64:
            self.username = f'{value[0:61]}...'
        self._username = value
