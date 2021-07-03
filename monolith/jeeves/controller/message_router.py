from jeeves.actions.misc import do_the_thing
from jeeves.actions.user import user_config, show_location
from jeeves.actions.weather import weather_action
from jeeves.outgoing.default import default_outgoing
from jeeves.actions.help import show_help_text
from jeeves.outgoing.slack import post_to_slack

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


async def process_message(message, metadata):
    """Decide on an action for a chat message.

    Arguments:
        message (str): The body of the chat message
        metadata (dict): Data about who sent the message,
              the time and channel.
    """
    reply = None

    print(f"In process message with '{message}'")
    for test, action in ACTION_MAP.items():
        if message.startswith(test):
            print(f"Working on {test}")
            reply = await action(message.lstrip(test), metadata)
            break

    if reply:
        post_to_slack(reply, metadata)

    """ If we have different response routes, we can use this method
    OUTGOING_MAP.get(metadata["type"], default_outgoing)(
        reply,
        metadata,
    )
    """
