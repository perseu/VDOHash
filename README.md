# VDOHash
This is a python script created to validate video files.
It first creates a text file with the hashes of the frames of the video so that later if someone claims to have that video file. One can use the file with the hash of the frames to check if the video file is valid, or if the video was altered.
The steps to use this are as follow:
First step create a text file that contains the hashs of the frames of the video file, and store that file that contain the hashs.
Example: VDOhash.py r=promnight.mp4 o=promnighthash.txt

Second step is the validation of a video file. One uses the file that contains the hashs to validate the video file.
Example: VDOhash.py t=Carriepromnight.mp4 i=promnighthash.txt

If promnight.mp4 and Carriepromnight.mp4 are the same, all the hash calculated on the second file should be the same as in ones on the text file promnighthash.txt, 
hence proving that promnight.mp4 and Carriepromnight.mp4 are the same file, and if that was your prom night... well... sorry about that because Carrie is a horror movie. :-\

The arguments are as follow:
     r - reference video. Or video that creates the list hash values.
     t - video to be validated. It's the video that we're attempting to see if it is the same as the reference.
     o - Hash output file.
     i - Input hash reference file.
     h - Help
     
Requirements:
OpenCV
