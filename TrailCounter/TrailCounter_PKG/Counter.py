'''
Created on Jan 16, 2021

@author: jaqua
'''
import os, io
from google.cloud import vision_v1
#from google.cloud.vision_v1 import types
import pandas as pd
#from PIL import Image
#from pandas.tests.extension.test_external_block import df
from datetime import datetime, timedelta
#import datetime
import math
from sqlalchemy.engine import strategies
import matplotlib


# def get_pic(my_pic_filename):
#     #set this thumbnail as the url
#     """add a jpg file in quotes that's in the same file as this"""
#     
#     with open(my_pic_filename,'rb') as f:
#         content = f.read()
#         
#     image2 = vision_v1.Image(content = content)
# 
#     return image2

os.environ['GOOGLE_APPLICATION_CREDENTIALS']= 'cloudvisionone-322022-c838d7c9b161.json'
 
# Instantiates a client
client = vision_v1.ImageAnnotatorClient()

def my_prop(my_file):
    
    image = vision_v1.Image(content = get_pic(my_file))
    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    print('Properties:')
 
    for color in props.dominant_colors.colors:
        print('fraction: {}'.format(color.pixel_fraction))
        print('\tr: {}'.format(color.color.red))
        print('\tg: {}'.format(color.color.green))
        print('\tb: {}'.format(color.color.blue))
        print('\ta: {}'.format(color.color.alpha))   

def get_pic(my_pic_filename):
    #set this thumbnail as the url
    """add a jpg file in quotes that's in the same file as this"""
     
    with open(my_pic_filename,'rb') as f:
        content = f.read()
         
    image2 = vision_v1.Image(content = content)
 
    return image2

def my_labeldetect(my_filename):
#### LABEL DETECTION ######
   
    df = pd.DataFrame(columns =('filename', 'label', 'label_score'))
    response_label = client.label_detection(image=get_pic(my_filename))
#     image2 = vision_v1.Image(content = get_pic(my_filename))
# 
# 
#     response_label = client.label_detection(image=image2)


    for label in response_label.label_annotations:
        print({'label': label.description, 'label_score': label.score})
        my_row = pd.DataFrame([[my_filename, label.description,label.score]], columns = df.columns)
        #print(my_row)
        df = df.append(my_row, ignore_index = True)
    
    
    return df

def my_object(my_filename):
    
    df = pd.DataFrame(columns =('filename', 'object', 'object_score', 'object_bounds', 'time'))
    columns_a= ('filename', 'object', 'object_score', 'object_bounds')
#     image2 = vision_v1.Image(content = get_pic(my_filename))

    objects = client.object_localization(image=get_pic(my_filename)).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        my_row = pd.DataFrame([[my_filename, object_.name,object_.score, object_.bounding_poly]], columns = columns_a)
        print(my_row)
        df = df.append(my_row, ignore_index = True)
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
            
            
    return df

def my_detect_text(my_filename):
    """Detects text in the file."""

#     image2 = vision_v1.Image(content = get_pic(path))
    df = pd.DataFrame(columns =('filename', 'text', 'time'))
    response = client.text_detection(image=get_pic(my_filename))
    df.text = response.text_annotations
    
    print('Texts:')

    for text in df.text:
        my_row = pd.DataFrame([[my_filename, text.description]], columns = ['filename', 'text'])
        df = df.append(my_row, ignore_index = True)
        
        if "202" in text.description:
            print('found date')
            '''extract the date into date format'''
            
            this_date = text.description
            this_date.replace("I","")
#             if ":" in text.description:
#                 print('nothing')
# 
#             else:
#                 date_object = datetime.strptime(text.description, '%Y/%m/%d')
           
        if ":" in text.description:
            
            print('found time')
#             if "/" in text.description:
#                 print('nothing')
#             
#             else:
#                 time_object = datetime.strptime(text.description, '%H:%M:%S')
                
            this_time = text.description
           
        
           
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))


    try:
         
        my_datetime = this_date + ' ' + this_time
        print(my_datetime)
        newdatetime = datetime.strptime(my_datetime,'%Y/%m/%d %H:%M:%S')
        
    except:
        try:    
            my_datetime = this_time
            print(my_datetime)
            newdatetime = datetime.strptime(my_datetime,'%H:%M:%S')
            if response.error.message:
                raise Exception(
                    '{}\nFor more info on error messages, check: '
                    'https://cloud.google.com/apis/design/errors'.format(
                        response.error.message))
            
        except:
            newdatetime = datetime(2000,1,1)
            
              
    

    df.loc[:,'time']=newdatetime
    print(type(newdatetime))
    print(newdatetime)  # printed in default format
    return newdatetime     
         
