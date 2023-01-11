from dataclasses import dataclass

@dataclass
class CallbackData:
    """Class of a image parse callback"""
    url: str
    fileContent: object
    uuid: str
