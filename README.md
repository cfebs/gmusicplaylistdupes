# kill google music playlist duplicates

Queries every user playlist and tries to remove duplicates via a playlist `trackId`

> **Use with caution**, I have tested this on my own playlists, but please start small
with a few tests in your library. I am not responsible for any damage to your library


### Quick usage

- [Download the script: https://raw.githubusercontent.com/cfebs/gmusicplaylistdupes/master/kill_playlist_dupes.py](https://raw.githubusercontent.com/cfebs/gmusicplaylistdupes/master/kill_playlist_dupes.py)
- `pip install gmusicapi`
- `python kill_playlist_dupes.py`

> Once you have gmusicapi installed, you can also use this oneliner: `python <(curl -sL https://raw.githubusercontent.com/cfebs/gmusicplaylistdupes/master/kill_playlist_dupes.py)`

Output will look something like this:

```
Processing playlist "Ska"

Found 64 dupe tracks out of 96 total in playlist "Ska"
Clean this up? (y/N) n
Moving on...
================================================================================

Processing playlist "Quality Hip-Hop"

Found 128 dupe tracks out of 192 total in playlist "Quality Hip-Hop"
Clean this up? (y/N) y
Removed 128 entries
```

User input is required to confirm track deletion.

### Advanced

If you would like to test without hitting the api every time, you can create a dump of the playlist response:

```
GMUSIC_WRITE_TEST_FILE=~/playlist_test.json python kill_playlist_dupes.py
```

And then you may use this test dump json to test the duplication prompts and output:

```
GMUSIC_DUPE_TEST_FILE=~/playlist_test.json python kill_playlist_dupes.py
```

To show individual unique and duplicate track information while processing playlists

```
GMUSIC_DUPE_SHOW_TEST_INFO=1 python kill_playlist_dupes.py
```

> Note: additional track information (artist, album, title) is printed if available.
> for some reason certain playlists do not have this information, in this case only the `trackid`
> is printed.

### Sources

- https://medium.com/@sebvance/how-to-remove-duplicates-from-your-google-music-library-593affef6dd1#.4qnjct1hu
- https://gist.github.com/sebvance/060da84f55b13837b310
- https://github.com/maxkirchoff/google-music-dupe-killer
- Api methods: https://github.com/simon-weber/gmusicapi/blob/develop/gmusicapi/clients/mobileclient.py
