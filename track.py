#!/usr/bin/env python
from __future__ import division
from PIL import Image, ImageDraw
from math import pi, cos, sin
from collections import Iterable

# Sizes are in feet
# Pivot line interior is 0
# All sizes are from the infield

S=15
X_MAX = 0
OUTLINE = "black"
LINES = "magenta"
BACK = "beige"
FRONT = "white"

def get_approx(x, x_beg, x_end, max_beg, max_end):
    deg = (x - x_beg) / (x_end - x_beg)

class Track(object):
    def __init__(self):
        self.scale = 10
        self.len = 108
        self.wid = 75
        self.mark_dist = 17.5
        self.int_radius = 12.5
        self.ext_radius = 26.5
        self.int_ext_shift = 1
        self.small_breadth = 13
        self.large_breadth = 15

    def draw(self, img):
        self.img = img
        self._draw_curves()
        self._draw_straights()

    def real_dim(self, dim):
        if isinstance(dim, Iterable):
            real_dim = tuple(self.real_dim(x) for x in dim)
        else:
            real_dim = self.scale*dim

        return real_dim

    def _draw_curves(self):
        img = self.img
        left_out_curve = (((self.len/2)-self.mark_dist-self.ext_radius),
                          ((self.wid/2)+self.int_ext_shift-self.ext_radius),
                          ((self.len/2)-self.mark_dist+self.ext_radius),
                          ((self.wid/2)+self.int_ext_shift+self.ext_radius))

        right_out_curve = (((self.len/2)+self.mark_dist-self.ext_radius),
                           ((self.wid/2)-self.int_ext_shift-self.ext_radius),
                           ((self.len/2)+self.mark_dist+self.ext_radius),
                           ((self.wid/2)-self.int_ext_shift+self.ext_radius))

        left_in_curve = (((self.len/2)-self.mark_dist-self.int_radius),
                          ((self.wid/2)-self.int_radius),
                          ((self.len/2)-self.mark_dist+self.int_radius),
                          ((self.wid/2)+self.int_radius))

        right_in_curve = (((self.len/2)+self.mark_dist-self.int_radius),
                          ((self.wid/2)-self.int_radius),
                          ((self.len/2)+self.mark_dist+self.int_radius),
                          ((self.wid/2)+self.int_radius))

        img.pieslice(self.real_dim(left_out_curve), 90, 270, FRONT, OUTLINE)
        img.pieslice(self.real_dim(right_out_curve), 270, 450, FRONT, OUTLINE)
        img.pieslice(self.real_dim(left_in_curve), 90, 270, BACK, OUTLINE)
        img.pieslice(self.real_dim(right_in_curve), 270, 450, BACK, OUTLINE)

    def _draw_straights(self):
        img = self.img
        top_out_left = (((self.len/2)-self.mark_dist),
                        ((self.wid/2)-self.int_radius-self.small_breadth))
        top_out_right = (((self.len/2)+self.mark_dist),
                         ((self.wid/2)-self.int_radius-self.large_breadth))
        top_in_left = ((self.len/2-self.mark_dist),
                       (self.wid/2-self.int_radius))
        top_in_right = (((self.len/2)+self.mark_dist),
                        ((self.wid/2)-self.int_radius))

        bottom_in_left = (((self.len/2)-self.mark_dist),
                          ((self.wid/2)+self.int_radius))
        bottom_in_right = (((self.len/2)+self.mark_dist),
                           ((self.wid/2)+self.int_radius))
        bottom_out_left = ((self.len/2-self.mark_dist),
                           (self.wid/2+self.int_radius+self.large_breadth))
        bottom_out_right = (((self.len/2)+self.mark_dist),
                            ((self.wid/2)+self.int_radius+self.small_breadth))


        top_straight = (top_out_left,
                        top_out_right,
                        top_in_right,
                        top_in_left)
        bottom_straight = (bottom_in_left,
                           bottom_in_right,
                           bottom_out_right,
                           bottom_out_left)

        img.polygon(self.real_dim(top_straight), FRONT, OUTLINE)
        img.polygon(self.real_dim(bottom_straight), FRONT, OUTLINE)

        # Let's erase black lines by putting colored lines on top
        img.line(self.real_dim((top_out_left, top_in_left)), FRONT)
        img.line(self.real_dim((top_out_right, top_in_right)), FRONT)
        img.line(self.real_dim((bottom_in_left, bottom_out_left)), FRONT)
        img.line(self.real_dim((bottom_in_right, bottom_out_right)), FRONT)
        img.line(self.real_dim((top_in_left, bottom_in_left)), BACK)
        img.line(self.real_dim((top_in_right, bottom_in_right)), BACK)

    def get_xy(x, pos=0.5, shift=0):
        """`x` is the middle distance from the start
           `pos` is position on the track. 0.0 is inside. 1.0 is outside
           `shift` is the shift position (if you want the track to start from the
           jammer line, us a `shift` of -30)"""
        pos_x = 0
        pos_y = 0
        end_first_curve = pi * 12.5
        end_first_line = end_first_curve + 35
        end_second_curve = end_first_line + pi * 12.5
        end_second_line = end_second_curve + 35

        end_of_track = 0
        x += shift
        x %= end_of_track

        lim_down = 0
        lim_up = end_first_curve
        min_width = 13
        max_width = 15
        ref_x = (108/2)-17.5
        ref_y = (75/2)
        angle_shift = -(pi/2)
        curve = True
        if end_first_curve <= x_int < end_first_line:
            # First line TODO
            print "Bottom line"
            lim_down = end_first_curve
            lim_up = end_first_line
            ref_x = (108/2)-17.5
            ref_y = (75/2)
            dim_shift = 1
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
            ref_x = (108/2)+17.5
            ref_y = (75/2)
            dim_shift = -1
            curve = False
        else:
            # First curve
            print "Left curve"

        prop = (x_int - lim_down) / (lim_up - lim_down)
        ref_len_min = 12.5

        if curve:
            ref_len_max = 12.5 + (((max_width - min_width) * prop) + min_width)
            ref_len = ((ref_len_max - ref_len_min) * pos) + ref_len_min
            angle = (prop * -2 * pi)/2 + angle_shift
            # Point defined by the arc of angle
            # of the circle of center (ref_x, ref_y) and radius ref_len
            pos_x = ref_len * cos(angle) + ref_x
            pos_y = ref_len * sin(angle) + ref_y
        else:
            ref_len_max = 12.5 + (((max_width - min_width) * (1-prop)) + min_width)
            ref_len = ((ref_len_max - ref_len_min) * pos * dim_shift) + ref_len_min * dim_shift
            pos_x = ref_x + (prop * 35 * dim_shift)
            pos_y = ref_y + ref_len
        return pos_x, pos_y

#def _draw_player(draw, x, y, size=3, color="yellow", outline="black"):
#    draw.ellipse((((x*S)-(size*S/2)),
#                  ((y*S)-(size*S/2)),
#                  ((x*S)+(size*S/2)),
#                  ((y*S)+(size*S/2))),
#                  fill=color,
#                  outline=outline)

def main():
    im = Image.new('RGBA', (108*10, 75*10), BACK)
    draw = ImageDraw.Draw(im)
    track = Track()
    track.draw(draw)

    # Jammers
#    x, y = get_xy(0, 0, shift=0)
#    _draw_player(draw, x, y, color="grey")

    im.show()

if __name__ == '__main__':
    main()
