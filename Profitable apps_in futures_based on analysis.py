#!/usr/bin/env python
# coding: utf-8

# # Gayathri's Mobile app analysis
# # My First Data science project
# - What is then project about? 
#     - To determine the profitablity of the 
# - What is our goal to achieve?
#     - 
# ` Datasets considered for this project are taken from Kaggle `

# In[1]:


from csv import reader

open_file = open('AppleStore.csv')
read_file = reader(open_file)
app_Store_InList = list(read_file)


open_file = open('googleplaystore.csv')
read_file = reader(open_file)
goggle_InList = list(read_file)    


# In[2]:


def explore_data(dataset,start,end,rows_and_columns = False):
    data_slice = dataset[start:end]
    for row in data_slice:
        print(row)
        print('\n')
    if rows_and_columns:
        print('Number of row: ',len(dataset[1:]))
        print('Number of columns', len(dataset[0]))


# In[3]:


print(app_Store_InList[0])
explore_data(app_Store_InList, 2, 5, True)


# In[4]:


print(goggle_InList[0])
explore_data(goggle_InList, 2,5, True)


# - We have 7197 iOS apps in this data set, and the columns that seem interesting are: 'track_name', 'currency', 'price', 'rating_count_tot', 'rating_count_ver', and 'prime_genre'. Not all column names are self-explanatory in this case, but details about each column can be found in the data set [documentation](https://www.kaggle.com/lava18/google-play-store-apps/home).

# - Now that we have analyzed the number of rows and columns in each data set, we now look at the actual data.
# ` In kaggle, it was reported that one of the row in google apps data set, was incomplete `
# 

# In[5]:


print(len(goggle_InList[10473]))
print(len(goggle_InList[0]))


# In[6]:


del goggle_InList[10473]


# In[7]:


print(len(goggle_InList[10473]))


# In[8]:


print(len(goggle_InList[10472]))


# In[9]:


print(goggle_InList[2])


# - The android data set seems to have duplicate entries in it. Identifying them and removing it becomes the next step.

# In[10]:


#create 2 lists- one for storing name of duplicate apps
# another for storing the names of unique apps
dupApps = []
uniqueApps=[]

for row in goggle_InList:
    name = row[0]
    if(name in uniqueApps):
        dupApps.append(name)
    else:
        uniqueApps.append(name)

#Print all duplicates
for row in goggle_InList:
    name = row[0]
    if name == 'Instagram':
        print(row)


# - There are a duplicates present in the data set
# - However, removing them randomly wouldnt be a better idea. Why? There are a lot of reasons:
# 1. You might be removing the most recent entyr
# 2. You might be identifying the duplicate column wrong. 

# In[11]:


# Print number of duplciate applications in the android google app store.
print(len(dupApps))


# - There are 1181 duplicate records in google app store. The number of  unique records are Total number of records - Total number of duplicates

# In[12]:


# Number of unique records
print('********Expected Length********= ', len(goggle_InList) - 1181)


# - Yay! We are now actually removing dupes from the code.
# - Ok, we now know there are 1181 dupes in the data set. 
# - We use dictionary to remove them, let's see how. I will place comments as and when required.

# In[13]:


#Create a dictionary

reviews_max = {}

for row in goggle_InList[1:]:
    name = row[0]
    n_reviews = float(row[3])

    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews

print('*******Actual Length******** = ' , len(reviews_max))


# - I created a dictionary "reviews_max" with the name of the app and max reviews as value. 
# - Now its time to remove the duplicates
#      - *explaining it later*

# - Create 2 lists
#     -  android clean to hold all the android apps without duplicates
#     -  already added list to hold if a row has been added ot the android list.
# 
# - Loop through the google app list, find out the name of the application, check in android clean. if already present with the same max count, do not append to it. Just append it to already added list.

# In[14]:




android_clean = []
already_added = []

for row in goggle_InList[1:]:
    name = row[0]
    n_reviews = float(row[3])
    
    if name not in already_added and reviews_max[name] == n_reviews:
        android_clean.append(row)
        already_added.append(name)
                


# - Print the count of android clean list. THis list does not contain any duplicates. The expected and actual count match and it is 9659

# #### Remove non english characters in the applications.

