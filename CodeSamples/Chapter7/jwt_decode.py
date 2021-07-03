import base64


def decode(data):
    # adding extra = for padding if needed
    pad = len(data) % 4
    if pad > 0:
        data += "=" * (4 - pad)
    return base64.urlsafe_b64decode(data)
