# music-catalogue
A messy little script that compiles the metadata of my music library into a handy CSV file. Written in R and Python.

* **filter.R** compiles all the filepaths of the music files, filtering out files that aren't included in the *format* variable.
* **meta.py** uses Python libraries to extract metadata, including Title, Artist, Album, Genre, Bitrate, Duration and Year.

The program uses the following libraries/packages.
* *tidyr* (R)
* *dplyr* (R)
* *time* (Python)
* *mutagen* (Python)
* *os* (Python)
* *audio-metadata* (Python)
* *pandas* (Python)
