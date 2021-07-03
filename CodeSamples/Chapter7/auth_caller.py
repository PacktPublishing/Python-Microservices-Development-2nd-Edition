# auth_caller.py
_TOKEN = None


def get_auth_header(new=False):
    global _TOKEN
    if _TOKEN is None or new:
        _TOKEN = get_token()
    return "Bearer " + _TOKEN


_dataservice = "http://localhost:5001"


def _call_service(endpoint, token):
    # not using session and other tools, to simplify the code
    url = _dataservice + "/" + endpoint
    headers = {"Authorization": token}
    return requests.get(url, headers=headers)


def call_data_service(endpoint):
    token = get_auth_header()
    response = _call_service(endpoint, token)
    if response.status_code == 401:
        # the token might be revoked, let's try with a fresh one
        token = get_auth_header(new=True)
        response = _call_service(endpoint, token)
    return response
