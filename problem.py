# import pandas as pd

# amount=int(input('Enter Amount :'))
# currency=str(input('Enter Currency type:'))
# dict1={'Australia':83.5,'Eurozone':91.0,'United Kingdom':108.5,'United Arab Emirates':22.7}

# while amount>0:
#     if currency=='USD':
#         print(f'RS.{dict1['Australia']*amount}')
#         break
#     elif currency=='EUR':
#         print(f'RS.{dict1['Eurozone']*amount}')
#         break
#     elif currency=='GBP':
#         print(f'RS.{dict1['United Kingdom']*amount}')
#         break
#     elif currency=='AED':
#         print(f'RS.{dict1['United Arab Emirates']*amount}')
#         break



# import numpy as np

# array1=np.array([[1,2],[3,4]])

# print(array1*2)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.linear_model import LogisticRegression
# from sklearn.svm import SVC
# from xgboost import XGBClassifier
# from sklearn import metrics

# import warnings
# warnings.filterwarnings('ignore')
# import matplotlib.pyplot as plt
# import pandas as pd
# df = pd.read_csv('newpro/tesla.csv')

# print(df.head())

# print(df.shape)

# print(df.info())

# print(df.describe())

# plt.figure(figsize=(15,5))
# plt.plot(df['Close'])
# plt.title('Tesla Close price.', fontsize=15)
# plt.ylabel('Price in dollars.')
# plt.show()

# print(df.head())

# print(df[df['Close'] == df['Adj Close']].shape)

# df = df.drop(['Adj Close'], axis=1)

# print(df.head())

# print(df.isnull().sum())

# features = ['Open', 'High', 'Low', 'Close', 'Volume']

# plt.subplots(figsize=(20,10))

# for i, col in enumerate(features):
#   plt.subplot(2,3,i+1)
#   sb.distplot(df[col])
# plt.show()




# ID='ST20250'
# # print(ID[0:2])
# import numpy as np

# matric=np.random.randint(1,101,(6,6))
# print(matric)

# first question
# b=matric[1:6:2,0:5:2]
# print(b)
# x=np.where((b%2)==0)
# print(x)
# print(b[x].reshape(2,-1))

# second question
# matric_mean=np.mean(matric)
# x=np.where(matric > matric_mean)
# print(x)
# matric[x]=-1
# print(matric)
# y=0

# third question
# for x in range(6):
#     i=matric[x,::-1]
#     y+=i[x]

    
# print(y)

# fourth question

# descen=np.sort(matric)
# print(descen)
# print(descen[0:6,::-1])

# print(matric.reshape(3,12))

# fifth question

hours = np.array([12,15,14,13,100,16,15,14,13,14])

mean =np.mean(hours)
print(mean)

std =np.std(hours)
print(std)

z_scores = (hours-mean)/std

print(z_scores)

outlier = np.where(np.abs(z_scores) > 2)

print(outlier)
print(hours[outlier])

print(np.abs(z_scores) <= 2)
cleaned_data = hours[np.abs(z_scores) <=2]
print(cleaned_data)

# sixth question
# data = np.array([
#     [85,78,np.nan],
#     [90,np.nan,88],
#     [np.nan,80,85],
#     [70,75,80]
# ])

# col_mean = np.nanmean(data,axis=0)

# print(col_mean)

# inds = np.where(np.isnan(data))

# print(inds)

# data[inds] = np.take(col_mean,inds[1])

# print(data)


# print('seventh question')

# scores = np.array([45,67,89,32,56,38,91,73,29,61])

# pass_student = scores >= 50

# fail_student = scores < 50
# print(pass_student)
# print(fail_student)

# total_pass = scores[pass_student]

# total_fail = scores[fail_student]

# print(total_pass)
# print(total_fail)

# scores[fail_student] += 5

# print(scores)

# print('---ninth question---')

# data = np.array([
#     [5,8,4],
#     [6,7,3],
#     [8,6,6],
#     [4,9,2],
#     [7,5,5]
# ])

# max_col = np.max(data,axis=0)

# min_col = np.min(data,axis=0)

# print(max_col)
# print(min_col)

# x_scaled = (data-min_col)/(max_col-min_col)

# print(x_scaled)

# print('tenth question --- ')

# marks_10th = np.array([75,88,95,62,70])

# marks_12th = np.array([400,420,380,460,410])

# max_10th = np.max(marks_10th)
# max_12th = np.max(marks_12th)

# print(max_10th)
# print(max_12th)

# min_10th = np.min(marks_10th)
# min_12th = np.min(marks_12th)

# print(min_10th)
# print(min_12th)

# norm_10th = (marks_10th-min_10th)/(max_10th-min_10th)
# norm_12th = (marks_12th-min_12th)/(max_12th-min_10th)

# print(norm_10th)
# print(norm_12th)

# print(np.stack((norm_10th,norm_12th),axis=1))
import pandas as pd

# data =  pd.read_csv('newpro/tesla.csv')

# print(data.info())

# print(data.isnull().sum())

# print(data.isnull().sum()/len(data)*100)

# import missingno as msno

# msno.matrix(data)
# print(msno.matrix(data))
# msno.heatmap(data)
# print(msno.heatmap(data))

# data_cleaned = data.dropna()
# print(data_cleaned.isnull().sum())
# print(data_cleaned)
# print(data)

# # data['Close'].fillna(data['Close'].mean(),inplace=True)

# print(data)
# data.fillna(method='bfill',inplace=True)

# print(data)

