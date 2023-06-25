import sys
import traceback


def get_traceback():
    return "".join(traceback.format_exception(*sys.exc_info()))
