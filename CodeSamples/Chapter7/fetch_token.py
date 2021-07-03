# fetch_token.py
import requests

TOKENDEALER_SERVER = "http://localhost:5000"
SECRET = "f0fdeb1f1584fd5431c4250b2e859457"


def get_token():
    data = {
        "client_id": "worker1",
        "client_secret": secret,
        "audience": "jeeves.domain",
        "grant_type": "client_credentials",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    url = tokendealer_server + "/oauth/token"
    response = requests.post(url, data=data, headers=headers)
    return response.json()["access_token"]


def verify_token(token):
    url = tokendealer_server + "/verify_token"
    response = requests.post(
        url, data={"access_token": token, "audience": "jeeves.domain"}
    )
    return response.json()


if __name__ == "__main__":
    token = get_token()
    print(token)
    print(verify_token(token))
