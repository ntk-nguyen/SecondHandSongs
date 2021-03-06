# SecondHandSongs

## Objectives

This application has two objectives:
* performs ETL(extract, translate, load) for a given datasets of songs and bands that have played them in a local SQLite 
database. 
* provides a GraphQL API to make it easy to look up what songs a band has played via a command line or a GraphQL interface.

## Dataset
The dataset was retrieved from the [**SecondHandSongs dataset**](http://millionsongdataset.com/secondhand/), the 
official list of cover songs within the Million Song Dataset.

The database will contain data from [SecondHandSongs train set](https://github.com/tb2332/MSongsDB/raw/master/Tasks_Demos/CoverSongs/shs_dataset_train.txt)
and the [list of artist](http://millionsongdataset.com/sites/default/files/AdditionalFiles/unique_artists.txt) stored in 
two different tables.

* **Songs**: the SHS dataset has a total of 18,196 tracks from the MSD, organized in "cliques", i.e. groups of versions 
of a single underlying musical work. Where possible, the cliques are referenced to "works" from the SHS site.

    The file format per line is:
    <br># - comment, ignore</br>
    <br>%a,b,c, title - beginning of a clique. a,b,c are work IDs (negative if not available)</br>
    <br>TID<SEP>AID<SEP>perf - track ID from the MSD (plus artist ID and SHS performance)</br>

* **Artists**: list of artists that have played the above songs.

There is a **one-to-many** relationship between songs and artists where an artist can play many songs.

## Project setup
This application uses ```Python 3.6.4``` with ```Flask```, ```Graphene```, and ```SQLAlchemy```.

```
# Clone the project
git clone https://github.com/ntk-nguyen/SecondHandSongs.git
cd .\SecondHandSongs\
mkdir database/data
# Downloading files
wget https://github.com/tb2332/MSongsDB/raw/master/Tasks_Demos/CoverSongs/shs_dataset_train.txt -OutFile database/data/shs_dataset_train.txt
wget http://millionsongdataset.com/sites/default/files/AdditionalFiles/unique_artists.txt -OutFile database/data/unique_artists.txt
# Create a virtualenv to isolate our package depencies locally
virtualenv env
# Activate the newly created virtualenv
.env\Scripts\activate # For use with Windows Powershell 
```

### Install dependencies
```
pip install -r requirements.txt
```

### Run setup.py to create a local database
```
python setup.py
```

## Usage
There are two ways to find what songs an artist has played:
* via command line
* via built-in GraphQL interface

##### Command line 
To search for what songs an artist has played through command line, run
```
>>> python command_line_query.py --h
usage: command_line_query.py [-h] [-a Artist ID]

Find songs that have been played by an artist

optional arguments:
  -h, --help    show this help message and exit
  -a Artist ID  Artist ID from the Second Hands Dataset
```

Example:
```
>>> python command_line_query.py -a ARXJJSN1187B98CB37
Artist ARXJJSN1187B98CB37 has played the following songs
        My Sweet Lord (MSD Track ID: TRPYNNL12903CAF506)
        Hark! The Herald Angels Sing (MSD Track ID: TRFMJLM12903CAF4FB)
        Silent Night (MSD Track ID: TRSKGOU12903CAF4FD)
        O Come All Ye Faithful (Album Version) (MSD Track ID: TRQSEJD12903CAF4F9)
```
##### GraphQL interface
Users can also use the GraphQL interface to search by running
```
>>> python app.py
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 281-170-868
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
Open your browser and navigate to ```http://127.0.0.1:5000/graphql``` .

**Find songs by an artist**: This query returns a list of songs by artist with ID ARXJJSN1187B98CB37
```
    {
	filterSongByArtist(artistId: "ARXJJSN1187B98CB37") {
	  msdTrackId
    artist{
      artistId
      artistName
    }
    performance
    title
	}
}
```
**Get list of songs**: This query returns a list of songs and other information
```
{
  songList {
    edges {
      node {
        msdTrackId
        artist {
          artistId
          artistName
        }
        performance
        title
      }
    }
  }
}
```
**Get list of artists**: This query returns a list of artists and other information
```
{
	artistList {
	  edges {
	    node {
	      artistId
        artistName
	    }
	  }
	}
}
```

## Unit Test
For unit test, run ```python test.py```