import matplotlib.pyplot as plt
import pandas as pd

url_mat = 'Datasets/material.csv'
with open(url_mat, 'r') as f_mat:
    data_mat = f_mat.read()
    # print (data_mat)
    

url_mat_pro = 'Datasets/material_progress.csv'
with open(url_mat_pro, 'r') as f_mat_pro:
    data_mat_pro = f_mat_pro.read()
    # print(data_mat_pro)
    
url_user_skill = 'Datasets/user_skill.csv'
with open(url_user_skill, 'r') as f_user_skill:
    data_user_skill = f_user_skill.read()
    # print(data_user_skill)
    

""" Creating tables"""

"""material.csv"""

val1 = ["Field Name", "Explanation"] 
val2 = ["","","",""] 
val3 = [["material_id:", "An id that starts with'DE'"],
        ["type:", "video/text/interactive"],
        ["language:", "en/de"],
        ["duration_minutes:", "Duration time in minutes"]
        ]
   
fig, ax = plt.subplots() 
ax.set_axis_off() 
table = ax.table( 
    cellText = val3,  
    rowLabels = val2,  
    colLabels = val1, 
    rowColours =["palegreen"] * 4,  
    colColours =["palegreen"] * 2, 
    cellLoc ='left',  
    loc ='upper center')         
   
ax.set_title('Explanation of material.csv file', 
             fontweight ="bold") 
plt.show()


"""material_progress.csv"""

val1 = ["Field Name", "Explanation"] 
val2 = ["","","",""] 
val3 = [["user_id:", "Unique id for each person"],
        ["material_id:", "An id that starts with'DE'"],
        ["start_at:", "Starting date and time"],
        ["finished_at:", "finishing date and time"]
        ]
   
fig, ax = plt.subplots() 
ax.set_axis_off() 
table = ax.table( 
    cellText = val3,  
    rowLabels = val2,  
    colLabels = val1, 
    rowColours =["palegreen"] * 4,  
    colColours =["palegreen"] * 2, 
    cellLoc ='left',  
    loc ='upper center')         
   
ax.set_title('Explanation of material_progress.csv file', 
             fontweight ="bold")   
plt.show()


"""user_skill.csv"""

val1 = ["Field Name", "Explanation"] 
val2 = ["","",""] 
val3 = [["user_id:", "Unique id for each person"],
        ["skill_id:", "Unique id for each person"],
        ["is_mastered:", "TRUE/FALSE"]
        ]
   
fig, ax = plt.subplots() 
ax.set_axis_off() 
table = ax.table( 
    cellText = val3,  
    rowLabels = val2,  
    colLabels = val1, 
    rowColours =["palegreen"] * 4,  
    colColours =["palegreen"] * 2, 
    cellLoc ='left',  
    loc ='upper center')         
   
ax.set_title('Explanation of user_skill.csv file', 
             fontweight ="bold") 
plt.show()



"""Calculation of user actual time"""

df_mat_pro = pd.read_csv(url_mat_pro)  #df_mat_pro is the dataframe of material_progress.csv
df_mat_pro = df_mat_pro.dropna()     #delete NAN and NAT data values as they were only 4.3%
df_mat_pro ['actual_time'] = pd.to_datetime(df_mat_pro['finished_at']) - pd.to_datetime(df_mat_pro['started_at'])     #calculate actual time in datatime format
df_mat_pro ['actual_time_sec'] = df_mat_pro['actual_time'].dt.total_seconds().astype(int)       #calculate actual time in seconds
del df_mat_pro['started_at']        #delete unnecessary columns
del df_mat_pro['finished_at']       #delete unnecessary columns    
print(df_mat_pro.head())

df_mat = pd.read_csv(url_mat)       #df_mat is the dataframe of material.csv


df_inner_material = pd.merge(df_mat, df_mat_pro, how='inner')       #inner join as material_id is common
del df_inner_material['actual_time']        #delete unnecessary columns
df_inner_material['estimated_time_sec'] = (df_inner_material['duration_minutes'])*60    #calculate duration_minutes in seconds


"""******* 
    (2.a): Do actual learning times deviate from our estimated learning times? ******"""
""" reply: df_inner_material is the inner join of material.csv and material_progress.csv
           as material_is is common.
           df_inner_material['actual-estimated'] is the difference between
           actual time that users spend and the estimated time (in seconds)
           Negative values means: user spent less time than estimated time.
           Positive values means: user spend more time than estimated time.
           
           pay attention to the the following line:
"""

df_inner_material['actual-estimated'] = df_inner_material['actual_time_sec'] - df_inner_material['estimated_time_sec']



