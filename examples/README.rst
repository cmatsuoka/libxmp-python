
Examples
--------

* player.py: A module player using pyaudio. This player uses the play_frame()
  method to play one frame per call.

  Usage: player.py <module file>::

    $ ./player.py cj-blue.zip
    Name: Blue Flame
    Type: Impulse Tracker 2.14 IMPM 2.00
    Instruments: 5   Samples: 28
      0 Bass / Rhythm Guitar              
      1 Lead Guitar                       
      2 Strings                           
      3 Drumkit                           
      4 Distorted Guitar                  
       1/ 42   44/ 64

* player2.py: Same as above, but using the play() method to play the entire
  module.

  Usage: player2.py <module file>


* callback.py: Same as above, but using the pyaudio callback and the
  play_buffer() method to play one buffer per call.

  Usage: callback.py <module file>


* info.py: List and identify module files.

  Usage: info.py <modules>::

    $ ./info.py *
    1942.mod                  Protracker (MOD)          1942
    4-MAT - Eternity.xm       Fast Tracker II (XM)      Eternity
    CJ-PURG1.IT               Impulse Tracker (IT)      Purgatory - Opening
    Deep In Her Eyes - Remake Impulse Tracker (IT)      Deep in her Eyes
    Kingdom.mod               Protracker (MOD)          kingdom of pleasure
    QUBE-Dpaint4Intro.mod     Startrekker (MOD)         tritris
    angie s.mod               Soundtracker (MOD)        angie s.
    bubble_bobble.mod         Protracker (MOD)          bubble bobble
    cj-blue.zip               Impulse Tracker (IT)      Blue Flame


* getsample.py: Extract samples from module files. If the instrument has more
  than one sample, all samples will be extracted to different wave files.

  Usage: getsample.py <module file> <instrument number>::

    $ ./getsample.py CJ-PURG1.IT 1
    Instrument 1 (Piano) has 4 samples
    Extract sample 0 as sample-01-00.wav (133994 bytes)
    Extract sample 1 as sample-01-01.wav (122421 bytes)
    Extract sample 2 as sample-01-02.wav (127232 bytes)
    Extract sample 3 as sample-01-03.wav (114800 bytes)


* showpattern.py: Dump pattern data.

  Usage: showpattern.py <module file> <pattern number>::

    $ ./showpattern.py hereyes_remake.zip 0
    PATTERN 00
    00|F#5 00|C#5 01|--- --|--- --|C#5 08|F#4 04|C#5 05|--- --|--- --|
    01|--- --|--- --|--- --|--- --|C#5 08|--- --|--- --|--- --|--- --|
    02|F#5 00|--- --|F#5 00|--- --|C#5 09|--- --|--- --|--- --|--- --|
    03|--- --|--- --|E 5 00|--- --|C#5 08|--- --|C#5 05|--- --|--- --|
    04|F#5 00|--- --|--- --|--- --|--- --|--- --|--- --|--- --|--- --|
    05|F#5 00|--- --|--- --|--- --|--- --|--- --|--- --|--- --|--- --|
    06|--- --|--- --|C#5 00|E 5 01|--- --|--- --|C#5 05|--- --|--- --|
    07|F#5 00|--- --|--- --|--- --|--- --|--- --|--- --|--- --|--- --|
    08|F#5 00|--- --|--- --|--- --|--- --|--- --|--- --|--- --|--- --|
    ...


* player_curses.py: Curses-based module player.

  Usage: curses_player.py <module file>::

    $ ./curses_player.py nearly_there_.mod
    Name: nearly there..                 Type: Protracker (M.K.)             
    Ins: 31   Smp: 31   Pos:  16/ 76   Row:   9/ 64
    
      1: by jogeir liljedahl    =============== 
      2:                        =============== 
      3: (c) noiseless 1993     ================
      4:                        ====            

