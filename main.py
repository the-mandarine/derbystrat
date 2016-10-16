#!/usr/bin/env python
from track import Track

def main():
    track = Track()
    track.lines()

    for i in range(10):
        track.skater(i*5+3, pos = 1, color="red")
        track.skater(i*5+3, pos = 2, color="green")
        track.skater(i*10+3, pos = 3, color="yellow")
        track.skater(i*10+3, pos = 4, color="blue")

    track.show()
    track.save("/tmp/track.png")

if __name__ == '__main__':
    main()
