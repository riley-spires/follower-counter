from dataclasses import dataclass

@dataclass(frozen=True)
class FollowerResponse():
    id: str
    followers_count: int
