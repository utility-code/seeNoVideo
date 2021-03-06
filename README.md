# SeeNoVideo

- A text based basic video editing program
- Created in python + ffmpeg backend
- Please do read this document for syntax and capbilites

# Installation
- pip install seenovideos
- [PYPI](https://pypi.org/project/seenovideos/)
- Grab all the required programs from the list [Requirements]

## Features so far
- Simple text based syntax : just write down what you want
- Works for audio/video (Same syntax. Just change filenames)
- Video stabilization
- Add audio
- Merge videos with individual settings
- Remove audio or replace with another
- Resize the video
- Speed up/slow down audio and video

## Syntax
- Note: here testVideos is the folder where I have my video files (so I dont have to specify the full path)
- Note: commands.txt is the name of the file where I can have my string instead of directly passing it.
- The most basic way to run it is
```sh
python -m seenovideo -f testVideos/ -t commands.txt 
```
Here, commands.txt has the string required.
- If you want to directly supply the string instead
```sh
python -m seenovideo -f testVideos/ -d -t "{name:venus.mp4,A:0,}+{name:grassTutorialNew.mp4,A:0,resize:128;128,}"
```
- To specify an output file name if youre merging videos add -o "filename.mp4"

## Supported options
- example syntax: 
{
name: file.mp4,
resize: 128;128,
}
- stabilize:1       for video stabilization  (this requires [vidstab](https://github.com/georgmartius/vid.stab))
- resize: size1,size2        for resizing
- trim:00-01-00;00-5-10     format: hh:mm:ss; hh:mm,ss  for start and end time of trimming the video
- speedV: multiplier        speed up video by a factor of the multipler (eg: 2)
- speedA: multiplier        speed up audio by a factor of the multipler (eg: 2)
- Merge multiple videos by
```py
{name:file1.mp4}+{name:grassTutorialNew.mp4}
```
        - Note that each of these videos can have their own arguments

## Demos
- Do check the demo.ipynb notebook
- note that since the demos are in a notebook the function call is a bit different. For proper syntax check the above section

## Requirements
- Linux/MacOS/WSL
- python of course
- ffmpeg
- [vidstab](https://github.com/georgmartius/vid.stab) for video stabilization

## FAQ

- WTF are you nuts?
        - You know what. I probably am. But basic video edit is too much work.
- Why.
        - This is for basic video editing. Why bother getting a UI and everything when you can just write it in a text file and be done with it?

## Contribution Guidelines
- Can I contribute? YES
- What do I need to do? First file an issue with a suggestion. Fork it. Code. Drop a PR
- Suggestions? File a PR
