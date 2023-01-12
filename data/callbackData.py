from dataclasses import dataclass
from typing import Optional

@dataclass
class CallbackData:
    """Class of a image parse callback"""
    url: Optional[str]
    fileContent: object
    uuid: str
