import audio_metadata
import pandas as pd
import os
import mutagen
import time

#Set directory, import dataframe, set datatypes

home = '/Users/calebtriscari/Music'
os.chdir(home)
cat = pd.read_csv('catalogue.csv')

cat['Title'] = cat['Title'].astype('string')
cat['Artist'] = cat['Artist'].astype('string')
cat['Album'] = cat['Album'].astype('string')
cat['Genre'] = cat['Genre'].astype('string')
cat['Format'] = cat['Format'].astype('string')
cat['Year'] = cat['Year'].astype('string')
cat['Duration'] = cat['Duration'].astype('string')

#assess file format and use appropriate library to extract information

for i in cat.index:
        path = cat['path'][i]
        filesplit = path.split('.')
        audio_format = filesplit[-1]
        cat.at[i, 'Format'] = audio_format

        if audio_format.lower() == 'm4a' or audio_format.lower() == 'm4p':
                try:
                        song = mutagen.File(path)

                        try:
                                title = song.tags['©nam'][0]
                                cat.at[i, 'Title'] = title
                        except:
                                title = 'Unavailable'
                                cat.at[i, 'Title'] = title

                        try:
                                artist = song.tags['©ART'][0]
                                cat.at[i, 'Artist'] = artist
                        except:
                                artist = 'Unavailable'
                                cat.at[i, 'Artist'] = artist

                        try:
                                album = song.tags['©alb'][0]
                                cat.at[i, 'Album'] = album
                        except:
                                album = 'Unavailable'
                                cat.at[i, 'Album'] = album

                        try:
                                year = song.tags['©day'][0]
                                year = year.split('-')
                                year = year[0]
                                cat.at[i, 'Year'] = year
                        except:
                                year = 'Unavailable'
                                cat.at[i, 'Year'] = year

                        try:
                                info = song.info.pprint()
                                info = info.split(',')
                                duration = info[1]
                                duration = duration.replace(' seconds', '')
                                duration = duration.strip()
                                duration = float(duration)
                                t = time.gmtime(duration)
                                duration = time.strftime('%M:%S', t)
                                cat.at[i, 'Duration'] = duration
                        except:
                                duration = 'Unavailable'
                                cat.at[i, 'Duration'] = duration

                        try:
                                genre = song.tags['©gen'][0]
                                cat.at[i, 'Genre'] = genre
                        except:
                                genre = 'Unavailable'
                                cat.at[i, 'Genre'] = genre

                        try:
                                bitrate = info[2]
                                bitrate = bitrate.replace(' bps','')
                                bitrate = bitrate.strip()
                                bitrate = int(bitrate)
                                bitrate = float(bitrate/1000)
                                cat.at[i, 'Bitrate'] = bitrate
                        except:
                                bitrate = None
                                cat.at[i, 'Bitrate']
                                
                except Exception as e:
                        print(e)
        else:
                try:
                        song = audio_metadata.load(path)

                        try:
                                title = song['tags']['title'][0]
                                cat.at[i, 'Title'] = title
                        except:
                                title = 'Unavailable'
                                cat.at[i, 'Title'] = title

                        try:
                                artist = song['tags']['artist'][0]
                                cat.at[i, 'Artist'] = artist
                        except:
                                artist = 'Unavailable'
                                cat.at[i, 'Artist'] = artist

                        try:
                                album = song['tags']['album'][0]
                                cat.at[i, 'Album'] = album
                        except:
                                album = 'Unavailable'
                                cat.at[i, 'Album'] = album

                        try:
                                year = song['tags']['date'][0]
                                cat.at[i, 'Year'] = year
                        except:
                                year = 'Unavailable'
                                cat.at[i, 'Year'] = year

                        try:
                                duration = song['streaminfo']['duration']
                                t = time.gmtime(duration)
                                duration = time.strftime('%M:%S', t)
                                cat.at[i, 'Duration'] = duration
                        except:
                                duration = 'Unavailable'
                                cat.at[i, 'Duration'] = duration

                        try:
                                genre = song['tags']['genre'][0]
                                cat.at[i, 'Genre'] = genre
                        except:
                                genre = 'Unavailable'
                                cat.at[i, 'Genre'] = genre

                        try:
                                bitrate = (song['streaminfo']['bitrate'])/1000
                                cat.at[i, 'Bitrate'] = bitrate
                        except:
                                bitrate = None
                                cat.at[i, 'Bitrate'] = bitrate

                except Exception as e:
                        print(e)

#Export dataframe

cat.to_csv('catalogue.csv', index = False)
