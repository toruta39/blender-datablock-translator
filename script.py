import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET

access_token = ""

def get_access_token():
    "Get access token from Azure Marketplace"

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

    return result['access_token']

def translate(text):
    "Translate text into English via Microsoft Translator"

    url = "http://api.microsofttranslator.com/v2/Http.svc/Translate"

    data = {
        "text": text,
        "to": "en"
    }

    data = urllib.parse.urlencode(data)
    url += "?" + data

    req = urllib.request.Request(url=url, method="GET")
    req.add_header("Authorization", "Bearer " + access_token)

    result = urllib.request.urlopen(req).read()
    result = str(result, "utf-8")
    result = ET.fromstring(result)
    result = result.text

    return result

access_token = get_access_token()
print(translate("これ"))
