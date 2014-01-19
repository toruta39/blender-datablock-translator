import urllib.request
import urllib.parse
import json

def get_access_token():
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

token = get_access_token()

print(token)
