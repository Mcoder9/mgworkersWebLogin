from datetime import datetime

def days_between(today, expirydate):
    d1 = datetime.strptime(today, "%d-%m-%Y")
    d2 = datetime.strptime(expirydate, "%d-%m-%Y")
    
    if d1>=d2:
        return 'Expired'
    else:
        return "Not Expire"

rem = days_between('11-04-2022','15-03-2022')

print(rem)