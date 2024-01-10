import os
from dotenv import load_dotenv, find_dotenv
import json
import base64


def get_service_account_key(forMainDB: bool = False) -> dict:
    """
    Returns service account key for firestore

    Args:
        forMainDB (bool, optional): If false, service account key for database
        containing only statistics is returned. If true, service account
        key for database containing all jobs is returned. Defaults to False.

    Returns:
        dict: Service account key
    """
    load_dotenv(find_dotenv())
    var_name = ""
    if forMainDB:
        var_name = 'BACKEND_DB'
    else:
        var_name = 'FRONTEND_DB'

    encoded_key = os.getenv(var_name)

    # https://stackoverflow.com/questions/50693871/error-in-json-loads-for-data-that-has-base64-decoding-applied
    dic = base64.b64decode(str(encoded_key)[2:-1]).decode('utf-8')
    return json.loads(dic)


def service_key_to_base64(service_key: dict) -> bytes:
    """
    Converts firebase service key to base64.

    Args:
        service_key (dict): Service account key generated in firebase project
        settings. Check docs for an example of a service key.

    Returns:
        bytes: base64 string. String begins with `b'` and ends with `'`
    """

    # convert json to a string
    str_service_key = json.dumps(service_key)

    # encode service key
    encoded_service_key = base64.b64encode(str_service_key.encode('utf-8'))

    # Format of encoded_service_key: b'a_lot_of_chars'
    return encoded_service_key


if __name__ == "__main__":
    service_key = {
        "type": "",
        "project_id": "",
        "private_key_id": "",
        "private_key": "",
        "client_email": "",
        "client_id": "",
        "auth_uri": "",
        "token_uri": "",
        "auth_provider_x509_cert_url": "",
        "client_x509_cert_url": "",
        "universe_domain": ""
    }
    print(service_key_to_base64(service_key))