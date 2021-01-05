#import libraries

library(dplyr)
library(tidyr)

#set undesirable folders, preferred formats and working directory

no_crawl <- c('Audio Music Apps', 'www.mp3accompanist.com',
            'Unknown Artist', 'iTunes',
            'Automatically Add to iTunes', 'Voice Memos',
            'GarageBand', 'Audio Music Apps')

formats <- c('.mp3', '.MP3', '.m4a', '.M4A', '.m4p',
           '.M4P', '.flac', '.FLAC', '.aac', '.AAC',
           'mp3', 'MP3', 'm4a', 'M4A', 'm4p',
           'M4P', 'flac', 'FLAC', 'aac', 'AAC')

setwd('~/Music/')

#set up data frame

all_files <- list.files(recursive = TRUE)
df <- data.frame(all_files, stringsAsFactors = FALSE)
new_df <- data.frame()
headers <- c('Title', 'Artist', 'Album', 'Year',
                 'Duration', 'Genre', 'Format', 'Bitrate')

#extract and filter out invalid entries

df <- df %>% separate(all_files, into = c('col1','col2'), sep = '/', extra = 'merge',fill = 'left')
df <- separate(data = df, col = col2, into = c('col2','col3'), sep = -4)

for (keyword in no_crawl){
  df <- df %>% filter(df[1] != keyword)
}

for (format in formats){
  set <- df %>% filter(df[3] == format)
  new_df <- bind_rows(new_df,set)
}

#merge back together, add columns and export

new_df <- unite(new_df, col = 'path', c('col1','col2'), sep = '/')
new_df <- unite(new_df, col = 'path', c('path','col3'), sep = '')

new_df[,headers] <- ''

write.csv(new_df, file = 'catalogue.csv', row.names = FALSE)