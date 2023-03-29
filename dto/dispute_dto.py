from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class DisputeDto:
    id: str
    text: str
    ends_on: datetime
    created_on: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc))
