# PySchoenberg
Twelve-Tonic Atonalizer and Encoder

This program atonalizes the tonal music by preserving the rhythm but changing each pitch according to Schoenberg's
12-tone technique. It could also encode AES-128 ciphertexts as sheet music!

---
<h3> How is it implemented? </h3>
You may first want to read the Wikipedia entry [here](https://en.wikipedia.org/wiki/Twelve-tone_technique) for the
basics. 
The basis for creation of the tone row for atonalizing is a random permutation of the 12 notes of the chromatic
scale to form an ordered list. Then each note would be transposed and a 12-tone matrix would be generated. Then, each
block of 12 pitches in the original music would be replaced with a randomly chosen valid path on the 12-tone matrix's
rows (i.e. right to left or left to right).
As for the encoding implementation, first a message is encrypted with AES-128 (implementation in ./src/aes.py) in 
base 24. Then all of the possible numbers from 0 to 23 are assigned to a valid path on the 12-tone matrix. Then, each
block of 12 pitches in the original music would be replaced by the path of each character of the ciphertext. If there
are more blocks of 12 pitches, they all would be removed.

<b>Remark: </b>For the sake of simplicity, though, this program uses only "sharp" as the accidental of each note and does not use "flat" although by definition, "normal" would not cause problems.

<b>Remark: </b>Things like repeat signs make the outcome to not be perfect twelve-tonic.

<b>Remark: </b>The result of encoding a ciphertext would not be perfectly twelve-tonic since almost always the
number of notes in a sheet is not divisible by twelve.

<b>Remark: </b>For decoding, you need two keys. Your actual encryption key to decrypt the AES encrypted message, 
and your encoding key which is a random permutation of notes of the chromatic scale. It is needed to generated the
exact 12-tone matrix which was created to encode the ciphertext.

---
<h3> Dependencies: </h3>
- Python 2.7
- [Music21](https://pypi.python.org/pypi/music21): Twelve-tone matrix is created by this module..
- [lxml](https://pypi.python.org/pypi/lxml)
- [PyCrypto](https://pypi.python.org/pypi/pycrypto): Needed for AES Encryption/Decryption.
- [MuseScore](http://musescore.com): Needed for sequencing MusicXML files and/or converting other variations of musical data (not pdf or jpg) into xml.
- [Audiveris 4.2.3](https://kenai.com/projects/audiveris/downloads/directory/oldies): (Optional) The optical music recognition software. If you don't install it, you won't be able to convert your sheet music from jpg or pdf to xml -which is the format that's used here to atonalize etc.

<b>Remark: </b> This program doesn't work on Windows.

---
<h3> Warning </h3>
It's better to not import anything in pdf or jpg format since the optical music recognition software 
are very faulty. The optimal format to be used with this program is MusicXML, which you'll be able to find plenty
of it in [MuseScore's library](http://musescore.com/sheetmusic). "mxl" and "mscz" formats are fine as well.

<b>Therefore</b> It'll almost always be impossible to retrieve a message if the encoded message is saved as pdf or jpg, since not a single note has to be missed/misread for the message to be recoverable. The only relatively practical solution is to manually rewrite the piece in a program like MuseScore and export it as xml!

---
<h3> How to work with it </h3>

1. Open up your terminal. Go to a directory you wish to install the program, then `git clone https://github.com/aalireza/PySchoenberg.git`
2. Go to the directory in which you've cloned the program during the step one. Then open up `config.txt`. You must fill in te sections for MUSESCORE_PATH, PLAYER_PATH and PDF_VIEWER and fill in the AUDIVERIS_PATH if you've installed the optional Audiveris program. Follow the instructions in config.txt to do so.
3. Now enter `python path-to-PySchoenberg-dir/src/main.py -f path-to-your-file`. (For example, if you have cloned PySchoenberg in your home directory and you have a file Fur_Elise.xml in your Downloads directory, then the command would be `python ~/PySchoenberg/src/main.py -f ~/Downloads/Fur_Elise.xml`)
4. The script of step 3 is interactive. You could press 'h' to see the options you have. 'a' is an option to atonalize the sheet. 'e' is to encode etc.

<b>Remark: </b> -r switch can be used to remove stuff from ./data/*/*

<b>Remark: </b> This program will not overwrite stuff for the sake of saving different atonalized versions of a file, however you should purge whatever you have created after you're done with it to avoid confusion.

<b>Remark: </b> If you've encoded something, the result in xml format would be saved in ./data/AES/ therefore you'll need to point to that file when trying to open up the program to decode.

---
<h3> Sample Music Files </h3>

Notice that the Atonalized versions of Mozart's Turkish March and the Batuque share the same form(!).

+ [Atonalized Mozart's Turkish March]
(https://www.dropbox.com/s/fg7pjsj6fzy48w0/rondo_Atonalized-1.mp3?dl=0)
Also, its normal/tonal version is  [here]
(https://www.dropbox.com/s/u1ju2k6anzrao6e/Normal_Rondo_Alla_Turca_Turkish_March.mp3?dl=0)

+ [Atonalized Beethoven's Moonlight SonataMvt3 (Version#1 (Regular Tempo: Presto agitato), Complete)](https://www.dropbox.com/s/r17hab1p37ziic8/Moonlight_Sonata_3rd_Movement_-_Ludwig_van_Beethoven_Atonalized-0.mp3?dl=0) Also its normal/tonal version is [here](https://www.dropbox.com/s/71zm6parsfavbe4/Normal_Moonlight_Sonata_3rd_Movement.mp3?dl=0).

+ [Atonalized Beethoven's Moonlight SonataMvt3 (Version#2 (Slower Tempo: Moderato, different note row than above), First Page)](https://www.dropbox.com/s/25ooxiionty9mnw/file-0_Atonalized-0.mp3?dl=0)
+ [A Batuque](https://www.dropbox.com/s/q98dz55cz2ee2p3/batuque_Atonalized-0.mp3?dl=0) Also its original/unaltered version which was taken from Arudiveris' library is [here](https://www.dropbox.com/s/jxkvp8eo184j3al/batuque_original.mp3?dl=0)

<h3> Sample Sheet Music </h3>

+ [Normal Mozart's Turkish March]
(https://www.dropbox.com/s/3a7y3ckr8i4nnbd/Normal_Rondo_Alla_Turca_Turkish_March_Complete.pdf?dl=0)
+ [Atonalized Mozart's Turkish March]
(https://www.dropbox.com/s/f2ecsnky2zo6a9s/rondo_Converted-1_Atonalized-0_Converted-0.pdf?dl=0)

---

<b>Credits: </b> This was a hackathon project which was created for SBHacks 2015 [(Link  is here)](http://challengepost.com/software/modern-mozart). "Parham Pourdavood" had the original idea of using 12-tones to atonalize musical sheets while saving the rhythm and "Ahmed Shehata" was creating a front-end GUI with Java which was not finished.

<b>Disclaimer: </b> Since it was originally a hackathon project (albeit the design decisions has been changed considerably) and also my first relatively non-trivial project, the coding quality may not be ideal.
