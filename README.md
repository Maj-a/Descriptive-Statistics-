# Descriptive Statistics
In this section, we explore the data by calculating basic statistics such as the mean, median, mode, and variance. We also check for any outliers. This helps us gain a deeper understanding of the dataset and provides a comprehensive summary.

## Background:
The data for analysis is a Glassdoor Gender Pay Gap in which base pay information is provided for each employee for all the roles and departments.

Link to the data set as accessed on the 04.07.2024: https://www.kaggle.com/datasets/nilimajauhari/glassdoor-analyze-gender-pay-gap/data 
(The reason why the link has not been provided as a hyperlink is to be transparent about the source of the data & security.)

## Here's what we'll explore in this project: 

1. **Import the Data:** We’ll begin by bringing in the Gender Pay Gap data.
2. **Mode Discovery:** We'll find the most common job titles across each department.
3. **Visualize with Box-Whisker Plots:** We’ll use box-whisker plots to explore BasePay.
4. **Spot Outliers:** Let’s check for outliers using the Boxplot() function from the 'car' package.
5. **Skewness and Kurtosis:** We’ll examine the skewness and kurtosis of BasePay.
6. **Scatter Plot Exploration:** We’ll create a scatter plot to see the relationship between BasePay and Age.
7. **Correlation Check:** Finally, we’ll calculate and interpret the correlation between BasePay and Age.
   
## Ready to dive in? Just keep scrolling!

### 0. Importing packages and libraries:

install.packages("car")
library("car")
library(e1071)
library(dplyr)
library(ggplot2)
library(scales)

###  1. Importing Glassdoor Gender Pay Gap data.

'GGPG_data<-read.csv(file.choose(),header=TRUE)'

'dim(GGPG_data)'

![image](https://github.com/user-attachments/assets/fab5dc2f-f5e5-4a3c-9447-52ae4f621661)

'head(GGPG_data)'

'str(GGPG_data)'

'summary(GGPG_data)'

![image](https://github.com/user-attachments/assets/42d2d85c-cfe4-4fe4-ad5b-8608f1894c1b)

###  2. Obtain the Mode for the count of job titles available across each Department. 

'JobTitles_per_Dep<-GGPG_data%>%
  group_by(Dept, JobTitle)%>%
  summarize(JobTitleCount=n())%>%
  filter(JobTitleCount==max(JobTitleCount))'
'JobTitles_per_Dep'

#### Calculating/ coding with length() instead of n():

'JobTitles_per_Dep2<-GGPG_data%>%
  group_by(Dept, JobTitle)%>%
  summarize(JobTitleCount=length(JobTitle))%>%
  filter(JobTitleCount==max(JobTitleCount))'
'JobTitles_per_Dep2'


![image](https://github.com/user-attachments/assets/39190f92-3536-4888-b1c2-d1eed5a1daeb)



###  3. Obtain box-whisker plots for Base Pay by Department.

'boxplot(BasePay~Dept, data=GGPG_data,
        col=c("springgreen", "pink2","red3", "royalblue","violetred"),
        main = "Box-whisker plots for BasePay by Department")'


![image](https://github.com/user-attachments/assets/ea959bc0-cf7c-4816-97bd-8dde9f5dbff1)

        

## Boxplot with ggplot & scale function
'ggplot(GGPG_data, aes(x = Dept, y = BasePay)) +
  geom_boxplot(col = c("springgreen", "pink2", "red3", "royalblue", "violetred")) +
  scale_y_continuous(labels = scales::comma_format()) + 
  labs(x = "Department", y = "Base Pay", title = "Box-whisker plots for Base Pay by Department") +
  theme_light()'  


![image](https://github.com/user-attachments/assets/a0b1fdb3-6b9a-4e19-b2e4-f13b57141fd1)



###  4. Detect outliers if present. Hint: use Boxplot() function of ‘car’ Package

'box<-boxplot(BasePay~Dept, data=GGPG_data)'

# calculating outliers
box$out
no_outliers<-length(box$out)
no_outliers

# another method -  dplyr & Inter Range Quantile(IQR)

outliers_list1 <- GGPG_data %>%
  group_by(Dept) %>%
  summarize(outliers = {
    Q1 <- quantile(BasePay, 0.25)
    Q3 <- quantile(BasePay, 0.75)
    IQR <- Q3 - Q1
    threshold <- 1.5
    lower_bound <- Q1 - threshold * IQR
    upper_bound <- Q3 + threshold * IQR
    outliers <- BasePay[BasePay < lower_bound | BasePay > upper_bound]
    list(outliers)
  })
outliers_list1
###--> Both methods show that there are three outliers, one in Administration department, one in Management
###    and one in Sales department. 

###  5. Find skewness and kurtosis of BasePay amount.

skewness(GGPG_data$BasePay, na.rm=T, type=2)

# Plotting a histogram 1
ggplot(GGPG_data, aes(x = BasePay)) +
  geom_histogram(binwidth = 50) +
  labs(x = "Billing Amount", y = "Frequency", title = "Distribution of Billing Amount by Insurance Provider")

# Plotting a histogram 2
hist(GGPG_data$BasePay, 
     main = "Histogram of Base Pay", 
     xlab = "Base Pay", 
     ylab = "Frequency", 
     col = "skyblue", 
     border = "black")

# --> The skewness value you obtained is 0.166472, indicating a mild positive skew. 
#     This suggests that while most of the BasePay values are clustered around the 
#     lower end of the scale, there are some higher values that are pulling the 
#     distribution slightly to the right. Overall, the distribution is relatively close 
#     to normal but with a slight rightward tilt.


###  6. Draw a scatter plot of Base Pay and Age. 

plot(GGPG_data$BasePay, GGPG_data$Age, col="red3",
     main="Scatter Plot of Base Pay vs Age")

# Below is same scatter plot completed with ggplot
ggplot(GGPG_data, aes(x=BasePay, y=Age)) + 
  geom_point(col="pink3") +
  geom_smooth(method = "lm", col = "blue")+
  labs(x = "Base Pay", y = "Age", title = "Scatter Plot of Base Pay vs Age with Trend Line")

# Hexbin graph (typically dedicated for large datasets, here just as a test)
install.packages("hexbin")
library(hexbin)
ggplot(GGPG_data, aes(x=BasePay, y=Age)) + 
  geom_hex(bins=30) +
  labs(x = "Base Pay", y = "Age", title = "Hexbin Plot of Base Pay vs Age") +
  scale_fill_continuous(type = "viridis")  # Color scale

# 2D graph: 
ggplot(GGPG_data, aes(x=BasePay, y=Age)) + 
  geom_point(col="pink3", alpha=0.2) + 
  geom_density_2d() +
  labs(x = "Base Pay", y = "Age", title = "2D Density Plot of Base Pay vs Age")

# All four graphs, plain scatter plot, plot with trend line,  the hexbin and 2D plot,all show positive correlation 
# between the base pay and the age. The upward sloped trend line,shows that 
# the relationship between base pay and age is moderate. 


### 7.  Find the correlation coefficient between Premium and Vintage period and interpret the value.

round(cor(GGPG_data$BasePay, GGPG_data$Age), 3)

##### --> Observation: Pearson Correlation Coefficient = 0.563 
##### The positive value of 0.563 indicates that as the age of employees increases, 
##### their base pay tends to increase as well, although the relationship is not perfect or 
##### linear. The correlation is strong enough to suggest a meaningful relationship,
##### but it also implies that other factors could influence base pay, and there is still 
##### variability not explained by age alone.
