import datetime

now = datetime.datetime.now()
epoch = now.timestamp()
print(now.timestamp())
now2 = datetime.datetime.fromtimestamp(epoch)
print(now)
print(now2)
