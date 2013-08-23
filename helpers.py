"""
helpers.py

author: erich@emfeld.com
========================

This file acts as the globally used function holder.
It is advised that you define your global functions here.

"""

import uuid
import base64

def generate_key():
    """
    generates a uuid, encodes it with base32 and strips it's padding.
    this reduces the string size from 32 to 26 chars.
    """
    return base64.b32encode(uuid.uuid4().bytes).strip('=').lower()


# end of file