def clean_time(df):
    
    '''
for every row, define last_clean_datetime, and next_clean_datetime, default to shift 1 and shift -1
check if 'clean times' say 1900 or 2000, which is 'dirty'
if time is 'dirty' move up one unitl there is a 'clean' time
once all times are clean

allow group after
    '''
    i = 1
    my_date = datetime(2020,1,1)
    df['last_clean_time'] = df['time'].shift(i)
    while not df[df.last_clean_time <my_date].empty:
        i+=1
        df.loc[df.last_clean_time <my_date,'last_clean_time'] = df['time'].shift(i)
        print(i)
        
        
    i = 1
    df['next_clean_time'] = df['time'].shift(-i)
    while not df[df['next_clean_time']<my_date].empty:
        i+=1
        df.loc[df.next_clean_time <my_date,'next_clean_time'] = df['time'].shift(-i)
        print(i)
    
    '''
    if time is dirty
    if last & next clean are same date
    use that date in time
    
    '''
    print(df.last_clean_time,'last_clean_time')
    print(df.next_clean_time,'next_clean_time')
                
#      #   df['last_clean_time'].date == df['next_clean_time'].date
#     for index, row in df.itertuples():
#         lct = row['last_clean_time']
# 
#         if row['time']<my_date:
#             row['time'].replace(year = lct.year, month = lct.month, day = lct.day)
    df.time = pd.to_datetime(df.time)
    print('df.time') 
    print(df.time)
    
    print(df.time.dt.date,'df.time.dt.date')
    df['new_date'] = df.time.apply(lambda x: x.date()) #df.time.apply(datetime.date())
    df['new_time'] = df.time.apply(lambda x: x.time())#pd.to_datetime(df.time).time()
   
#     print('new_date')
#     print(df.new_date)
#     
#     print('new_Time')
#     print(df.new_time)
#     print('new_time_2')
#     print(df['new_time'])
    
    
    df.loc[df.time<my_date,'new_date'] = pd.to_datetime(df.last_clean_time).dt.date
    df.loc[df.new_date.isnull(), 'new_date'] = pd.to_datetime(df.next_clean_time).dt.date
    print('df.time')
    print(df.time)
    print(df.new_date)
    df.loc[df.time<my_date,'time'] = df.apply(lambda x: x['time'].replace(year = x.new_date.year, month = x.new_date.month, day = x.new_date.day),  axis = 1)  
    #lambda x: datetime.combine(pd.to_datetime(df['new_date']), df['new_time']), axis = 1)
    #df.loc[df.time<my_date, 'time'] = datetime.combine(df.last_clean_time.date(), df.time.time()) #df.apply(lambda x: datetime.combine(x.new_date, x.new_time))#pd.to_datetime(df.new_date.strftime + " " + df.new_time.strftime)
    print(df.time)
   # df.loc[type(df.time) != datetime,'time'] = my_date
   # print(df.time)

    #settime = datetime(year = df.last_clean_time.year, month = df.last_clean_time.month, day = df.last_clean_time.day, hours = )
    #df.loc[df.time <= my_date.time]
    
#     df_prime = df.loc[df.time.dt.year <= my_date.year]
#     df_prime.time.dt.year = my_date.year
   # df.loc[df_prime.index,'time'] = df.prime.time
    
    #print(df_prime)
    print(df)
    print('printed df prime and df')
    
   #pd.to_datetime(df.loc[df['time']<my_date,'time']).replace(year = pd.DatetimeIndex(df.last_clean_time).year, month = pd.DatetimeIndex(df.last_clean_time).month, day = pd.DatetimeIndex(df.last_clean_time).day)

    #pd.to_datetime(df.loc[df['time']<my_date,'time']).replace(year = pd.to_datetime(df.last_clean_time).year, month = pd.to_datetime(df.last_clean_time).month, day = pd.to_datetime(df.last_clean_time).day)
    print(df)

    
    return df
  
