import json


def parse_json_response(response: str):

    try:
        return json.loads(response)

    except Exception:

        start = response.find("{")
        end = response.rfind("}")

        if start != -1 and end != -1:

            try:
                return json.loads(response[start : end + 1])

            except Exception:
                pass

    return {}
