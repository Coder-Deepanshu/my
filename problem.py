# # import pandas as pd
# # a=[1,2,3]
# # m=pd.Series(a)
# # print(m)

# # #  for print any row of any index
# # print(m[0])

# # # for labling the index
# # m=pd.Series(a,index=['x','y','z'])
# # print(m)

# # print(m['x'])

# # # key/value object as series
# # b={'name':['rahul','mohan'],'address':['punjab','malikpur'],'class':['10th','11th']}
# # n=pd.Series(b)
# # print(n)

# # # for calling specific object from the dictionery
# # print(b['name'])

# # #  for calling multiple object from the dictionery, if object name does not exist in the dictionery it give none value
# # n=pd.Series(b,index=['name','address'])
# # print(n)

# # # for creating dataframe 
# # c={'name':['abhishek','rahul','mohan'],'age':[78,56,56],'address':['malikpur','karsan','mithapur']}
# # j=pd.DataFrame(c)
# # print(j)


# income=int(input('Enter your monthly income: $'))

# input(f"You have ${income} income for this month.")
# category={'food':[],'Transport':[],'Entertainment':[],'Bills':[]}
# a=category['food'] 
# b=category['Transport'] 
# c=category['Entertainment'] 
# d=category['Bills'] 
# #  for input (1/2/3)
# for i in range(100):
#     print("--Menu--" )
#     print("1.Add Expenses") 
#     print("2.View Summary" )
#     print("3.Exit")
#     option=int(input('Enter Option Number(1/2/3):'))
#     if option==1:
#         exp=int(input(f"Enter the Expenses Category(1.Food,2.Transport,3.Entertainment,4.Bills):"))
#         e1=int(input("Enter the amount of the Expenses: $"))
#         if exp==1:
#             category['food'].append(e1)
#         elif exp==2:
#             category['Transport'].append(e1)
#         elif exp==3:
#             category['Entertainment'].append(e1)
#         elif exp==4:
#             category['Bills'].append(e1)
#         elif exp==5:
#             category['Savings'].append(e1)
#     if option==2:
#         print(category['food'])
#         l1=200
#         l2=300
#         l3=200
#         l4=200
#         l5=600
#         len1=len(a)
#         len2=len(b)
#         len3=len(c)
#         len4=len(d)
#         if  len1!=0:
#             if a[0]>l1:
#                 print(f"alert: Your Food Expenses is ${a[0]-l1} more than ${l1}")
#             elif a[0]<l1:
#                 print(f"Congratualtions You Save ${l1-a[0]} from Food Expenses ${l1}")
#             else:
#                 print("Your Food Expenses is equal to budget")
#         else:
#             a[0]=0
#             print("Your Food Expenses is 0")
        
#         if  len2!=0:
#             if b[0]>l2:
#                 print(f"alert: Your Transport Expenses is ${a[0]-l2} more than ${l2}")
#             elif b[0]<l2:
#                 print(f"Congratualtions You Save ${l2-a[0]} from Transport Expenses ${l2}")
#             else:
#                 print("Your Transport Expenses is equal to budget")
#         else:
#             b[0]=0
#             print("Your Transport Expenses is 0")

#         if  len3!=0:
#             if c[0]>l3:
#                 print(f"alert: Your Entertainment Expenses is ${c[0]-l3} more than ${l3}")
#             elif c[0]<l3:
#                 print(f"Congratualtions You Save ${l3-c[0]} from Entertainment  Expenses ${l3}")
#             else:
#                 print("Your Entertainment  Expenses is equal to budget")
#         else:
#             c[0]=0
#             print("Your Entertainment  Expenses is 0")

#         if  len4!=0:
#             if d[0]>l4:
#                 print(f"alert: Your Bills Expenses is ${d[0]-l4} more than ${l4}")
#             elif d[0]<l4:
#                 print(f"Congratualtions You Save ${l4-d[0]} from Bills Expenses ${l4}")
#             else:
#                 print("Your Bills Expenses is equal to budget")
#         else:
#             d[0]=0
#             print("Your Bills Expenses is 0")

#         i=income-a[0]-b[0]-c[0]-d[0]
#         if  i!=0:
#             if i>l5:
#                 print(f"Congratualtion You Save is ${income-a[0]-b[0]-c[0]-d[0]-l5} more than ${l5}")
#             elif i<l5:
#                 print(f"alert Your Saving fall down ${l5-income-a[0]-b[0]-c[0]-d[0]} from ${l5}")
#             else:
#                 print("Your Saving is equal to budget")
#         else:
#             print("Your Saving is 0")

#     elif option==3:
#         break  
            
# income = int(input("Enter your income: $ "))
# printy = f"Your income is: $ {income} for this month."
# print(printy)

# print('--menu--')
# print('1. ADD Expense')
# print('2. View summary')
# print('3. Exit')

# choice = int(input('Enter your choice: '))
# if choice == 1:
#     expense = int(input("Enter the amount of the expense: $ "))
#     print(f"Your expense is: $ {expense} for this month.")
#     print(f"Enter your expense category: {'food', 'transport', 'entertainment', 'bills', 'savings'}: food")



# a='GK0'
# B=1

# c=int(a[2])+B
# print(c)

# print(a[0:2]+str(c))

import numpy as np

A=np.array([[4,-2],[1,1]])

eignvalue,eignvector=np.linalg.eig(A)

print(eignvalue)

print(eignvector)
        


        