def my_photos(directory):
    df = pd.DataFrame(columns =('file_number','filename', 'object', 'object_score','object_bounds','time'))
    columns_a = ('file_number','filename', 'object', 'object_score','object_bounds')
    n_file = 1
    for filename in os.listdir(directory):
        newpath = os.path.join(directory,filename)
        df = df.append(my_object(newpath),ignore_index = True)
        
        print(df)
        df.loc[df['filename']== newpath,'file_number'] = n_file
        n_file += 1
        print(df)
#         df.iloc[-1]['time'] = my_detect_text(os.path.join(directory, filename))
        #df.loc[newpath,'time']
        df.loc[df.filename.isin([newpath]),'time'] = my_detect_text(newpath)
#         masks = df.loc['filename'].values == newpath
#         df_new = df.loc[mask]]
        #df.loc['filename' = newpath,'time'] =  my_detect_text(newpath)

        '''
        Issue:  if you don't get the right time, then you can't be assigned to the correct group (which implies the day?) and you can't know what day those poeple were hiking on
        Fix:  if you didn't abstract a time, figure out if you're in the group of photos before or after your photo.
        (if you have two in a row   
        Find all rows whose day is < 2020 [really would like all rows whose day is not between last and next entry]
        Set day to same day as next image, if time is earlier than next image, otherwise set day to day of last image if time is after time of last image, otherwise error
        
        
        '''
        df
    return df

def group_data(df,lasttime,x):
    '''
    
    find elements with NaN
    first one is lasttime
    create data frame of data with no group
    get last time from first element of that group
    find all elements with the same time as that group
    give all those elements the same group number
    
        df.loc[df['time'] == lasttime, 'group'] = x
    print(df)
    df1 = df[df['group']==-1]
    print(df1)

    if not df1.empty:
                
        lasttime = df1.iloc[0,3]
        print(lasttime)
        print(df1.size)
        group_data(df,lasttime,x+1)
              
    
    print('empty')
    print(df)
    return df
    '''
    
    '''
    find elements that fit within range criteria
        assess if group time is within range of lasttime
        range is relative to lasttime
        add range as a row to the table
    assign all rows that fit criteria with the same group
    create new data frame for remaining groups
    repeat recurrsively for remaining group
    at the end, assess if there is any overlap, and give an indication
    '''
    
    #create range criteria
    range_size = timedelta(seconds = 30) #size of range in seconds Syntax : datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
    range_start = lasttime
    
    print(range_size)
    print(range_start)  
    
    range_end = range_start + range_size
    

    #remove elements that say 'error' or other text
    df_error = df[df['time'].map(type) == str]
    df_clean = df[df['time'].map(type) != str]
    
    print(df_error)
    print(df_clean)
    #find elements that fit within range criteria
    i_range_start = (df[df['time'].map(type) != str].time >= range_start)
    i_range_end = (df[df['time'].map(type) != str].time < range_end)
    i_tot = i_range_start & i_range_end
    
    print('i_range_start')
    print(i_range_start)
    
    
    
    print('i_tot')
    print(i_tot)
#     i_tot = i_tot.flatten()
    
    df.loc[i_tot[:],'group']=x
    
#     df.loc[(df[df['time'].map(type) != str].time >= range_start) & (df[df['time'].map(type) != str].time < range_end), 'group'] = x

    #df.loc[(df['time'] >= range_start) & (df['time'].map(type) < range_end),'group']= x
    df.loc[df['group']==x,'range_start'] = range_start
    print(df)
    df1 = df[df['group']==-1]
    print(df1)
    df1.head(1)
    print('df1')
    
    if not df1.empty:
                
        lasttime = df1.iloc[0].time
        print(lasttime)
        print(df1.size)
        group_data(df,lasttime,x+1)
              
    
    print('empty')
    print(df)
    return df

