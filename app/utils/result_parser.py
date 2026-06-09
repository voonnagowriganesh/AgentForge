# def extract_result(data):

#     if isinstance(data, dict):
#         return str(data.get("result", data))

#     return str(data)


def extract_result(data):

    if hasattr(data, "result"):
        return str(data.result)

    if isinstance(data, dict):
        return str(data.get("result", data))

    return str(data)
