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
from datetime import datetime

def search_photos():
    import tkinter as tk
    m = tk.Tk()
    m.title('search')
    search = tk.Button(m, bg='#45a2ff', text ='search my photos!', width = 20, height = 5)
    search.pack()
    m.mainloop()


search_photos()
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
   
    df = pd.DataFrame(columns =('filename', 'label', 'score'))
    response_label = client.label_detection(image=get_pic(my_filename))
#     image2 = vision_v1.Image(content = get_pic(my_filename))
# 
# 
#     response_label = client.label_detection(image=image2)


    for label in response_label.label_annotations:
        print({'label': label.description, 'score': label.score})
        my_row = pd.DataFrame([[my_filename, label.description,label.score]], columns = df.columns)
        #print(my_row)
        df = df.append(my_row, ignore_index = True)
    
    
    return df

def my_object(my_filename):
    
    df = pd.DataFrame(columns =('filename', 'object', 'score', 'time'))
    columns_a= ('filename', 'object', 'score')
#     image2 = vision_v1.Image(content = get_pic(my_filename))

    objects = client.object_localization(image=get_pic(my_filename)).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        my_row = pd.DataFrame([[my_filename, object_.name,object_.score]], columns = columns_a)
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
    texts = response.text_annotations
    
    print('Texts:')

    for text in texts:
        my_row = pd.DataFrame([[my_filename, text.description]], columns = ['filename', 'text'])
        df = df.append(my_row, ignore_index = True)
        
        if "202" in text.description:
            print('found date')
            '''extract the date into date format'''
            
            this_date = text.description
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

    my_datetime = this_date + ' ' + this_time
    print(my_datetime)
    newdatetime = datetime.strptime(my_datetime,'%Y/%m/%d %H:%M:%S')
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))     
    

    df.loc[:,'time']=newdatetime
    print(type(newdatetime))
    print(newdatetime)  # printed in default format
    return newdatetime     
         
def my_photos(directory):
    df = pd.DataFrame(columns =('filename', 'object', 'score','time'))
    columns_a = ('filename', 'object', 'score')
    for filename in os.listdir(directory):
        newpath = os.path.join(directory,filename)
        df = df.append(my_object(newpath),ignore_index = True)
        
#         df.iloc[-1]['time'] = my_detect_text(os.path.join(directory, filename))
        df.loc[newpath,'time'] =  my_detect_text(newpath)
    return df

        
directory1 = r'C:\Users\jaqua\Pictures\Saved Pictures\2017\12'    
directory = r'C:\Users\jaqua\Downloads\test'
fname1 = '20210124_123122.jpg'
fname2 = 'Normal-People.jpg'
fname3 = 'DSCF0001.jpg'

#df = my_object(fname1)
print('my detect text for file: ')
print(fname3)
df = my_detect_text(fname3)
print(df)
#pin = df['object'].value_counts(normalize=False)['Person']
#print(pin)

df = my_photos(directory)
n = len(pd.unique(df['filename']))
df['object'].value_counts(normalize=True)
print(df)
# pin = df['object'].value_counts(normalize=False)['Person']
# 
# print('Persons = ')
# print(pin)

print("I'm done")



