#!/usr/bin/env python
from __future__ import division
from PIL import Image, ImageDraw
from math import pi, cos, sin

# Sizes are in feet
# Pivot line interior is 0
# All sizes are from the infield

S=10
X_MAX = 0
OUTLINE = "black"
LINES = "magenta"
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

    # Pivot line
    draw.line((top_out_left, top_in_left), LINES)
    # Jammer line
    jam_line = ((top_out_left[0]+(30*S), top_out_left[1]),
                (top_in_left[0]+(30*S), top_in_left[1]))
    draw.line(jam_line, LINES)

def get_approx(x, x_beg, x_end, max_beg, max_end):
    deg = (x - x_beg) / (x_end - x_beg)

def get_xy(x_int, pos=0, shift=0):
    """`x_int` is the inside distance from the start
       `pos` is position on the track. 0.0 is inside. 1.0 is outside
       `shift` is the shift position (if you want the track to start from the
       jammer line, us a `shift` of -30)"""
    pos_x = 0
    pos_y = 0
    end_first_curve = pi * 12.5
    end_first_line = end_first_curve + 35
    end_second_curve = end_first_line + pi * 12.5
    end_second_line = end_second_curve + 35
    x_int += shift
    x_int %= end_second_line

    lim_down = 0
    lim_up = end_first_curve
    ref_x = (108/2)-17.5
    ref_y = (75/2)
    min_width = 13
    max_width = 15
    angle_shift = -(pi/2)
    curve = True
    if end_first_curve <= x_int < end_first_line:
        # First line TODO
        print "Bottom line"
        lim_down = end_first_curve
        lim_up = end_first_line
        curve = False
    elif end_first_line <= x_int < end_second_curve:
        # Second curve TODO
        print "Right curve"
        lim_down = end_first_line
        lim_up = end_second_curve
        ref_x = (108/2)+17.5
        angle_shift = pi/2
        curve = True
    elif end_second_curve <= x_int < end_second_line:
        # Second line TODO
        print "Top line"
        lim_down = end_second_curve
        lim_up = end_second_line
        curve = False
    else:
        # First curve
        print "Left curve"

    prop = (x_int - lim_down) / (lim_up - lim_down)
    ref_len_min = 12.5
    ref_len_max = 12.5 + (((max_width - min_width) * prop) + min_width)
    #ref_len_max = 12.5 + 13
    ref_len = ((ref_len_max - ref_len_min) * pos) + ref_len_min
    print prop, pos, ref_len

    if curve:
        angle = (prop * -2 * pi)/2 + angle_shift
        # Point defined by the arc of angle
        # of the circle of center (ref_x, ref_y) and radius ref_len
        pos_x = ref_len * cos(angle) + ref_x
        pos_y = ref_len * sin(angle) + ref_y
    else:
        pass
    return pos_x, pos_y

def _draw_player(draw, x, y, size=20, color="yellow", outline="black"):
    draw.ellipse((((x*S)-(size/2)),
                  ((y*S)-(size/2)),
                  ((x*S)+(size/2)),
                  ((y*S)+(size/2))),
                  fill=color,
                  outline=outline)

def draw_track(draw):
    """Cf. Appendix A"""
    _track_curves(draw)
    _track_straights_clean(draw)



def main():
    im = Image.new('RGBA', (108*S, 75*S), BACK)
    draw = ImageDraw.Draw(im)
    draw_track(draw)

    x, y = get_xy(100, 0, shift=0)
    _draw_player(draw, x, y)
#    x, y = get_xy(10, 1, shift=0)
#    _draw_player(draw, x, y)
#    x, y = get_xy(20, 0, shift=0)
#    _draw_player(draw, x, y)

    print x, y
    _draw_player(draw, x, y)

    im.show()

if __name__ == '__main__':
    main()
