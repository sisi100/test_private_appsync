def getUsers(arguments):
    return [{"id": "hogehoge", "name": "hogehoge"}]


def handler(event, context):
    return globals()[event["info"]["fieldName"]](event["arguments"])
