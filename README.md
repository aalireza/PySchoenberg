# PySchoenberg
Twelve-Tonic Atonalizer and Encoder

This program atonalizes the tonal music by preserving the elements of the original music such as rhythm, texture, dynamics, and timbre but changing each pitch so that the musical lines follow Schoenberg's 12-tone technique. Users may enjoy a unique experience of listening to atonalized music that was originally written tonally. PySchoenberg also facilitates the process of writing 12-tone music and allows composers to write with an ease and speed that would not be possible otherwise. It could also encode AES-128 ciphertexts as sheet music!

---
<h3> How it is implemented? </h3>
You may first want to read the Wikipedia entry here for the basics. The building block of the 12-tone technique is the tone row, which is an ordered arrangement of all chromatic scale notes occurring only once within the row. The tone row may appear in four different forms of Prime, Retrograde, Inversion, and Retrograde-Inversion. The tone row and its forms may be freely transposed in any degree of the chromatic scale. Any pitch in the set also can be composed in any octave. To access all the possible rows, a 12-tone matrix is generated. Then, each block of 12 pitches in the original music would be replaced with a randomly chosen series of the 12-tone matrix. 

<h3> Musical Outcome </h3>

The fact that PySchoenberg follows the strict principals of 12-tone technique allows for producing a music that is slightly different from commonplace method of writing 12-tone music, which is not that limited by strict 12-tonic principals. To give an example, PySchoenberg follows the principle of not repeating a pitch until all other pitches have been used in the set. However, repeating the same note or group of notes in succession is customary in this style. Also, as a coincidence, some sets may be used simultaneously in different parts that cause certain tonal relations between the notes (e.g. triads or harmonic elements) that a composer would avoid using. The result of the atonalized music sounds unique and unusual since, regardless of the pitches, the rhythm and contour of the new music belongs to a tonal one. Moreover, for the sake of simplicity this program uses only the sharp symbol (♯) as the accidental.


<h3> Composing Benefits </h3>

PySchoenberg by skipping the cumbersome process of manually plugging in 12-tone rows saves composers a tremendous amount of time and energy and allows them to focus on structure, rhythm, contour, and other important aspects of their composition. By automating the process of atonalizing, this program affects the volume of atonal and12-tone music composers will be able to produce and helps composers enrich and diversify the current repertoire of 12-tone music. 

<h3> Encoder </h3>

For the encoding implementation, first a message is encrypted with AES-128 (implementation in ./src/aes.py) in base 24. Then all of the possible numbers from 0 to 23 are assigned to a valid path on the 12-tone matrix. Then, each block of 12 pitches in the original music would be replaced by the path of each character of the ciphertext. If there are more blocks of 12 pitches, they all would be removed
<b>Remark: </b>The result of encoding a ciphertext would not be perfectly twelve-tonic since almost always the
number of notes in a sheet is not divisible by twelve.

<b>Remark: </b>For decoding, you need two keys. You actuall encryption key to decrypt the AES encrypted message, 
and your encoding key which is a random permutation of notes of the chromatic scale. It is needed to generated the
exact 12-tone matrix which was created to encode the ciphertext.

---
<h3> Prerequisites </h3>
- Python 2.7
- [Music21](https://code.google.com/p/music21/downloads/list): Twelve-tone matrix is created by this module. You may also install it via pip.
- [lxml 3.3.6](https://pypi.python.org/pypi/lxml/3.3.6): Needed to parse MusicXML files. Newer versions should be fine as well, theoretically. You may also install it via pip.
- [PyCrypto](https://pypi.python.org/pypi/pycrypto): Needed for AES Encryption/Decryption
- [MuseScore](http://musescore.com)
- [Audiveris 4.2.3](https://kenai.com/projects/audiveris/downloads/directory/oldies): The optical music recognition software.

<b>Remark: </b>This has only been tested on Ubuntu and Arch linux, though in theory it sould work on OS X as well.
If you have Windows, you need to go through the source code yourself and translate all of the system commands 
yourself.

---
<h3> Warning </h3>
It's better to not import anything in pdf or jpg format since the optical music recognition softwares 
are very faulty. The optimal format to be used with this program is MusicXML, which you'll be able to find plenty
of it in [MuseScore's library](http://musescore.com/sheetmusic). "mxl" and "mscz" formats are fine as well.

---
<h3> How to work with it </h3>

Clone this locally or download it as zip (link to your right). First go to ./config.txt and change what you need. Then cd into .src i.e.
``` cd ~/PATH TO MAIN FOLDER/PySchoenberg/src/ ``` then 
``` python main.py -f ABSOLUTE-PATH-TO-YOUR-FILE ```. The rest should be obvious (you may press 'h' there for
help).

<b>Remark: </b> -r switch can be used to remove stuff from ./data/*/*

<b>Remark: </b> This program will not overwrite stuff for the sake of saving different atonalized versions of a file, however you should purge whatever you have created after you're done with it to avoid confusion.

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

<b>Credits: </b> "Parham Pourdavood" had the original idea of automating 12-tone technique to atonalize tonal music while preserving the rhythm and metric structure of the original music. 
This was a hackathon project which was created for SBHacks 2015 [(Link  is here)](http://challengepost.com/software/modern-mozart). 

<b>Disclaimer: </b> Since PySchoenberg was originally a hackathon project (albeit the design decisions has been changed considerably) and also my first relatively non-trivial project, the coding quality may not be ideal.
