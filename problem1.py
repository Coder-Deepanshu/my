# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# # Sample data with outliers
# data = np.array([20, 21, 19, 22, 500, 18, 23, 24, 40, 22])

# q1 = np.percentile(data,25) # <--------------------------------------------------------------------------->
# q3 = np.percentile(data,50)

# print('q1',q1)
# print('q3',q3)

# iqr =  q3-q1

# print(iqr)

# # define bounds

# lower_bound = q1 - 1.5*iqr
# upper_bound = q3 + 1.5*iqr

# print('lower bound :',lower_bound)
# print('upper bound :',upper_bound)

# outlier = [x for x in data if x<lower_bound or x>upper_bound]

# print(outlier)

# # plt.figure(figsize=(10, 6))
# # sns.boxplot(x=data)
# # plt.title("Boxplot Showing Outliers")
# # plt.show()

# filter_data = []

# for i in data : 
    
#     if i==500:
#         filter_data.append(False)
#     elif i==40:
#         filter_data.append(False)
#     else:
#         filter_data.append(True)

# print(data[filter_data])


# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# # Create a dataset with outliers
# np.random.seed(42)
# normal_data = np.random.normal(loc=50000, scale=10000,
# size=98)
# outliers = np.array([150000, 5000])
# salary_data = np.concatenate([normal_data, outliers])
# df = pd.DataFrame({
# 'EmployeeID': range(1, 101),
# 'Salary': salary_data
# })
# # Visualize the data
# plt.figure(figsize=(12, 6))
# plt.subplot(1, 2, 1)
# sns.histplot(df['Salary'], kde=True)
# plt.title('Salary Distribution with Outliers')
# plt.subplot(1, 2, 2)
# sns.boxplot(y=df['Salary'])
# plt.title('Boxplot of Salaries')
# plt.tight_layout()
# plt.show()

# # Detect outliers using IQR method
# q1 = df['Salary'].quantile(0.25)
# q3 = df['Salary'].quantile(0.75)
# iqr = q3 - q1
# lower_bound = q1 - 1.5 * iqr
# upper_bound = q3 + 1.5 * iqr
# # Identify outliers
# outliers_mask = (df['Salary'] < lower_bound) | (df['Salary'] >
# upper_bound)
# outliers_df = df[outliers_mask]
# print(f"Detected {len(outliers_df)} outliers:")
# print(outliers_df)
# # Apply different outlier treatments and compare
# # 1. Remove outliers
# df_removed = df[~outliers_mask].copy()
# # 2. Cap outliers
# df_capped = df.copy()
# df_capped['Salary'] = np.where(
# df_capped['Salary'] > upper_bound,
# upper_bound,
# np.where(
# df_capped['Salary'] < lower_bound,
# lower_bound,
# df_capped['Salary']
# )
# )
# # 3. Transform data
# df_transformed = df.copy()
# df_transformed['Salary_Log'] = np.log1p(df_transformed['Salary'])
# # Compare statistics
# print("\nOriginal Data Statistics:")
# print(df['Salary'].describe())
# print("\nAfter Removing Outliers:")
# print(df_removed['Salary'].describe())
# print("\nAfter Capping Outliers:")
# print(df_capped['Salary'].describe())
# print("\nLog-Transformed Data:")
# print(df_transformed['Salary_Log'].describe())
# import numpy as np

# marks = [55,57,60,62,65,67,69,70,71,73,75,78,80,82,85,150]

# q1 = np.percentile(marks,25)

# q3 =  np.percentile(marks,75)

# print('q1',q1)
# print('q3',q3)

# iqr = q3-q1
# print('iqr',iqr)

# lower_bound = q1-1.5*iqr
# upper_bound = q3+1.5*iqr
# print('lower bound',lower_bound)
# print('upper bound',upper_bound)

# outlier = [x for x in marks if x<lower_bound or x>upper_bound]

# print(outlier)

import numpy as np
import pandas as pd

np.random.seed(42)
salaries = np.random.normal(loc=50000,scale=8000,size=10000)

salaries[100] = np.nan
salaries[500] = np.nan

salaries = np.append(salaries,[45000,55000,45000])

salaries[9000] = 999999
salaries[9500] = 888888

df = pd.DataFrame({'Salary':salaries})

# print(df.head())

# print(df.info())

# print(df.isnull().sum())

df.dropna(inplace=True)

# print(df.isnull().sum())

# print(df.duplicated().sum())

df.drop_duplicates(inplace=True)

# print(df.duplicated().sum())
df['Salary'] =np.unique(df['Salary'])
q1 = np.percentile(df['Salary'],25)
q3 = np.percentile(df['Salary'],75)

iqr = q3-q1

lower_bound = q1 - 1.5*iqr
upper_bound = q3 + 1.5*iqr

print(lower_bound)
print(upper_bound)
outlier = df[(df['Salary']<lower_bound) | (df['Salary']>upper_bound)]

print(outlier.head(20))












            






