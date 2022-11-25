def getUniqueId(event):
    return event['day'] + '-' + event['title']

def getEvent(uniqueId: str):
    day, title = uniqueId.split('-')
    return {'day': day, 'title': title}