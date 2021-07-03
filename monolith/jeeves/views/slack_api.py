import logging

from quart import Blueprint, request

from jeeves.controller.message_router import process_message

# Respond to the SlackBot setup challenge

slack_api = Blueprint("api", __name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def respond_to_slack_challenge(incoming_challenge):
    return incoming_challenge.get("challenge", ""), 200


def extract_slack_text(request_body):
    # Deep JSON structure
    elements = request_body["event"]["blocks"][0]["elements"][0]["elements"]
    for part in elements:
        if part["type"] == "text":
            return part["text"].lstrip()
    # fallback to full text + replace so that
    # <some user id> some text
    # becomes:
    # some text
    return request_body["event"]["text"].partition(">")[2].lstrip()


def outgoing_metadata(request_body):
    return {
        "type": "slack",
        "message_type": request_body["event"]["type"],
        "team": request_body["event"]["team"],
        "sender": request_body["event"]["user"],
        "channel": request_body["event"]["channel"],
        "ts": request_body["event"]["ts"],  # used for replies
    }


@slack_api.route("/slack", methods=["POST"])
async def incoming_slack_endpoint():
    """Receive an event from Slack."""

    request_body = await request.get_json()

    # When setting up a Slack app, we are sent a verification
    # challenge, and we must respond with the token provided.
    if request_body.get("type", "") == "url_verification":
        logger.info("Responding to url verification challenge")
        return respond_to_slack_challenge(request_body)

    logger.debug("Received message: %s", extract_slack_text(request_body))
    await process_message(
        extract_slack_text(request_body), outgoing_metadata(request_body)
    )

    # Slack ignores the data here, but a value may help our debugging.
    return {"status": "OK"}, 200
