from uuid import uuid4

def getEventId(event):
    return event['day'] + '-' + event['title']

def getEvent(uniqueId: str, ts: str):
    day, title = uniqueId.split('-')
    return {'day': day, 'title': title, 'ts': ts}

def genUniqueId():
    return str(uuid4())