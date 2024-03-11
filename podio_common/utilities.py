from enum import Enum
import logging

logger = logging.getLogger(__name__)


class SuperEnum(Enum):
    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other

        if isinstance(other, Enum):
            return self.value == other.value

        return False

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
    
def remove_formatting(input: str) -> str:
    string = str(input)

    # remove paragraph
    string = string.replace("<p>", "").replace("</p>", "")

    # remove < >
    string = string.replace("&gt;", "").replace("&lt;", "")

    return string

def validate_dict(keys, input_dict: dict) -> bool:
    """validate dict and return true or false
    input: keys-> list
           input_dict: dict

    """

    if not isinstance(input_dict, dict):
        logger.error("Not a valid dict input")
        return False

    missing_keys = []

    for i in keys:
        if i not in input_dict:
            missing_keys.append(i)

    if missing_keys:
        logger.info(f"Not a valid dict. Missing keys: {missing_keys}")
        logger.info(input_dict)
        return False

    return True