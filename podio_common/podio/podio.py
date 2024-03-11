import logging
import os
import csv
from .pypodio import api
import podio_common.utilities as Util
from datetime import date, datetime

logger = logging.getLogger(__name__)


################################### THIS MODULE HOLDS PODIO METHODS
## ALL INPUTS/OUTPUTS ARE DICT

### API CALL METHODS


def get_podio_app(
    podio_client_id: int,
    podio_client_secret: str,
    podio_app_id: int,
    podio_app_token: str,
) -> api.OAuthAppClient:
    """
    Get podio client app

    :param podio_client_id: Podio Client ID
    :type: int

    :param podio_client_secret: Podio Client Secret
    :type: str

    :param podio_app_id: Application ID
    :type: int

    :param podio_app_token: Podio Client Token
    :type: str

    :return: OAuthAppClient
    :rtype: api.OAuthAppClient
    """
    try:
        return api.OAuthAppClient(
            podio_client_id, podio_client_secret, podio_app_id, podio_app_token
        )
    except Exception as e:
        directory = 'error_logs'
        file_name = f'{date.today().strftime("%d-%m-%Y")}.csv'
        file_path = os.path.join(directory, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r', newline='') as file:
                existing_text = file.read().strip()
                if existing_text:
                    with open(file_path, 'a', newline='') as file:
                        file.write(f'Time : {datetime.now().time().strftime("%H:%M:%S")}\n{e}\n\n')
                else:
                    with open(file_path, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([f'Time : {datetime.now().time().strftime("%H:%M:%S")}\n{e}\n\n'])
        else:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([f'Time : {datetime.now().time().strftime("%H:%M:%S")}\n{e}\n\n'])
           


def get_item_by_id(app: api.OAuthAppClient, item_id: int) -> dict:
    """
    Get item by item_id

    :param app: OAuthAppClient
    :type: api.OAuthAppClient

    :param item_id: Item ID
    :type: int

    :return: Item info
    :rtype: dict
    """
    return app.Item.find(item_id)


def get_item_values_by_item_id(
    app: api.OAuthAppClient, item_id: int, values_only: bool = True
) -> dict:
    """returns a podio item values"""
    if values_only:
        return app.Item.values_v2(item_id)
    else:
        return app.Item.values(item_id)


def get_items_by_filter(app: api.OAuthAppClient, app_id: int, filter: dict) -> dict:
    """returns podio item values by filter"""
    return app.Item.filter(app_id, filter)


def create_item(app: api.OAuthAppClient, app_id: int, insert: dict) -> dict:
    """insert a podio item in referenced app"""
    return app.Item.create(app_id, insert)


def update_item_by_id(app: api.OAuthAppClient, item_id: int, update) -> dict:
    """update a podio item in referenced app"""
    return app.Item.update(item_id, update)


### OTHER METHODS


def get_value(field):
    """Returns field value based on field type"""
    if field["type"] == "text":
        return field["values"][0]["value"]

    elif field["type"] in ["number", "money"]:
        return field["values"][0]["value"]

    elif field["type"] == "category":
        return field["values"][0]["value"]["id"]

    elif field["type"] == "date":
        return field["values"][0]["start_date"]

    # apps might have multiple references so we must create a list
    elif field["type"] == "app":
        value = []
        if "config" in field:
            if "settings" in field["config"]:
                if "referenced_apps" in field["config"]["settings"]:
                    for i in field["values"]:
                        value.append(i["value"])

                    return value

        for i in field["values"]:
            value.append(i["value"]["item_id"])

        return value

    return None


def get_category_value(field):
    """Returns field category label value"""
    if field["type"] == "category":
        return field["values"][0]["value"]["text"]


def value_cleanup(value, remove_formatting: bool = True, convert_none: bool = True):
    if value is None:
        if convert_none:
            return ""

    if remove_formatting:
        return Util.remove_formatting(value)

    return value


def get_field_by_field_id(
    fields, field_id: int, remove_formatting: bool = True, convert_none: bool = True
):
    """Returns podio field value by field_id"""
    value = None
    for f in fields:
        if f["field_id"] == field_id:
            value = get_value(f)
            break

    if f["type"] == "app":
        return value

    return value_cleanup(value, remove_formatting, convert_none)


def get_field_by_field_label(
    fields, field_label: str, remove_formatting: bool = True, convert_none: bool = True
):
    """Returns podio field value by field label"""
    value = None
    for f in fields:
        if f["label"] == field_label:
            if f["type"] == "category":
                value = get_category_value(f)
            else:
                value = get_value(f)

            break

    return value_cleanup(value, remove_formatting, convert_none)


def validate_purchase_order_item_attributes(attributes: dict) -> bool:
    """validate order item attributes dict
    input: attributes
    outpu: true or false
    """

    keys = [
        "instantiated_from",
        "item",
        "ticket_subject",
        "ticket_number",
        "order_item",
        "quantity",
        "priority",
        "status",
        "additional_note",
        "shipping_address",
        "customer",
        "orders",
    ]

    return Util.validate_dict(keys, attributes)
