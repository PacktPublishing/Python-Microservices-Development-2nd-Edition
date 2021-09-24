ACTION_MAP = {
    "help": show_help_text,
    "weather": weather_action,
    "config": user_config,
    "get location": show_location,
    # TODO: Give the user a link to their profile on the web, for oauth.
    # "login": direct_user_to_web,
    # "signin": direct_user_to_web,
}

OUTGOING_MAP = {"slack": post_to_slack}


async def show_help_text(message, metadata):
    return "This is some help text"


async def process_message(message, metadata):
    """Decide on an action for a chat message.

    Arguments:
        message (str): The body of the chat message
        metadata (dict): Data about who sent the message,
              the time and channel.
    """
    reply = None

    for test, action in ACTION_MAP.items():
        if message.startswith(test):
            reply = await action(message.lstrip(test), metadata)
            break

    if reply:
        post_to_slack(reply, metadata)


async def extract_location(text):
    return text.replace("weather", "").replace("in", "").strip()


async def fetch_user_location(slack_id):
    user = db.session.query(User).filter(User.slack_id == slack_id).first()
    return user.location


async def weather_action(text, metadata):
    potential_location = extract_location(text)
    if not potential_location:
        potential_location = fetch_user_location(metadata["sender"])
    if potential_location:
        await process_weather_action(potential_location, metadata)
    else:
        await send_response("I don't know where you are", metadata)


async def process_weather_action(location, metadata):
    reply = await fetch_weather(location)
    await send_response(reply, metadata)
