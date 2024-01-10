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
         "type": "service_account",
  "project_id": "itjobmeter-stats",
  "private_key_id": "30c9e13fcf93060045fa9f5405d2ae5a01febacd",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC07kKTtMT/GQN0\nf6uDdKIaLrl3V/z9aZG65/P4VgisV9rpxLuh+Hro3qlqDK52ga9OUc7svfj1Mw/G\nYGpsq+dK3lyggLCWq4/MmioDD5a7kihaRuEMM+exNGlXKAdSgQ6oPapPd3suQMAP\ns1EIqikPUhJWE1CDUBbraYxmwWe+5Bk6SSWJVtuFCU2DxeCMz1kG4RUTL+7RNp5o\nBXjvGez+916bJFaYN9RIcWLJp5FwJ3rsJ120m+iAqV3c14YE4dwptPHlrs5pWbyA\nxyYYcPm/nuqpTuGFXzO71Vg6KBXGupPjMHjIT51giLw4luxP78+Bu5ZNDqpUH/2A\nnJyBmgnHAgMBAAECggEAHAhWVGBLrWKIwIIPZtypSPk4Tx9Y2UKEC7tod2+NBHbQ\nOiv7Dktbb70f7ohsd3v8V1whfVipvAPfS9MgahnwSg9Ntqh5s759FyxDmhnONt2c\nVvBoaeWY3kHKmHBhQg0w4iw7uPhAI5hwqX4U7gy/M9p5cNCpRs8f3fWKhVkt48tc\nwvnRNw+utSNGGkXG4sjHeyDkwIjVndOK/84dE1D4AiW6klbPOo7jExwNo2mKSU7w\nnP5nE6t58TkC9/vSq8JIjFRtFZYCsESPbuXBv0RSBGK8doFqIQrP8cFxakWq0mFP\nFp5+xl7ZFRmAD5zmMqRd123rIqPakuDuEkSPUkrh4QKBgQDhMvr4iG33bmsYNTeE\nnHEyZsa8DEowWd/qJcfNQTiKX/2Rv68IfgNuG/SkYLYdaIFfEsRIF1eOAu25oXDa\nysilqmriXBDvQEYrVtWtLm/sYdjt3coTepg9UXBmqJpU2NTWBxODw4OaS633hSIT\nWud1fkL4hCV2ZyFfJXYefPuubwKBgQDNrUjtS+rQGZfsqHbVJJCEaleQm6g5Ow2r\njUscipU2XxiKWNObnoNSNMdaB79XA9YQQOF+izOSfnccd4lLFHVhFvBFcKEkb2+l\n2eQk7uS7dfUplxTZRmeJVdZEHnXGX7MuJ5uJCk12gItfX0aDWYMrx8abc4ThQ2Ht\nyxMW7lOGKQKBgGu6jpKL+UcPXE31Tzyx9fitb86PdoIQzGvfbOhElf6kEtJBR0Mh\nvRRUbUChPx1sW88WVC1EdU7rGbveffU8YqXVk1H7xuIc9jRPUuKIv2PuHu8TVVLi\nJ6fVqJaDe2ixXYeRVQWIZxFNuMgauQVXTDhJkVH/LUip5y3z5sCI+4EjAoGATVwi\nE+78EO2vcPokSCMKoGOHMAL8ERqfF6l7WO7fFKZMCq1CWkQSzLbBTKGhXE87Er30\nkq405aLfljt3zl+RjsUb9mJYmeW4Lr93ylR4f/HsFoqW8upCQyuf/dsfHVAdivym\nybKwVCQhR+wED595cNwhXZLjpf68NL6vHW7ix5ECgYAt/Typw4lcmyhBGeRcdLPx\nmGVQrGFSHs7ih2BxcU8OIOYLieXfpaD8GnGxuO3LrDafgtPTspm3wXVrrH1gsYut\np368H2VJLHan9M2VbZuM471x2Z7bpWM17ouKpadvLGg00GjB/zTN2aM2/JhxuhMn\nDYPHsYcY5R3/U90sBZ4vOA==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-mk9ry@itjobmeter-stats.iam.gserviceaccount.com",
  "client_id": "110828251736539836081",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-mk9ry%40itjobmeter-stats.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
    }
    print(service_key_to_base64(service_key))
    # b'eyJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsICJwcm9qZWN0X2lkIjogInh4eCIsICJwcml2YXRlX2tleV9pZCI6ICJ4eHgiLCAicHJpdmF0Z
    # V9rZXkiOiAieHh4eCIsICJjbGllbnRfZW1haWwiOiAieHh4eC5jb20iLCAiY2xpZW50X2lkIjogInh4eHgiLCAiYXV0aF91cmkiOiAieHh4eCIsI
    # CJ0b2tlbl91cmkiOiAieHh4eCIsICJhdXRoX3Byb3ZpZGVyX3g1MDlfY2VydF91cmwiOiAieHh4eCIsICJjbGllbnRfeDUwOV9jZXJ0X3VybCI6ICJ4eHh4In0='
