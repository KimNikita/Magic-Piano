import os
import sys
from piano_key import PianoKey


def main():
    path = os.path.abspath('sound')
    a = PianoKey(0, 0, 100, 100, 'C4', path, 1000, 1000)
    b = PianoKey(0, 0, 100, 100, 'D4', path, 1000, 1000)
    c = PianoKey(0, 0, 100, 100, 'E4', path, 1000, 1000)
    d = PianoKey(0, 0, 100, 100, 'F4', path, 1000, 1000)
    e = PianoKey(0, 0, 100, 100, 'G4', path, 1000, 1000)
    f = PianoKey(0, 0, 100, 100, 'A4', path, 1000, 1000)
    k = PianoKey(0, 0, 100, 100, 'B4', path, 1000, 1000)

    while True:
        a.play_sound()
        b.play_sound()
        c.play_sound()
        d.play_sound()
        e.play_sound()
        f.play_sound()
        k.play_sound()


if __name__ == '__main__':
    sys.exit(main() or 0)
