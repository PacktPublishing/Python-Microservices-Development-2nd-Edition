import requests
from quart import current_app


def post_to_slack(message, metadata):
    print(f"post_to_slack {message}")
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['SLACK_TOKEN']}",
    }
    print(f"headers {headers}")
    print(metadata)
    response = requests.post(
        current_app.config["SLACK_POST_URL"],
        json={
            "token": current_app.config["SLACK_TOKEN"],
            "text": message,
            "channel": metadata["channel"],
        },
        headers=headers,
    )
    response.raise_for_status()
