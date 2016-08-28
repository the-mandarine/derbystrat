#!/usr/bin/env python
from PIL import Image, ImageDraw
# Sizes are in feet
S=10
OUTLINE = "black"
BACK = "beige"
FRONT = "white"

def _track_curves(draw):
    left_out_curve = (((108/2)-17.5-26.5) * S,
                      ((75/2)+1-26.5) * S,
                      ((108/2)-17.5+26.5) * S,
                      ((75/2)+1+26.5) * S)
    draw.pieslice(left_out_curve, 90, 270, FRONT, OUTLINE)
    right_out_curve = (((108/2)+17.5-26.5) * S,
                       ((75/2)-1-26.5) * S,
                       ((108/2)+17.5+26.5) * S,
                       ((75/2)-1+26.5) * S)
    draw.pieslice(right_out_curve, 270, 450, FRONT, OUTLINE)
    left_in_curve = (((108/2)-17.5-12.5) * S,
                      ((75/2)-12.5) * S,
                      ((108/2)-17.5+12.5) * S,
                      ((75/2)+12.5) * S)
    draw.pieslice(left_in_curve, 90, 270, BACK, OUTLINE)
    right_in_curve = (((108/2)+17.5-12.5) * S,
                      ((75/2)-12.5) * S,
                      ((108/2)+17.5+12.5) * S,
                      ((75/2)+12.5) * S)
    draw.pieslice(right_in_curve, 270, 450, BACK, OUTLINE)

def _track_straights_clean(draw):
    top_out_left = (((108/2)-17.5) * S,
                    ((75/2)-12.5-13) * S)
    top_out_right = (((108/2)+17.5) * S,
                     ((75/2)-12.5-15) * S)
    top_in_left = ((108/2-17.5) * S,
                   (75/2-12.5) * S)
    top_in_right = (((108/2)+17.5) * S,
                    ((75/2)-12.5) * S)

    bottom_in_left = (((108/2)-17.5) * S,
                      ((75/2)+12.5) * S)
    bottom_in_right = (((108/2)+17.5) * S,
                       ((75/2)+12.5) * S)
    bottom_out_left = ((108/2-17.5) * S,
                       (75/2+12.5+15) * S)
    bottom_out_right = (((108/2)+17.5) * S,
                        ((75/2)+12.5+13) * S)


    top_straight = (top_out_left,
                    top_out_right,
                    top_in_right,
                    top_in_left)
    draw.polygon(top_straight, FRONT, OUTLINE)
    bottom_straight = (bottom_in_left,
                       bottom_in_right,
                       bottom_out_right,
                       bottom_out_left)
    draw.polygon(bottom_straight, FRONT, OUTLINE)

    # Let's erase black lines by putting colored lines on top
    draw.line((top_out_left, top_in_left), FRONT)
    draw.line((top_out_right, top_in_right), FRONT)
    draw.line((bottom_in_left, bottom_out_left), FRONT)
    draw.line((bottom_in_right, bottom_out_right), FRONT)
    draw.line((top_in_left, bottom_in_left), BACK)
    draw.line((top_in_right, bottom_in_right), BACK)

def draw_track(draw):
    """Cf. Appendix A"""
    _track_curves(draw)
    _track_straights_clean(draw)




def main():
    im = Image.new('RGBA', (108*S, 75*S), BACK)
    draw = ImageDraw.Draw(im)
    draw_track(draw)
    im.show()

if __name__ == '__main__':
    main()
