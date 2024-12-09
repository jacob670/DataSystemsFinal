"""
Analyzing and interepting Olympic Swimming History data. Performed data inspection and clean up, aggregations, cross tabulation, logarithmic regression, and created data visualizations
The dataset can be found here: https://www.kaggle.com/datasets/datasciencedonut/olympic-swimming-1912-to-2020?resource=download
Jacob Esteves, Cimi Halilaj, Owen Rogonjic
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

swimming_data = pd.read_csv('Olympic_Swimming_Results_1912to2020.csv')

"""
================== INITIAL DATA INSPECTION ==================
"""

# What are the data types of each column listed?
data_types = swimming_data.dtypes
# Integers: Year, Relay, Rank
# Strings/Objects: Location, Distance, Stroke, Gender, Team, Athlete, Results


# How many rows and columns are in the dataset?
num_columns = len(swimming_data.columns)
num_rows = len(swimming_data.index) 
# There are 10 columns and 4359 rows


# What are the names of the columns?
column_names = swimming_data.columns
# Names: Location, Year, Distance (in meters), Stroker, Relay?, Gender, Team, Athlete, Results, Rank


# Does the set contain null values? If there are null values, where are they located? 
null_values = swimming_data.isnull().sum()
# There are 14 null values in the Athlete column, and 28 null values in the Results column
null_athlete_values = swimming_data.loc[swimming_data['Athlete'].isnull()]
null_result_values = swimming_data.loc[swimming_data['Results'].isnull()]
# Displays the actual rows that contain null values -> displayed as 'nan' 


# How many unique values are in the data set
unique_values = swimming_data.nunique()
# Unique Values: 22 locations, 25 years, 8 distances, 6 strokes, 2 Relay? column, 2 unique genders, 87 teams, 2,821 athletes, 3,635 results, and 6 ranks.


# What are the first 5 rows of this Olympic swimming dataset?
head_values = swimming_data.head()
# Results from the men's 100 meter backstroke in Tokyo at the 2020 Olympics.


# How many different Countries have medals?
medal_list = [1,2,3]
unique_teams = swimming_data[swimming_data['Rank'].isin(medal_list)]
num_unique_medals = unique_teams['Team'].nunique()
# There are 60 Countries with medals in the dataset.


# What are the number of male athletes in the dataset?
male_athletes = swimming_data[swimming_data['Gender'] == 'Men']
unique_male_athletes = male_athletes['Athlete'].nunique()
# There are 1504 male athletes in this dataset






"""
================== DATA CLEANUP ==================
"""

"""
Switch the rows with Rank 0 to 5 and Rank 5 to 6. New correlations are shown below
1 -> Gold
2 -> Silver
3 -> Bronze
4 -> No Medal
5 -> DNS/DNF or Disqualified
6 -> No Data
"""
swimming_data.loc[swimming_data['Rank'] == 5, 'Rank'] = 6
swimming_data.loc[swimming_data['Rank'] == 0, 'Rank'] = 5


# Rename the Team column to 'Country' in order for clarification
swimming_data.rename(columns={"Team": "Country"}, inplace=True)


# Fix the data, where nan/null values appear
# Add 0 to results in order to perform calculations, and switch the athlete name to 'No Name'
swimming_data.loc[swimming_data["Athlete"].isnull(), "Athlete"] = "No Name"
swimming_data.loc[swimming_data["Results"].isnull(), "Results"] = 0


# Add a string version of 'Rank' column in order for data to be more readable
rank_medal_mapping = {
    1: 'Gold',
    2: 'Silver',
    3: 'Bronze',
    4: 'No Medal',
    5: 'DNS/DNF or Disqualified',
    6: 'No Data'
    }

swimming_data['Medal?'] = swimming_data['Rank'].map(rank_medal_mapping)
            

# Swap the Relay column with string values instead of boolean logic; Makes it more readable again
relay_mapping = {
    0: 'Individual',
    1: 'Relay'
    }

title_switch_mapping = {
    'Relay?': 'Race Format'
    }

swimming_data['Relay?'] = swimming_data['Relay?'].map(relay_mapping)
swimming_data.rename(columns=title_switch_mapping, inplace=True)


# Creates Event column to potray proper swimming terminology and allows for data anaylsis techniques
swimming_data['Event'] = swimming_data['Distance (in meters)'] + " " + swimming_data['Stroke']


# Convert Distance column into an integer column to allow calculations
def convert_values(distance):
    """ if the distance contains x, split the string and mutiply the values to return the total distance for relays
        otherwise, eliminate the character m at the end of every indivudal event """
        
    if 'x' in distance:
        parts = distance.split('x')
        if len(parts) == 2:
            num1, num2 = parts
            return int(num1) * int(num2)
    else:
        return int(distance.replace("m", ""))
        
swimming_data['Distance (in meters)'] = swimming_data['Distance (in meters)'].apply(convert_values)
swimming_data.rename(columns={'Distance (in meters)': 'Distance (m)'}, inplace=True)


# Identify for that each row, is the swimmer a winner -> Rank = 0
def calculate_winner(rank):
    not_winner = [2, 3, 4, 5]
    if rank == 1:
        return "True"
    elif rank in not_winner:
        return "False"
    else:
        return "No Data"
    
swimming_data['Winner?'] = swimming_data['Rank'].apply(calculate_winner)


# The default data type for the results currently are objects. In order to perform data anaylsis techniques on the set, we must convert this column to floating point numbers
"""
MM:SS.sss & HH:MM:SS.ssssss need to convert to purely seconds
"""
def convert_results_seconds(result):
    if 'est' in str(result):
        result = result.replace('est', '')
    
    if ':' not in str(result):
          return result
    
    bits = result.split(":")
    
    if len(bits) == 3:
        hours, minutes, seconds = float(bits[0]), float(bits[1]), float(bits[2])
        return hours * 3600 + minutes * 60 + seconds
    elif len(bits) == 2:
        minutes, seconds = float(bits[0]), float(bits[1])
        return minutes * 60 + seconds
    elif len(bits) == 1:  
        seconds = float(bits[0])
        return seconds
    else:
        return result


def convert_float(value):
    try:
        return float(value)
    except:
        return None
    
swimming_data['Time_in_Seconds'] = swimming_data['Results'].apply(convert_results_seconds)
swimming_data['Time (s)'] = swimming_data['Time_in_Seconds'].apply(convert_float)






"""
================== SLICING AND DICING THE DATA ==================
"""

# What is the minimum time at the men's 200 individual medley at the 2016 Olympics (1st place winner)
filtered_data = swimming_data[
    (swimming_data["Year"] == 2016) & 
    (swimming_data["Distance (m)"] == 200) &
    (swimming_data['Gender'] == 'Men') &
    (swimming_data["Stroke"] == "Individual medley")
]

min_two_hundred_time = filtered_data["Results"].min()
# The minimum time, or the time of the first place winner is 1:54.6600

# Group all participating countries by most silver medals
silver_medals = swimming_data[swimming_data["Medal?"] == "Silver"]
silver_medal_counts = silver_medals.groupby("Country").size()
silver_medal_counts = silver_medal_counts.sort_values(ascending=False)
# USA has the most silver medals with 171, followed by Australia with 67

# Group all male swimmers by most gold medals
male_gold_medals = swimming_data[
    (swimming_data["Gender"] == "Men") & 
    (swimming_data["Medal?"] == "Gold")
]
gold_medals_by_swimmer = male_gold_medals.groupby("Athlete").size()
gold_medals_by_swimmer = gold_medals_by_swimmer.sort_values(ascending=False)
# Micheal Phelps has the most gold medals in the dataset with 13, followed by Mark Spitz with 4


"""
 Function that creates a new column 'Race Type' depending on how long the race is.  

 length < 100: Sprint
 200 <= length <= 500: Middle-Distance
 length > 500: Distance
