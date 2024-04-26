import pingparsing
import os
from dotenv import load_dotenv

load_dotenv()


def ping(address: str, ptype="uptime"):
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = address
    transmitter.count = os.getenv("PING_COUNT")
    result = transmitter.ping()
    print(ptype)
    if ptype == "uptime":
        ping_result = ping_parser.parse(result).as_dict()["rtt_min"]
        if ping_result is not None:
            return {"status": True}
        return {"status": False}
    elif ptype == "verbose":
        return ping_parser.parse(result).as_dict()


def init(args: str, ptype="uptime"):
    result = ping(args, ptype)
    return result