# - Here we are analyzing only English apps directed to English speaking audience.
# - How do we remove these foreign characters?
#        Two steps --->
#          1)   Yes, by using ASCII values. We know English characters are within the range 0 -127
#             In order to find out the ASCII value, use ord() function
#         2) You can assign a character to each individual character in a string. 
#        DID YOU KNOW??
#            You can iterate through a string and loop through its characters in for loop!!
#            Isnt it interesting

# In[15]:


# LETS WRITE A FUNCTION- To see if a string is in English or not, by using above 2 functions.

def isEnglish(somestring):
    for charac in somestring:
        num = ord(charac)
        if num >127:
            return False
    return True
        
print(isEnglish('Instagram'))


# In[16]:


#  LETS WRITE Another FUNCTION- To see if a string is in English with not more
# than 3 foreign characters


def isEngWith3ForeignChars(somestring):
    count = 0
    for charac in somestring:
        num = ord(charac)
        if num >127:
            count +=1
            if(count > 3):
                return False
            
    return True
        
print(isEngWith3ForeignChars('爱奇奇奇奇PPS 😜'))


# - Use the new function to remove the application names from the data set using the above function.  This should only filter out the names for English speaking audience only. 

# In[17]:


#create a list to insert 
eng_android_clean = []

for row in android_clean:
    name = row[0]
    isEnglish = isEngWith3ForeignChars(name)
    if isEnglish:
        eng_android_clean.append(row)
        
print('*****English only free android apps in the data set are******* = ', len(eng_android_clean))


# ## So far -
#  ###### Removed inaccurate data
#  ###### Removed duplicate entries for the same application names
#  ###### Removed non english application names using ord() 

# In[18]:


print(eng_android_clean[0])


# ### Last Step for now:
# - Removing the non-free apps from the data set 

# In[19]:


# loop through the android clean english only apps data set and remove the ones that are not free
free_eng_android_clean = []

for row in eng_android_clean:
    #Element number 6 is the one
    isFree = row[6]
    if isFree == 'Free':
        free_eng_android_clean.append(row)

print('*****Free English only android apps****** = ' , len(free_eng_android_clean))
    
    
    


# In[20]:


print(free_eng_android_clean[1])


# ### What's next?
# #### Let's define the steps and why we do that
#             ` What's our end goal? 
#                 Find out the apps from both android and app store market and see how many of them are using it. Let's look at the genres that people are interested. 
#                 I am going a build a frequency table that would tell us the list of genres and how many are using it. ` 

# In[21]:


# Lets create a frequency

frequency_dict_google = {}

for row in free_eng_android_clean:
    genre = row[9]
    if genre in frequency_dict_google:
        frequency_dict_google[genre] +=1
    else:
        frequency_dict_google[genre] = 1
        
print('******Frequency of genres in android apps******\n\n', frequency_dict_google)


# In[22]:


frequency_dict_apple = {}

for row in app_Store_InList[1:]:
    genre = row[11]
    if genre in frequency_dict_apple:
        frequency_dict_apple[genre] +=1
    else:
        frequency_dict_apple[genre] = 1
        
print(frequency_dict_apple)


# ### Most popular Genre -  liked by customers

# ### Android vs Apple

# In[23]:


print('Most like genre- Google = ', max(frequency_dict_google.values()))


# In[24]:


print('Most like genre- Apple = ', max(frequency_dict_apple.values()))


# #### THe above code wouldnt give us the key. The best thing to do is to sort it and take out the first element to get the max.Similar to what you are used to do in Excel!
#     Let's do it!

# In[25]:


def freq_table1(dataset, index):
    freq_dict = {}
    total = 0
    
    for row in dataset:
        total +=1
        freq_of = row[index]
        if freq_of in freq_dict:
            freq_dict[freq_of] +=1
        else:
            freq_dict[freq_of] =1
    
    table_percentages = {}
    
    for key in freq_dict:
        percentage = (freq_dict[key] / total) * 100
        table_percentages[key] = percentage      
            
    return table_percentages



# In[26]:


