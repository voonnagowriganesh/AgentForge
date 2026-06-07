from datetime import datetime


def current_time(time):

    result = datetime.now().isoformat()

    return {
        "success": True,
        "tool": "datetime",
        "result": result,
    }
