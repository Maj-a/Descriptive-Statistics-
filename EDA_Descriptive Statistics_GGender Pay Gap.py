# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 19:55:25 2024

@author: Maja
"""

########    Descriptive Statistics 

#####    QUESTIONS 


# 0) Import libraries
import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import skew
import matplotlib.pyplot as plt
import seaborn as sns

### 1) Importing Glassdoor Gender Pay Gap data.

GGPG_data = pd.read_csv("C:/Users/Maja/Documents/Learning/MS_Projects/Portfolio 2024/GitHub Portfolio/3_ Descriptive Statistics/Glassdoor Gender Pay Gap.csv")
print("Head of GGPG_data:", GGPG_data.head(n=20))
print("Dimension of GGPG_data: ",GGPG_data.shape)
print(GGPG_data.info)
print(list(GGPG_data))
# Check column names
print("Columns in GGPG_data DataFrame:", GGPG_data.columns)

### 2)  Obtain the Mode for the count of job titles available across each Department. 
 

# Group by Department and find the mode for Job Title
JobTitles_per_Dep = (GGPG_data
                                  .groupby('Dept')['JobTitle']
                                  .apply(lambda x: x.mode().iloc[0] if not x.mode().empty else None))

# Convert the result to a DataFrame for better readability
JobTitles_per_Dep = JobTitles_per_Dep.reset_index()

# Print the result
print("Most frequent job title department:", JobTitles_per_Dep)

### 3) Obtain box-whisker plots for Base Pay by Department. 

# Createing the box-whisker plot for Base Pay
GGPG_data.boxplot(column='BasePay')

# Adding labels and title
plt.xlabel('')
plt.ylabel('Values')
plt.title('Box-whisker Plot of Base Pay')

# Show the plot
plt.show()
# Createing the box-whisker plot for Base Pay by Department
# Create a box-whisker plot using seaborn
plt.figure(figsize=(10, 6))
sns.boxplot(x='Dept', y='BasePay', data=GGPG_data, palette="Set2")

# Adding labels and title
plt.xlabel('Dept')
plt.ylabel('BasePay')
plt.title('Box-Whisker Plot of Base Pay by Department')

# Show the plot
plt.show()


### 4) Detect outliers if present. Hint: use Boxplot() function of ‘car’ Package

# Calculate Q1 and Q3
Q1 = GGPG_data['BasePay'].quantile(0.25)
print("Q1 is ", Q1)
Q3 = GGPG_data['BasePay'].quantile(0.75)
print("Q3 is", Q3)

# Calculate IQR
IQR = Q3 - Q1
print("IQR is", IQR)

# Define upper and lower bounds
Upper_bound = Q3 + 1.5 * IQR
print("Upper bound", Upper_bound)
Lower_bound = Q1 - 1.5 * IQR
print("Lower bound",Lower_bound)

# Identify outliers
outliers = GGPG_data[(GGPG_data['BasePay'] < Lower_bound) | (GGPG_data['BasePay'] > Upper_bound)]

# Print outliers
print("Outliers:")
print(outliers)

### 5) Find skewness and kurtosis of Base Pay.

skewness_BasePay = stats.skew(GGPG_data['BasePay'])
print(f"Skewness for Base Pay is: {skewness_BasePay:.3f}")

# --> The skewness value you obtained is 0.166, indicating a mild positive skew. 
#     This suggests that while most of the BasePay values are clustered around the 
#     lower end of the scale, there are some higher values that are pulling the 
#     distribution slightly to the right. Overall, the distribution is relatively close 
#     to normal but with a slight rightward tilt.


# Grouping the data by 'Dept' and calculating skewness for 'Base Pay'
skewness_by_provider = GGPG_data.groupby('Dept')['BasePay'].apply(lambda x: skew(x.dropna()))

# Converting the result to a DataFrame for better readability
skewness_by_provider_df = skewness_by_provider.reset_index()

# Printing the result
print(skewness_by_provider_df)

 
### 6) Draw a scatter plot of Base Pay and Age. 

plt.figure(figsize=(8, 6))
plt.scatter(GGPG_data['Age'], GGPG_data['BasePay'], color='blue', alpha=0.5)
plt.title('Base Pay vs. Age')
plt.xlabel('BasePay')
plt.ylabel('Age')
plt.grid(True)
plt.show()

# Because there are a lot of the data points, the graph is over plotting, 
# the points are overlapping, different approach will be taken.
# Create a hexbin plot
plt.figure(figsize=(10, 6))
plt.hexbin(GGPG_data['BasePay'], GGPG_data['Age'], gridsize=30, cmap='viridis', mincnt=1)
# Adding labels and title
plt.xlabel('BasePay')
plt.ylabel('Age')
plt.title('Hexbin Plot of Base Pay vs Age')
# Add a color bar
plt.colorbar(label='Count')
# Show the plot
plt.show()

# Create a 2D density plot with scatter points
plt.figure(figsize=(10, 6))
# Scatter plot with transparency
sns.scatterplot(x='BasePay', y='Age', data=GGPG_data, color='pink', alpha=0.2)
# 2D density plot
sns.kdeplot(x='BasePay', y='Age', data=GGPG_data, cmap='viridis', alpha=0.5)
# Adding labels and title
plt.xlabel('BasePay')
plt.ylabel('Age')
plt.title('2D Density Plot of Base Pay vs Age')
# Show the plot
plt.show()


### 7) Find the correlation coefficient between Base Pay and Age and interpret the value.
correlation_coefficient = GGPG_data['BasePay'].corr(GGPG_data['Age'])
print("Correlation coefficient value for Age and BasePay is ", correlation_coefficient.round(4))

##### --> Observation: Pearson Correlation Coefficient = 0.5627 
##### The positive value of 0.563 indicates that as the age of employees increases, 
##### their base pay tends to increase as well, although the relationship is not perfect or 
##### linear. The correlation is strong enough to suggest a meaningful relationship,
##### but it also implies that other factors could influence base pay, and there is still 
##### variability not explained by age alone.