"""
def classify_race_type(length):
    if length <= 100:
        return "Sprint"
    elif 200 <= length <= 500:
        return "Middle-Distance"
    elif length > 500:
        return "Distance"
    else:
        return "Unknown"

swimming_data['Race Type'] = swimming_data['Distance (m)'].apply(classify_race_type)


# e. Find the average time (mean) in the women’s 100 butterfly throughout all Olympic years by all people who have swam it. 
# (Just need results float)
womens_100fly = swimming_data[
    (swimming_data["Gender"] == 'Women') &
    (swimming_data["Distance (m)"] == 100) &
    (swimming_data["Stroke"] == "Butterfly")
]

mean_one_hundred_fly_time = womens_100fly["Results"].mean()


# f. Display how many events there were in the 1984 Olympics. 
# (Just need event column)
swimming_1984 = swimming_data[swimming_data['Year'] == 1984]
unique1984__events = swimming_1984['Event'].nunique()


# g. Group the female swimmers only by name alphabetically.
female_swimmers = swimming_data[swimming_data['Gender'] == 'Women']
alphabetical_female_swimmers = female_swimmers.sort_values(by = 'Athlete')


# h. What was the average time of all of the winners of the 100 freestyle from the Olympic years 1912-1932. 
# (Just need results float)
early_winners_100free = swimming_data[
    (swimming_data["Distance (m)"] == 100) &
    (swimming_data["Stroke"] == "Freestyle") &
    (swimming_data['Year'] <= 1932)
]

mean_100free_time = early_winners_100free['Results'].mean()






"""
================== DATA VISUALIZATIONS ==================
"""

# VISUALIZATION 1
# Bar Graph comparing the top 10 Countries with highest medal count, and what medals they may contain

gold_medals = swimming_data[swimming_data['Rank'] == 1]
unique_gold_medal_count = gold_medals["Country"].value_counts()

silver_medals = swimming_data[swimming_data['Rank'] == 2]
unique_silver_medal_count = silver_medals["Country"].value_counts()

bronze_medals = swimming_data[swimming_data['Rank'] == 3]
unique_bronze_medal_count = bronze_medals["Country"].value_counts()

top = unique_gold_medal_count + unique_silver_medal_count + unique_bronze_medal_count
top_sorted = top.sort_values(ascending=False)

medal_counts = pd.DataFrame({
    'Gold': unique_gold_medal_count,
    'Silver': unique_silver_medal_count,
    'Bronze': unique_bronze_medal_count
})

colors = {
    "Gold": "royalblue", 
    "Silver": "slategray", 
    "Bronze": "silver"
} 

medal_counts['Total'] = medal_counts['Gold'] + medal_counts['Silver'] + medal_counts['Bronze']
top_ten_countries = medal_counts.sort_values(by='Total', ascending=False).head(10)

top_ten_countries[['Gold', 'Silver', 'Bronze']].plot(kind='bar', stacked=True, figsize=(10, 6), color=[colors['Gold'], colors['Silver'], colors['Bronze']])

plt.xlabel('Country', fontsize=14)
plt.ylabel('Number of Medals', fontsize=16)
plt.title('Top 10 Countries by Medal Count', fontsize=16)
plt.xticks(rotation=0)
plt.legend(title='Medals')

plt.show()





# VISUALIZATION 2
# Scatterplot throughout 1912-2020 of 200 women’s freestyle winners

fig, ax = plt.subplots()

women_two_hundred_winners = swimming_data[(swimming_data['Gender'] == 'Women') & 
                                          (swimming_data['Event'] == '200m Freestyle') & 
                                          (swimming_data['Rank'] == 1)]


ax.scatter(women_two_hundred_winners['Year'], women_two_hundred_winners['Time_in_Seconds'], color='royalblue')
plt.plot(women_two_hundred_winners['Year'], women_two_hundred_winners['Time_in_Seconds'], color='slategray')

plt.xlabel('Olympic Year')
plt.ylabel('Time (s)')
plt.title('200m Freestyle Winners (Women) Time vs. Year')

plt.show()





# VISUALIZATION 3
# Barchart of different 100 meter race best times for men and women

fig, ax = plt.subplots(figsize=(10, 6))
strokes = ['Backstroke', 'Breaststroke', 'Butterfly', 'Freestyle']

men_one_hundred_winners = swimming_data[(swimming_data['Distance (m)'] == 100) & (swimming_data['Rank'] == 1) & 
                                        (swimming_data['Gender'] == 'Men')]

women_one_hundred_winners = swimming_data[(swimming_data['Distance (m)'] == 100) & (swimming_data['Rank'] == 1) & 
                                          (swimming_data['Gender'] == 'Women')]
    
# Get minimum time (fastest) from each different type of stroke
fastest_men_times = men_one_hundred_winners.groupby('Event')['Time_in_Seconds'].min()
fastest_women_times = women_one_hundred_winners.groupby('Event')['Time_in_Seconds'].min()

men_times = {}
women_times = {}
for i in range(4):
    men_times[strokes[i]] = fastest_men_times[i]
    women_times[strokes[i]] = fastest_women_times[i]

strokes = men_times.keys()
x_pos = [0, 1, 2, 3]
bar_width = 0.2


# Dictionary, so enumerate
for i, stroke in enumerate(strokes):
    men_label = ''
    if i == 0:
        men_label = 'Men'
    women_label = ''
    if i == 0:
        women_label = 'Women'
        
    ax.bar(x_pos[i] - bar_width / 2, men_times[stroke], bar_width, label=men_label, color='cornflowerblue')
    ax.bar(x_pos[i] + bar_width / 2, women_times[stroke], bar_width, label=women_label, color='palevioletred')


ax.set_xlabel('Event', fontsize=14)
ax.set_ylabel('Time (s)', fontsize=14)
ax.set_title('Comparison of Fastest 100m Times for Men and Women', fontsize=16)

ax.set_xticks(x_pos)
ax.set_xticklabels(strokes, rotation=0)
ax.legend()
plt.tight_layout()

plt.show()





# VISUALIZATION 4
# Bar graph of the top 10 countries with the highest number of athletes. Compares values between number of male and female athletes

athletes_by_country_gender = swimming_data.groupby(['Country', 'Gender'])['Athlete'].nunique().reset_index()
pivot_data = athletes_by_country_gender.pivot(index='Country', columns='Gender', values='Athlete')

top_ten_countries = pivot_data.sum(axis=1).nlargest(10).index

top_ten_data = pivot_data.loc[top_10_countries]

top_ten_data.plot(kind='bar', figsize=(12, 8), color=['cornflowerblue', 'palevioletred'], edgecolor='black')

plt.title("Top 10 Countries by Number of Athletes", fontsize=16)
plt.xlabel('Country', fontsize=14)
plt.ylabel('Number of Athletes', fontsize=14)

plt.xticks(rotation=0, ha='right')  
plt.legend(title="Gender", fontsize=14)
plt.tight_layout()

plt.show()






# VISUALIZATION 5
# Box plot of the men's 200m Individual Medley Times

plt.figure(figsize=(12, 6))

mens_two_hundred_im = swimming_data[
    (swimming_data['Distance (m)'] == 200) & 
    (swimming_data['Stroke'] == 'Individual medley') & 
    (swimming_data['Gender'] == 'Men')
]

sns.boxplot(x='Year', y='Time_in_Seconds', data=mens_two_hundred_im)

plt.title("Men's 200 Individual Medley (IM) Times by Olympic Year", fontsize=14)
plt.xlabel("Olympic Year", fontsize=12)
plt.ylabel("Time (Seconds)", fontsize=12)

plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

plt.show()






# VISUALIZATION 6
# Box plot of the women's 200m Individual Medley Times

plt.figure(figsize=(12, 8))

womens_two_hundred_im = swimming_data[
    (swimming_data['Distance (m)'] == 200) & 
    (swimming_data['Stroke'] == 'Individual medley') & 
    (swimming_data['Gender'] == 'Women')
]

# contains nan value, cannot plot with them
womens_two_hundred_im = womens_two_hundred_im.dropna()
sns.boxplot(x='Year', y='Time_in_Seconds', data=womens_two_hundred_im)

plt.title("Women's 200 Individual Medley (IM) Times by Olympic Year", fontsize=14)
plt.xlabel("Olympic Year", fontsize=12)
plt.ylabel("Time (Seconds)", fontsize=12)

plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

plt.show()






# VISUALIZATION 7
# Combined box plot of the genders of the 200 IM results across all years 
plt.figure(figsize=(12, 6))

mens_two_hundred_im['Gender'] = 'Men'
womens_two_hundred_im['Gender'] = 'Women'
combined_200_im = pd.concat([mens_two_hundred_im, womens_two_hundred_im])

sns.boxplot(data=combined_200_im, x='Year', y='Time_in_Seconds', hue='Gender', palette='Set2')

plt.title('200 IM Best Times (Men & Women) Across Olympic Years')
plt.xlabel('Year')
plt.ylabel('Time in Seconds')

plt.xticks(rotation=45)
plt.legend(title='Gender')
plt.tight_layout()

plt.show()







"""
================== DATA ANALYSIS TECHNIQUES ==================
"""

# Implements logarithmic regression and calculates correlation in order to predict values 
mens_winner_one_hundred_free = swimming_data[(swimming_data['Gender'] == 'Men') & 
                            (swimming_data['Event'] == '100m Freestyle') &
                            (swimming_data['Rank'] == 1)]

mens_winner_one_hundred_free['Year'] = pd.to_numeric(mens_winner_one_hundred_free['Year'], errors='coerce')
mens_winner_one_hundred_free['Time (s)'] = pd.to_numeric(mens_winner_one_hundred_free['Time (s)'], errors='coerce')

x_values = mens_winner_one_hundred_free['Year']
y_values = mens_winner_one_hundred_free['Time (s)']

log_x = np.log(x_values)

a, b = np.polyfit(log_x, y_values, 1)

predicted_time = a * log_x + b


fig, ax= plt.subplots()
ax.scatter(x_values, y_values)
ax.plot(x_values, predicted_time)

plt.xlabel('Olympic Year')
plt.ylabel('Time (s)')
plt.title('100 Meter Freestyle Men Winners Time vs. Olympic Year')
plt.legend()

plt.show()

log_correlation = np.corrcoef(log_x, mens_winner_one_hundred_free['Time (s)'])[0, 1]
# R= -.96795. The correlation for this relationship is about -.96795, therefore the predictions that will be made are fairly accurate


# CROSS TABULATION
# Implementation of cross-tabulation using different countries and the gold medals they have won in the men's 100 breaststroke and the women's 100 breaststroke 
# Shows if swimming in the Olympics for a speicfic country improves the chance you have of getting a gold medal for the specific event
mens_one_hundred_breast = swimming_data[(swimming_data['Gender'] == 'Men') & (swimming_data['Event'] == '100m Breaststroke')]
womens_one_hundred_breast = swimming_data[(swimming_data['Gender'] == 'Women') & (swimming_data['Event'] == '100m Breaststroke')]

ct = pd.crosstab(mens_one_hundred_breast['Country'], mens_one_hundred_breast['Winner?'], normalize = 'index')
ct.drop('No Data', axis = 1, inplace = True)
ct

ct1= pd.crosstab(womens_one_hundred_breast['Country'], womens_one_hundred_breast['Winner?'], normalize = 'index')
ct1.drop('No Data', axis = 1, inplace = True)




