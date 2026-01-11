# from datetime import datetime

# now = datetime.now()

# current_date = now.date()
# current_time = now.time()

# time = datetime.strptime('12:56:39.000000', '%H:%M:%S.%f')
# current_time = datetime.strptime(str(current_time), '%H:%M:%S.%f')
# diff = current_time - time

# data = str(current_date)+ '&' + str(current_time)

# print(data)
# print(int(diff.total_seconds()))

# from datetime import datetime

# now = datetime.now()
# print(now.date())

# print(2.0 + 1)

# id = 'GK2026TR1'

# print(f"{id[0:8]}{int(id[8:])+1}")

list1 = []

for i in range(1,6):
    due = {}
    list1.append(due)

print(list1)

for i in list1:
    if len(i)!=0:
       print(i['amount'])
       print(i['amt'])