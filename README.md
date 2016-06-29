# kill google music playlist duplicates

Queries every user playlist and tries to remove duplicates via a playlist `trackId`

### Quick usage

```
pip install gmusicapi
python kill_playlist_dupes.py
```

Output will look something like this:

```
Processing playlist "killer"
Found 0 dupe tracks out of 3 total
================================================================================

Processing playlist "SURF"
Found 2 dupe tracks out of 29 total
These tracks are unique:
No track info, id:8a9571bd-ceac-3af9-bc97-48ab15b9dfc8
No track info, id:866b62ab-1d32-3879-a88b-fbf8c973b33d
No track info, id:c22afb02-59c5-3532-a528-bfa8302267e0
No track info, id:e7d31c90-38a0-3dde-aea2-8958ce0a6b31
No track info, id:ea8daaee-2596-3e92-93bd-9f8c4efc01b9
No track info, id:934d8e8f-b447-36fa-83e5-020a50f68fa4
No track info, id:cf5950b5-5b41-3258-a39b-6fd5be7906da
No track info, id:8462f1e5-06ce-3ade-bd60-a65f42949ffa
No track info, id:52d228be-9763-3aba-9492-ed1327773365
No track info, id:a2ed0d3f-9ca4-39d3-b5fe-d4a4fa56bcc6
No track info, id:3bcf321f-9560-374b-be03-796e53707245
No track info, id:6812772d-0952-37e6-bb71-2d045a24e077
No track info, id:be0b3d24-320f-3823-8a21-3029d45e5ab2
No track info, id:4f2066a1-5f20-3e51-aea3-5aea2415463d
No track info, id:7e113c9a-98e6-3fa6-ab7c-2f99c6ccfecd
No track info, id:91c46ff3-af3d-32f0-968e-a0bc50d11722
No track info, id:34445b1b-05d6-3f88-9f3b-b0595650f303
No track info, id:938e93e4-61cc-3080-b5e0-f51113d9204c
No track info, id:dfba714a-61c3-33ed-8696-19230f369646
No track info, id:8608fd01-d09e-3d41-9845-8e5bd147e1b1
No track info, id:1e48b964-886e-3966-8131-8d91ea4a8bf8
No track info, id:5c7efcab-a55f-3572-8c4f-5ad9781aa598
No track info, id:7753e971-0c94-3369-8c03-a3f0ace40f12
No track info, id:84e64539-1690-32de-b68f-3a3543718e3d
No track info, id:a6b11121-43d5-3b49-b02e-3790bcf455c9
No track info, id:08d82d70-13f1-39cb-be30-eb3b442555af
No track info, id:ded553bf-855d-32b9-9024-0979c67e5441

These tracks are duplicates!!:
No track info, id:a2ed0d3f-9ca4-39d3-b5fe-d4a4fa56bcc6
No track info, id:938e93e4-61cc-3080-b5e0-f51113d9204c
Clean this up? [y/N]
```

User input is required to confirm track deletion.

> `No track info` is displayed when there is no detailed track (artist, album, title) about the track.
> 


### Advanced

If you would like to test without hitting the api every time, you can create a dump of the playlist response:

```
GMUSIC_WRITE_TEST_FILE=~/playlist_test.json python kill_playlist_dupes.py
```

And then you may use this test dump json to test the duplication prompts and output:

```
GMUSIC_DUPE_TEST_FILE=~/playlist_test.json python kill_playlist_dupes.py
```

### Sources

- https://medium.com/@sebvance/how-to-remove-duplicates-from-your-google-music-library-593affef6dd1#.4qnjct1hu
- https://gist.github.com/sebvance/060da84f55b13837b310
- https://github.com/maxkirchoff/google-music-dupe-killer
- Api methods: https://github.com/simon-weber/gmusicapi/blob/develop/gmusicapi/clients/mobileclient.py