""" (2.b):Do the results differ between different types or languages of materials?
    reply:I groupped df_inner_material by type and language seperately.
          also I calculated sum and mean for each group.
    
"""
df_inner_type_sum = df_inner_material.groupby("type")['actual-estimated'].sum()
df_inner_type_mean = df_inner_material.groupby("type")['actual-estimated'].mean()

df_inner_language_sum = df_inner_material.groupby("language")['actual-estimated'].sum()
df_inner_language_mean = df_inner_material.groupby("language")['actual-estimated'].mean()


""" (2.c): Can you detect learners who might be "cheating" with their learning progress (i.e., who probably have not been consuming the learning material) from the data?
    reply: in df_inner_material table users with negative ['actual-estimated'] are probably cheating
    
"""
    #done previously


"""
    (3):   What other information can you derive from the data?
    reply: bar charts of 4 previous tables
"""
#Bar Chart of :df_inner_type_sum
plotdata = pd.DataFrame(df_inner_type_sum)
plotdata.plot(kind="bar")
plt.title("Sum of differences between actual spending time and estimated time for each type")
plt.xlabel("type")
plt.ylabel("Sum of 'Actual-Estimated time'(sec)")
plt.fontweight = "bold"

#Bar Chart of :df_inner_type_mean
plotdata = pd.DataFrame(df_inner_type_mean)
plotdata.plot(kind="bar")
plt.title("Mean of differences between actual spending time and estimated time for each type")
plt.xlabel("type")
plt.ylabel("Mean of 'Actual-Estimated time'(sec)")
plt.fontweight = "bold"

#Bar Chart of :df_inner_language_sum
plotdata = pd.DataFrame(df_inner_language_sum)
plotdata.plot(kind="bar", color='red')
plt.title("Sum of differences between actual spending time and estimated time for each language")
plt.xlabel("language")
plt.ylabel("Sum of 'Actual-Estimated time'(sec)")
plt.fontweight = "bold"

#Bar Chart of :df_inner_language_mean
plotdata = pd.DataFrame(df_inner_language_mean)
plotdata.plot(kind="bar", color='red')
plt.title("Mean of differences between actual spending time and estimated time for each language")
plt.xlabel("language")
plt.ylabel("Mean of 'Actual-Estimated time'(sec)")
plt.fontweight = "bold"

"""
    Second Question:
"""


class User:
    def __init__(self, user_key:int, skill_dict:dict):      #2 attributes
        self.user_key = user_key            #values starts from 0
        self.skill_dict = skill_dict        #dictionary that contains skill_id and mastery level
                                            #that means: {'skill_id':True/False}
        
    def describe(self):                     #print user_key, list of his/her skills
                                            #and mastery status
        print(self.user_key)
        print(self.skill_dict)
    
    def number_of_skills(self):             #indicates number of skills and 
                                            #percentage of skills that the user is mastered
        print("Number of skills:", len(self.skill_dict))
        count = 0
        for k,v in self.skill_dict.items():
            if v:
                count+=1
        per = (count/len(self.skill_dict))*100
        print("Percentage of mastered skills:",per)
    
    
""" create objects of Class User
"""
df_user_skill = pd.read_csv(url_user_skill)     #creat the dataframe of user_skill.csv
df_mat_pro_user_skill = pd.merge(df_inner_material, df_user_skill, how='inner')

i = 0
all_users_dic = {}          #is a nested dictionary that the key of first level dictionary is user_id 
                            #and values of the first level dictionary is a dictionary that the keys are
                            #skill_id and the values are mastery status(True/False)
for index in df_mat_pro_user_skill.index:   #iterating to creat the nested dictionary
    i+= 1
    if df_mat_pro_user_skill['user_id'][index] not in all_users_dic:    #if this user_id doesn't exist in the all_users_dic
        dd = {df_mat_pro_user_skill['skill_id'][index] : df_mat_pro_user_skill['is_mastered'][index]}
        all_users_dic.setdefault(df_mat_pro_user_skill['user_id'][index] , dd)
    else:                                                               #if this user_id doesn't exist in the all_users_dic
        d = {df_mat_pro_user_skill['skill_id'][index]:df_mat_pro_user_skill['is_mastered'][index]}
        all_users_dic[df_mat_pro_user_skill['user_id'][index]].update(d)
    

my_objs=[]      #list of objects
j = 0           #user_key
for k in all_users_dic:                         #Creates objects 
    my_objs.append(User(j, all_users_dic[k]))  
    j+=1
    
my_objs[0].describe()
my_objs[0].number_of_skills()
    




