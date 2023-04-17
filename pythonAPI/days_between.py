from datetime import datetime, date

def days_between(d1, d2):
    if d1 == '':
        d1= date.today()
        d1 = str(d1)
    if d2 == '':
        d2 = d1
    
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)