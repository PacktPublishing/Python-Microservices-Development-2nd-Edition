from jeeves.database import User, db

CONFIG_CMDS = [
    "get",
    "set",
    "show",
]


def set_config(label, value):
    pass


async def fetch_user(metadata):
    user = db.session.query(User).filter(User.slack_id == metadata["sender"]).first()
    if user is None:
        user = User()
        user.is_admin = False
        user.slack_id = metadata["sender"]
        db.session.add(user)
        db.session.commit()
        user = (
            db.session.query(User).filter(User.slack_id == metadata["sender"]).first()
        )

    return user


async def show_location(message, metadata):
    user = await fetch_user(metadata)
    if user.location:
        return f"You are in {user.location}"
    else:
        return "I don't know where you are."


async def user_config(message, metadata):
    print(message)
    print(metadata)
    operation = message.split()[0].lstrip()
    print(f"operation {operation}")
    if operation not in CONFIG_CMDS:
        return f"I don't know what to do. Possible keywords: {CONFIG_CMDS}"

    user = await fetch_user(metadata)

    if operation == "show":
        reply = ""
        if not user.config:
            return "No config values found!"
        print(user.config)
        for k, v in user.config.items():
            reply += f"{k}: {v}\n"
        print(f"Returning {reply}")
        return reply
    if operation == "set":
        label, value = message.split(maxsplit=2)[1:]
        if user.config:
            new_config = dict(user.config)
        else:
            new_config = {}
        new_config.update({label: value})
        user.config = new_config
        db.session.commit()
        reply = f"Set {label} to {value}"
        print(f"Returning {reply}")
        return reply
