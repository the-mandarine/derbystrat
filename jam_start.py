#!/usr/bin/env python
from derbystrat.track import Track

def main():
    track = Track(shift=-30)
    track.lines()

    track.skater(3.6, 1.1)
    track.skater(1.5, 1.6)
    track.skater(1.5, 2.3)
    track.skater(3.6, 2.8)

    track.skater(10, 2.5, color="grey")
    track.skater(10, 3.5, color="grey")
    track.skater(12.6, 2.5, color="grey")
    track.skater(12.6, 3.5, color="grey")

    # Jammers
    track.skater(-1.6, 3.8, jammer = True)
    track.skater(-3, 1.5, color="grey", jammer = True)

    track.show()
    track.save("/tmp/track.png")

if __name__ == '__main__':
    main()
