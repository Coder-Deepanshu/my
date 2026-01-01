from datetime import datetime

now = datetime.now()

current_date = now.date()
current_time = now.time()

time = datetime.strptime('12:56:39.000000', '%H:%M:%S.%f')
current_time = datetime.strptime(str(current_time), '%H:%M:%S.%f')
diff = current_time - time

data = str(current_date)+ '&' + str(current_time)

print(data)
print(int(diff.total_seconds()))