# data.to_csv('newpro/tesla.csv',index=False)

# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# # Create sample data with missing values
# data = {
# 'Name': ['John', 'Anna', 'Peter', 'Linda'],
# 'Age': [28, None, 34, 29],
# 'City': ['Delhi', 'Mumbai', None, 'Bangalore'],
# 'Salary': [50000, 60000, None, 45000]
# }
# df = pd.DataFrame(data)
# print("Original DataFrame:")
# print(df)
# # Check missing values
# print("\nMissing values per column:")
# print(df.isnull().sum())
# # Visualize missing values
# plt.figure(figsize=(10, 6))
# sns.heatmap(df.isnull(), cbar=False, yticklabels=False,
# cmap='viridis')
# plt.title('Missing Value Heatmap')
# plt.tight_layout()
# # Apply different imputation strategies
# # Mean imputation for Age
# df['Age'].fillna(df['Age'].mean(), inplace=True)
# # Mode imputation for City
# df['City'].fillna(df['City'].mode()[0], inplace=True)
# # Forward fill for Salary
# df['Salary'].fillna(method='ffill', inplace=True)
# print("\nDataFrame after imputation:")
# print(df)

# import pandas as pd
# # Create example dataframe with duplicates
# data = {
# 'Name': ['Raj', 'Priya', 'Raj', 'Amit', 'Priya'],
# 'Age': [28, 22, 28, 30, 22],
# 'City': ['Mumbai', 'Delhi', 'Mumbai', 'Kolkata', 'Delhi']
# }
# df = pd.DataFrame(data)
# print("Original DataFrame:")
# print(df)
# # Check for duplicate rows
# print("\nDuplicate rows:")
# print(df.duplicated())
# # Get count of duplicates
# print(f"\nTotal duplicates: {df.duplicated().sum()}")
# # Remove duplicates
# df_clean = df.drop_duplicates()
# print("\nDataFrame after removing duplicates:")
# print(df_clean)
# # Remove duplicates based on specific columns
# df_clean_subset = df.drop_duplicates(
# subset=['Name', 'City'])
# print("\nDataFrame after removing duplicates by Name and City:")
# print(df_clean_subset)
# # Keep last duplicate instead of first
# df_clean_last = df.drop_duplicates(keep='last')
# print("\nKeeping last occurrence:")
# print(df_clean_last)


import numpy as np


# students = np.array([
#         [80,85],
#         [78,82],
#         [65,60],
#         [90,88]
#     ])

# n = students.shape[0]
# print(n)

# dist_matrix = np.zeros((n,n))

# print(dist_matrix)

# for i in range(n):
#     for j in range(n):
#         dist = np.linalg.norm(students[i]-students[j])
#         print(i,j)
#         print(dist)
#         dist_matrix[i,j] = round(dist,2)


# print(dist_matrix)

# scores = np.array([45,23,67,89,38,40,75,19])

# fail =  np.where(scores < 40)

# scores[fail] = 0

# passed = np.where(scores >= 40)

# scores[passed] = 1

# print(scores)
# passes=sum(scores)
# fail = len(scores)-passes

# print(passes)
# print(fail)
# print(passes/len(scores)*100)

# data =  np.array([
#     [80,7.5],
#     [60,8.0],
#     [90,9.2],
#     [45,6.5],
#     [75,7.8]
# ])

# max_value =  np.max(data,axis=0)
# print(max_value)

# min_value =  np.min(data,axis=0)
# print(min_value)

# normalised = (data-min_value)/(max_value-min_value)

# print(np.round(normalised,3))


# departments =  np.array(['CS','IT','CS','ECE','ME','IT','ME'])

# x = np.unique(departments)
# value = 0
# for i in x:
#     new = np.where( departments == i )
#     departments[new] = int(value)
#     value+=1

# print(np.array(departments,dtype='int'))

# data = np.array(
#     [
#         [160,58],[170,67],[180,80],[155,50],[165,60]
#     ]
# )

# length =  data.shape[0]

# query =  np.array([168,65])

# dis_matrix =  np.zeros((length))

# print(dis_matrix)

# for i in range (length) :
#     dis = np.linalg.norm(data[i]-query)

#     dis_matrix[i] = round(dis,2)

# print(dis_matrix)

# min_value =  np.min(dis_matrix)

# index = np.where( dis_matrix==min_value)

# print(min_value)
# print(index)
# print(data[index])

# max_value =  np.max(data,axis=0)
# min_value = np.min(data,axis=0)

# print(max_value)
# print(min_value)

# normalized =  (data-min_value)/(max_value-min_value)

# print(normalized)

# student = (np.where(normalized[:,0] > 0.5)) and (np.where(normalized[:,1] > 0.5))

# print(normalized[student])


# data =np.array([
#     [160,58,0],[170,67,1],[180,80,1],[165,60,0]
# ])

# query = np.array([168,65])

# x =  data[:,0:2]

# y =  data[:,2]

# print(x)
# print(y)

# dis = np.linalg.norm(x-query,axis=1)
# print(dis)

# min_values =  np.argsort(dis)[:3]

# print(y[min_values])

# prediction = np.round(np.mean(y[min_values]).astype(int))

# print(prediction)
# print(np.mean(y[min_values]))

data = np.array([
    ['male','BCA'],['female','BSC'],['male','BSC'],['female','BCA'],['male','BCA']
])

x = (np.where( data[:,0] == 'male',0,1 ))
y = (np.where(data[:,1] == 'BCA',1,0))

print(np.stack((x,y),axis=1))









