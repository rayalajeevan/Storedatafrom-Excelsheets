import schedule
import requests
import datetime
import socket
def schedule_request():
    print("started",datetime.datetime.now())
    ip=str(socket.gethostbyname(socket.gethostname()))
    try:
        data=requests.get("http://{ip}:7000/deleteautomate".format(ip=ip),timeout=1000)
        print(data.status_code)
        print("ended",datetime.datetime.now())
    except:
        print("ERROR")
schedule_request()    
sch=schedule.every(360).minutes.do(schedule_request)
while True:
    schedule.run_pending()
