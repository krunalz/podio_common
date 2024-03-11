import logging
import podio_common.podio.podio as Podio
from podio_common.podio.podio_item_source import PodioItemSource


logger = logging.getLogger(__name__)


class PodioItem:
    """
    Main class for all podio items, represents a podio item
    """

    def __new__(cls, *args, **kwargs):
        if cls is PodioItem:
            raise TypeError(f"only childrens of '{cls.__name__}' may be instantiated")
        return object.__new__(cls, *args, **kwargs)

    def read_common_fields_from_item_json(self) -> bool:
        """Reads common fields for items regardless of type"""
        self.valid_item = False
        if not self.instantiated_from == PodioItemSource.PodioJSON:
            logger.info("Common fields can only be read if instantiated from JSON")
            return False

        if not Podio.validate_ticket_json_dict(self.item_json):
            logger.info(f"Not a valid ticket detail json...")
            return False

        ## KK add a try

        if "app_item_id" in self.item_json:
            self.app_item_id = self.item_json["app_item_id"]
            self.app_item_id_formatted = self.item_json["app_item_id_formatted"]
            self.item_id = self.item_json["item_id"]
            if "app" in self.item_json and "app_id" in self.item_json["app"]:
                self.app_id = self.item_json["app"]["app_id"]
            else:
                self.app_id = 0
            self.created_on = self.item_json["created_on"]

            if "comments" in self.item_json:
                self.comments = self.item_json["comments"]
            else:
                self.comments = ""

            self.last_event_on = self.item_json["last_event_on"]

            if "refs" in self.item_json:
                self.refs = self.item_json["refs"]
            else:
                self.refs = ""

            self.title = self.item_json["title"]

            if "files" in self.item_json:
                self.files = self.item_json["files"]
            else:
                self.files = ""

            self.fields = self.item_json["fields"]

            self.valid_item = True

        return self.valid_item

    def get_field_value_by_id(self, field_id: int, remove_formatting: bool = True, convert_none: bool = True):
        return Podio.get_field_by_field_id(self.fields, field_id, remove_formatting, convert_none)

    def get_field_value_by_label(self, field_label: str, remove_formatting: bool = True, convert_none: bool = True):
        return Podio.get_field_by_field_label(self.fields, field_label, remove_formatting, convert_none)

    def invalid_field(self, message: str) -> None:
        logger.info(message)
        if self.invalid_reasons is None:
            self.invalid_reasons = message
        else:
            self.invalid_reasons += message

        self.valid_item = False