def display_table(dataset, index):
    table = freq_table1(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# In[27]:


print('*****Sorted with max PRIME GENRES- APPLE STORE***** \n\n')
display_table(app_Store_InList[1:],11)


# - What is the most common genre? What is the runner-up?
#     - Games : 3862 is the most common genre
#     - Entertainment : 535 is the runner up
# 
# - What other patterns do you see?
#     - All entertainment related apps are most commonly used apps
#     - Other such as news, weather business are very less downloaded. 
#     
#     
# - What is the general impression — are most of the apps designed for practical purposes (education, shopping, utilities, productivity, lifestyle) or more for entertainment (games, photo and video, social networking, sports, music)?
#     - Yes, most of the apps are designed for least critical stuff in life. 
#     - Most critical app genres such as medical and business are not downloaded by many or not being created at all. 
# 
# - Can you recommend an app profile for the App Store market based on this frequency table alone? If there's a large number of apps for a particular genre, does that also imply that apps of that genre generally have a large number of users?
# 
#     - I dont think we can conclude that easily the genre. But, with the current statistics, we can say that any app related to Games is going to succeed. However, these do not mean there a

# In[28]:


print('*****Sorted with max GENRES- GOOGLE PLAY STORE***** \n\n')
display_table(free_eng_android_clean,9)


# 

# In[29]:


print(' \n')
print('*****Sorted with max CATEGORY - GOOGLE PLAY STORE***** \n\n')
display_table(free_eng_android_clean,1)


# Analyze the frequency table you generated for the Category and Genres column of the Google Play data set.
# 
# *What are the most common genres?*
# - Family and Games
# - Games is at the top again but not the first 
# 
# *What other patterns do you see?*
# - Unlike critical apps related to medicine, business are also in the top 20% 
# 
# *Compare the patterns you see for the Google Play market with those you saw for the App Store market.
# Can you recommend an app profile based on what you found so far? Do the frequency tables you generated reveal the most frequent app genres or what genres have the most users?*
# - Yes, somewhat.
# - Games are the highest in both Google and Apple App store.
# 

# ## Most popular apps by Genre on the App store

# In[30]:


# Most popular apps by Genre on the App store



# In[31]:


prime_genres_ios = freq_table1(app_Store_InList[1:], -5)

for uniquegenre in prime_genres_ios:
    total = 0
    len_genre = 0
    for row in app_Store_InList:
        genre_app = row[-5]
        if uniquegenre == genre_app:
            user_rating = float(row[5])
            total += user_rating
            len_genre += 1
    avg_userratings = total / len_genre
    print(genre_app,' : ', avg_userratings)
    
        


# In[32]:


for app in app_Store_InList[1:]:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5])


# ## Most Popular Apps by Genre on Google Play

# For the Google Play market, we actually have data about the number of installs, so we should be able to get a clearer picture about genre popularity. However, the install numbers don't seem precise enough — we can see that most values are open-ended (100+, 1,000+, 5,000+, etc.):

# In[33]:


display_table(free_eng_android_clean,5)


# In[35]:


categories_android = freq_table1(free_eng_android_clean,1)


# In[47]:


print('Category:                  Installs')

for category in categories_android:
    total = 0
    len_category = 0
    for row in free_eng_android_clean:
        if category == row[1]:
            installs = row[5]
            installs = installs.replace('+', '')
            installs = installs.replace(',', '')
            installs = int(installs)
            total = total + installs
            len_category += 1
    
    #Find average number of installs 
    avg = total / len_category
    print(category, '            ', avg)
    


# In[65]:


for app in free_eng_android_clean:
    if (app[1] == 'MEDICAL' and (app[5] == '1,000,000,000+'
                                            or app[5] == '500,000,000+'
                                            or app[5] == '100,000,000+')):
        print(app[0], ':', app[5])


# I would go for Medical apps as there are non-

# In[66]:


for app in free_eng_android_clean:
    if app[1] == 'MEDICAL' and (app[5] == '1,000,000+'
                                            or app[5] == '5,000,000+'
                                            or app[5] == '10,000,000+'
                                            or app[5] == '50,000,000+'):
        print(app[0], ':', app[5])


# Gayathri's take on this:
# 
# There are very few medical apps that are good and are in demand. Based rise in the number of games
# and entertainment apps and less of fitness/health apps, 
# there is a possibility that these medical apps can prove demanding in future. 
