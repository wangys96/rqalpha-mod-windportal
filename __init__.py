import click
from rqalpha import cli


__config__ = {
    "wind_id": "windquery",
    "wind_password":"wind2010query",
    "wind_address":"10.35.64.39:1521/winddb",
}

def load_mod():
    from .mod import WindMod
    return WindMod()
