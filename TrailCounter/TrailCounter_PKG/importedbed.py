'''
Created on Oct 9, 2021

@author: jaqua
'''
import pandas as pd
from datetime import datetime
import math



df = pd.read_csv('test_file_alpha1.csv')
lasttimestamp = df.loc[0,['time']]

'''
if timestamp of photo is within limit (60) of another timestamp, then put them in the same group
for each photo, get all the rows of the data frame within limit
set all the rows within limit to the same group if there is no group number
if there is a group number combine groups
'''
#t = df['time']-lasttimestamp
df['t'] =[0, 0, 0, 0, 1, 1, 1, 1, 1, 1]

#print(df['time']==df.loc[0,['time']])

timestamplast = datetime.strptime(df.loc[0,'time'],'%Y-%m-%d %H:%M:%S')
df.loc[df['t']==0,'group'] = 1
print(timestamplast)


print(df)

df1 = df[df['group'] != 'NaN']

print(df1)


'''
count number of people for each file
'''

def count_persons(df):
    my_files = df['filename'].unique().tolist()
    df['persons'] = -1
    print(df.columns)
    for my_file in my_files:
        print(my_file)
        print([df['filename'] == my_file])
        print(df.loc[df.filename == my_file,'persons'])
        print(df[df['filename'] == my_file]['object'].value_counts(normalize = False)['Person'])
        df.loc[df.filename == my_file, 'persons'] = df[df['filename'] == my_file]['object'].value_counts(normalize = False)['Person']
        print(df['persons'])
        
    print(df[['filename', 'group','persons','object']])
    '''
        
        my_row = pd.DataFrame([[my_file,df['filename' == my_file].value_counts(normalize=False)['Person']]], columns = ['filename', 'persons'])
        dgroup = dgroup.append(my_row, ignore_index = True)
    
    
    create group df
    '''
    groups = df['group'].unique().tolist()
    print(groups)
    dgroup = pd.DataFrame(groups,columns = ['group'])
    print('what')
    print(dgroup)
    #dgroup = pd.DataFrame(columns = ['group', 'persons'])
    #dgroup['persons'] = -1
    for a in groups:
        #dgroup['group'] = a
        dgroup.loc[dgroup.group==a,'persons'] = max(df.loc[df['group']==a,'persons'])
        print(dgroup.loc[dgroup.group ==a,'persons'])
        print(max(df.loc[df['group']==a,'persons']))
       # dgroup.loc[dgroup.group ==a,'persons'] =  max(df.loc[df['group']==a,'persons'])
        #dgroup[['group': a, 'persons': max(df.loc[df['group']==a,'persons']) ]]
        print(dgroup['persons'])
       # my_row = pd.DataFrame([[a, df['group'== a].value_counts(normalize=False)['Person']]], columns = ['group', 'persons'])
       # dgroup = dgroup.append(my_row, ignore_index = True)
            
            
    print(dgroup)
    return dgroup


'''

count max number of people per group
'''
dg = count_persons(df)
print(dg.persons.sum())
print(dg)
'''
add to df


def maxphoto(df,a):

    
    max
    dgroup['group': a, 'persons': df['group'== a].value_counts(normalize=False)['Person']]
    

dgroup = maxphoto(df)
pin = dgroup['object'].value_counts(noralize=False)['Person']
pin = df['object'].value_counts(normalize=False)['Person']
print(pin)
'count number of people in each photo'
'for each group'
'find the max of each photo from the group'
'count the people in all the groups'

'''


'''
for row in df.rows:
    if row['time'] < 

add group numbers for each group (as a column)
for each group, report number of people as max of group

'''