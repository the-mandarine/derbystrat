#!/usr/bin/env python
from __future__ import division
from PIL import Image, ImageDraw
from math import pi, cos, sin, sqrt
from collections import Iterable

# Sizes are in feet
# Pivot line interior is 0
# All sizes are from the infield

SCALE = 10
X_MAX = 0
OUTLINE = "black"
LINES = "magenta"
BACK = "beige"
FRONT = "white"

def get_approx(x, x_beg, x_end, max_beg, max_end):
    deg = (x - x_beg) / (x_end - x_beg)

class Track(object):
    def __init__(self, shift = 0):
        self.scale = SCALE
        self.len = 108
        self.wid = 75
        self.mark_dist = 17.5
        self.int_radius = 12.5
        self.ext_radius = 26.5
        self.int_ext_shift = 1
        self.small_breadth = 13
        self.large_breadth = 15
        self.shift = shift
        self.curve_length = pi * 19.1
        self.line_length = sqrt(35*35 + 1)

    def draw(self, img):
        self.img = img
        self._draw_curves()
        self._draw_straights()
        self._draw_marks()

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
        top_in_left = self.get_xy(0, 0.5, -self.shift)
        top_out_left = self.get_xy(0, 4.5, -self.shift)
        bottom_in_left = self.get_xy(self.curve_length, 0.5, -self.shift)
        bottom_out_left = self.get_xy(self.curve_length, 4.5, -self.shift)
        bottom_in_right = self.get_xy(self.curve_length + self.line_length,
                                      0.5, -self.shift)
        bottom_out_right = self.get_xy(self.curve_length + self.line_length,
                                      4.5, -self.shift)
        top_in_right = self.get_xy((2 * self.curve_length) + self.line_length,
                                      0.5, -self.shift)
        top_out_right = self.get_xy((2 * self.curve_length) + self.line_length,
                                      4.5, -self.shift)

        top_straight = (top_out_left,
                        top_out_right,
                        top_in_right,
                        top_in_left)
        bottom_straight = (bottom_in_left,
                           bottom_in_right,
                           bottom_out_right,
                           bottom_out_left)

        # Using polygons in order to color the track directly
        img.polygon(self.real_dim(top_straight), FRONT, OUTLINE)
        img.polygon(self.real_dim(bottom_straight), FRONT, OUTLINE)

        # Let's erase black lines by putting colored lines on top
        img.line(self.real_dim((top_out_left, top_in_left)), FRONT)
        img.line(self.real_dim((top_out_right, top_in_right)), FRONT)
        img.line(self.real_dim((bottom_in_left, bottom_out_left)), FRONT)
        img.line(self.real_dim((bottom_in_right, bottom_out_right)), FRONT)
        img.line(self.real_dim((top_in_left, bottom_in_left)), BACK)
        img.line(self.real_dim((top_in_right, bottom_in_right)), BACK)

    def _draw_marks(self):
        img = self.img

        for mark in range(20):
            adv = mark * 10
            int_mark = self.get_xy(adv, pos = 2.2)
            ext_mark = self.get_xy(adv, pos = 2.8)
            if not mark == 14:
                img.line(self.real_dim((int_mark, ext_mark)), OUTLINE)

        jam_line_int = self.get_xy(0, pos = 0.5, shift = (0 - self.shift))
        jam_line_ext = self.get_xy(0, pos = 4.5, shift = (0 - self.shift))
        img.line(self.real_dim((jam_line_int, jam_line_ext)), OUTLINE)

        piv_line_int = self.get_xy(-30, pos = 0.5, shift = (0 - self.shift))
        piv_line_ext = self.get_xy(-30, pos = 4.5, shift = (0 - self.shift))
        img.line(self.real_dim((piv_line_int, piv_line_ext)), OUTLINE)

    def get_xy(self, x, pos=2.5, shift=0):
        """`x` is the middle distance from the start
           `pos` is position on the track. 0.5 is inside. 4.5 is outside
           `shift` is the shift position (if you want the track to start from the
           jammer line, us a `shift` of -30)"""
        pos_x = 0
        pos_y = 0
        # linear approximation
        end_first_curve = self.curve_length
        # pythagore on trapezoid
        end_first_line = end_first_curve + self.line_length
        end_second_curve = end_first_line + self.curve_length
        end_second_line = end_second_curve + self.line_length

        end_of_track = end_second_line
        x += (self.shift + shift)
        x %= end_of_track

        if 0 <= x < end_first_curve:
            # First curve
            lim_down = 0
            lim_up = end_first_curve
            width_beg = 13
            posval_beg = width_beg / 4
            width_end = 15
            posval_end = width_end / 4
            ref_x_beg = ref_x_end = (108/2)-17.5
            angle_shift = -(pi/2)
            curve = True
        elif end_first_curve <= x < end_first_line:
            # First line
            lim_down = end_first_curve
            lim_up = end_first_line
            width_beg = 15
            posval_beg = width_beg / 4
            width_end = 13
            posval_end = width_end / 4
            ref_x_beg = (108/2)-17.5
            ref_x_end = (108/2)+17.5
            dim_shift = 1
            curve = False
        elif end_first_line <= x < end_second_curve:
            # Second curve
            lim_down = end_first_line
            lim_up = end_second_curve
            width_beg = 13
            posval_beg = width_beg / 4
            width_end = 15
            posval_end = width_end / 4
            ref_x_beg = ref_x_end = (108/2)+17.5
            angle_shift = (pi/2)
            curve = True
        elif end_second_curve <= x < end_second_line:
            # Second line
            lim_down = end_second_curve
            lim_up = end_second_line
            width_beg = 15
            posval_beg = width_beg / 4
            width_end = 13
            posval_end = width_end / 4
            ref_x_beg = (108/2)+17.5
            ref_x_end = (108/2)-17.5
            dim_shift = -1
            curve = False

        prop = (x - lim_down) / (lim_up - lim_down)
        posval = ((posval_end - posval_beg) * prop) + posval_beg
        ref_x = ((ref_x_end - ref_x_beg) * prop) + ref_x_beg
        ref_y = 75/2
        ref_len = 12.5 - (posval / 2) + (pos * posval)

        if curve:
            angle = (prop * -2 * pi)/2 + angle_shift
            # Point defined by the arc of angle
            # of the circle of center (ref_x, ref_y) and radius ref_len
            pos_x = ref_len * cos(angle) + ref_x
            pos_y = ref_len * sin(angle) + ref_y
        else:
            # Point defined to be vertically at ref_len distance of the
            # point (ref_x, ref_y).
            pos_x = ref_x
            pos_y = ref_y + (ref_len * dim_shift)
        return pos_x, pos_y

    def player(self, adv, pos = 2.5, size=2, color="yellow", outline="black"):
        x, y = self.get_xy(adv, pos)
        self.img.ellipse((((x*self.scale)-(size*self.scale/2)),
                          ((y*self.scale)-(size*self.scale/2)),
                          ((x*self.scale)+(size*self.scale/2)),
                          ((y*self.scale)+(size*self.scale/2))),
                          fill=color,
                          outline=outline)

def main():
    im = Image.new('RGBA', (108*10, 75*10), BACK)
    draw = ImageDraw.Draw(im)
    track = Track(shift = 20)
    track.draw(draw)

    # Jammers
    #p = Player(0, 0)
    for i in range(40):
        track.player(i*5+3, pos = 1, color="red")
        track.player(i*5+3, pos = 2, color="green")
        track.player(i*5+3, pos = 3, color="yellow")
        track.player(i*5+3, pos = 4, color="blue")



    im.show()

if __name__ == '__main__':
    main()