def count_persons(df):
    my_files = df['filename'].unique().tolist()
    df['persons'] = 0
    print(df.columns)
    for my_file in my_files:
        try:
            df.loc[df.filename == my_file, 'persons'] = df[df['filename'] == my_file]['object'].value_counts(normalize = False)['Person']
            print(df['persons'])
        except:
            df.loc[df.filename == my_file, 'persons'] = 0
            df.loc[df.filename == my_file, 'errors'] = 'error in # of persons' 
            '''-2 now indicates an error'''
        
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
        try:
            dgroup.loc[dgroup.group==a,'persons'] = max(df.loc[df['group']==a,'persons'])
            dgroup.loc[dgroup.group==a, 'range_start'] = max(df.loc[df['group']==a,'range_start'])
            #dgroup.loc[dgroup.group==a,'days'] = dgroup.loc[dgroup.group==a,'range_start'].day
        except:
            dgroup.loc[dgroup.group==a,'errors'] = 'error in count_persons: either with #of persons or range_start'
            #dgroup.loc[dgroup.group==a,'range_start'] = 'error'

        print(dgroup['persons'])
        print(dgroup)
    
    dgroup.loc[:,'days'] = dgroup.range_start.apply(lambda x: x.date()) #pd.to_datetime(dgroup.range_start).day()
    print(dgroup)     
    df_day = dgroup.groupby('days')['persons'].sum().reset_index()       
            
#     my_days = df['day'].unique().tolist()
#     print(my_days)
#     df_days = pd.DataFrame(my_days, columns = ['days'])
#     
#     for d in my_days:
#         df_days.loc[df_days.day == d, 'persons'] = sum(df.loc[df''])
            
    print(dgroup)
    print(df_day)
    return df_day







#df.groupby(by=['filename'])['object'].value_counts(normalize = True) 
#determine if photos are of the same people
#  use time constraint as 'sameness'
#     add column for unique person count
#     for each entry, unique person = count of person, if time < threshold from previous entry
#get the max number of people from photos of same people
#add that to count one time
#annotate photos as same group of people
#print results to a record (database or spreadsheet)


        
directory1 = r'C:\Users\jaqua\Pictures\Saved Pictures\2017\12'    
directory = r'C:\Users\jaqua\Downloads\test'
fname1 = '20210124_123122.jpg'
fname2 = 'Normal-People.jpg'
fname3 = 'DSCF0001.jpg'
site1 = 'https://drive.google.com/drive/folders/1M61acPE_F61y5n0DCUiHy0QJnXepxJg3?usp=sharing'
alphatest = r'C:\Users\jaqua\Downloads\PUP 9__-20211014T013101Z-001\PUP 9_\100MEDIA'
gammatest = r'C:\Users\jaqua\Downloads\Thopmson__-20211127T004305Z-001\Thopmson_\PUP 9_\100MEDIA'
betatest = r'C:\Users\jaqua\Downloads\Thopmson__-20211127T004305Z-001\Thopmson_\PUP 10_\100MEDIA'
beta2 = r'C:\Users\jaqua\Downloads\Thopmson__-20211127T004305Z-001\Thopmson_\PUP 10_\103MEDIA'
#df = my_object(fname1)
# print('my detect text for file: ')
# print(fname3)
# df = my_detect_text(fname3)
# print(df)
# pin = df['object'].value_counts(normalize=False)['Person']
# print(pin)

#count number of people in photos
'''
Execution starts here
'''

df_prime = my_photos(gammatest)
df_prime.to_csv('clean_test_dirty.csv')
df = clean_time(df_prime)

lasttime = df.loc[0,'time']

df['group'] = -1
df = group_data(df,lasttime,1)

#print(df.dtypes)
print(df)
print('got here')

pin = df['object'].value_counts(normalize=False)['Person']
print(pin)
df.to_csv('gammatest.csv')
#df_prime.to_csv('clean_test_dirty.csv')

'''
clean up time -
    if can't find day, check if previous and next file have the same day, then use that.
    if they don't have the same, then choose next day if day/time is not later than the next file.
    need time to be in the dg file
'''
'''

count max number of people per group
'''
dg = count_persons(df)
dg.to_csv('beta_2 _people.csv')
print('most important number =')
print(dg.persons.sum())
print(dg)
'''
df = my_photos(directory)
n = len(pd.unique(df['filename']))

print(n)
'''
#df['object'].value_counts(normalize=True)
#print(df[['filename','group','time']])

#df['counts']= df.groupby(by=['filename'])['object'].value_counts(normalize = True) 
# df.to_csv('test_file_alpha2.csv')
# dg.to_csv('test_file_alpha2_dg.csv')
#print(df)

# pin = df['object'].value_counts(normalize=False)['Person']
# 
# print('Persons = ')
# print(pin)
dg.plot(x = "days", y = "persons", kind = "bar")
    
print("I'm done")



