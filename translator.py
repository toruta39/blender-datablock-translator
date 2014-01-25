import urllib.request
import urllib.parse
import json
import time
import xml.etree.ElementTree as ET

access_token = ""
access_token_expires_at = time.time()


def get_access_token():
    """Get access token from Azure Marketplace.
    If there's no existed access token, it'll try request a new one.

    Returns: string
    """

    global access_token

    if (not bool(access_token)) or time.time() > access_token_expires_at:
        access_token = req_access_token()

    return access_token


def req_access_token():
    """Request a new access token from Azure Marketplace

    Returns: string
    """

    global access_token_expires_at

    url = "https://datamarket.accesscontrol.windows.net/v2/OAuth2-13"
    data = {
        "client_id": "blender-assets-translator",
        "client_secret": "5TITh8SzOtQIefUJ/vKW10yk4/oNbGbgI+GquUdtgHo=",
        "scope": "http://api.microsofttranslator.com",
        "grant_type": "client_credentials"
    }

    data = urllib.parse.urlencode(data)
    data = bytes(data, "utf-8")

    req = urllib.request.Request(url=url, data=data)

    result = urllib.request.urlopen(req).read()
    result = str(result, "utf-8")
    result = json.loads(result)

    access_token_expires_at = time.time() + int(result["expires_in"])

    return result["access_token"]


def translate(text, to_lang="en", from_lang=""):
    """Translate text to the target language

    Keyword arguments:
    text -- text to translate
    to_lang -- optional, the target language code
    from_lang -- optional, the source language code

    Returns: string
    """

    url = "http://api.microsofttranslator.com/v2/Http.svc/Translate"

    data = {
        "text": text,
        "to": to_lang,
        "from": from_lang
    }

    data = urllib.parse.urlencode(data)
    url += "?" + data

    req = urllib.request.Request(url=url, method="GET")
    req.add_header("Authorization", "Bearer " + get_access_token())

    result = urllib.request.urlopen(req).read()
    result = str(result, "utf-8")
    result = ET.fromstring(result)
    result = result.text

    return result
