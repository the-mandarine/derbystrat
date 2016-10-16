#!/usr/bin/env python
from __future__ import division
from PIL import Image, ImageDraw
from math import pi, cos, sin, sqrt
from collections import Iterable

# Sizes are in feet
# Pivot line interior is 0
# All sizes are from the infield

X_MAX = 0
OUTLINE = "black"
LINES = "magenta"
BACK = "beige"
FRONT = "white"

def get_approx(x, x_beg, x_end, max_beg, max_end):
    deg = (x - x_beg) / (x_end - x_beg)

class Track(object):
    def __init__(self, shift = 0, lanes = 4, scale = 10):
        self.scale = scale
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
        self.lanes = lanes
        self.im = Image.new('RGBA', (self.len*self.scale, self.wid*self.scale),
                            BACK)
        self.img = ImageDraw.Draw(self.im)

    def show(self):
        self.im.show()

    def save(self, filename):
        self.im.save(filename)

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
        top_out_left = self.get_xy(0, self.lanes+0.5, -self.shift)
        bottom_in_left = self.get_xy(self.curve_length, 0.5, -self.shift)
        bottom_out_left = self.get_xy(self.curve_length, self.lanes+0.5,
                                      -self.shift)
        bottom_in_right = self.get_xy(self.curve_length + self.line_length,
                                      0.5, -self.shift)
        bottom_out_right = self.get_xy(self.curve_length + self.line_length,
                                      self.lanes+0.5, -self.shift)
        top_in_right = self.get_xy((2 * self.curve_length) + self.line_length,
                                      0.5, -self.shift)
        top_out_right = self.get_xy((2 * self.curve_length) + self.line_length,
                                      self.lanes+0.5, -self.shift)

        top_straight = (top_out_left, top_out_right, top_in_right, top_in_left)
        bottom_straight = (bottom_in_left, bottom_in_right, bottom_out_right,
                           bottom_out_left)

        # Using polygons in order to color the track directly
        img.polygon(self.real_dim(top_straight), FRONT)
        img.polygon(self.real_dim(bottom_straight), FRONT)

        # Let's add black lines by putting colored lines on top
        img.line(self.real_dim((top_out_left, top_out_right)), OUTLINE)
        img.line(self.real_dim((top_in_left, top_in_right)), OUTLINE)
        img.line(self.real_dim((bottom_in_left, bottom_in_right)), OUTLINE)
        img.line(self.real_dim((bottom_out_left, bottom_out_right)), OUTLINE)
        # Erase black ligns due to ellipses
        img.line(self.real_dim((top_in_left, bottom_in_left)), BACK)
        img.line(self.real_dim((top_in_right, bottom_in_right)), BACK)

    def _draw_marks(self):
        img = self.img

        for mark in range(20):
            adv = mark * 10
            int_mark = self.get_xy(adv, self.lanes*0.55, -self.shift)
            ext_mark = self.get_xy(adv, self.lanes*0.70, -self.shift)
            # TODO find a better solution than this
            if not mark == 16:
                img.line(self.real_dim((int_mark, ext_mark)), OUTLINE)

        jam_line_int = self.get_xy(0, pos = 0.5, shift = (0 - self.shift))
        jam_line_ext = self.get_xy(0, pos = self.lanes+0.5,
                                   shift = (0 - self.shift))
        img.line(self.real_dim((jam_line_int, jam_line_ext)), OUTLINE)

        piv_line_int = self.get_xy(-30, pos = 0.5, shift = (0 - self.shift))
        piv_line_ext = self.get_xy(-30, pos = self.lanes+0.5,
                                   shift = (0 - self.shift))
        img.line(self.real_dim((piv_line_int, piv_line_ext)), OUTLINE)

    def get_xy(self, x, pos=2.5, shift=0):
        """`x` is the middle distance from the start
           `pos` is position on the track. 0.5 is inside. 4.5 is outside
           `shift` is the shift position (if you want the track to start from the
           jammer line, us a `shift` of -30)"""
        pos_x = 0
        pos_y = 0
        ref_y = self.wid/2
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
            ref_x = (self.len/2)-self.mark_dist
            angle_shift = -(pi/2)
            curve = True
        elif end_first_curve <= x < end_first_line:
            # First line
            lim_down = end_first_curve
            lim_up = end_first_line
            ref_x_beg = (self.len/2)-self.mark_dist
            ref_x_end = (self.len/2)+self.mark_dist
            dim_shift = 1
            curve = False
        elif end_first_line <= x < end_second_curve:
            # Second curve
            lim_down = end_first_line
            lim_up = end_second_curve
            ref_x = (self.len/2)+self.mark_dist
            angle_shift = (pi/2)
            curve = True
        elif end_second_curve <= x < end_second_line:
            # Second line
            lim_down = end_second_curve
            lim_up = end_second_line
            ref_x_beg = (self.len/2)+self.mark_dist
            ref_x_end = (self.len/2)-self.mark_dist
            dim_shift = -1
            curve = False

        posval_beg = self.small_breadth / self.lanes
        posval_end = self.large_breadth / self.lanes
        prop = (x - lim_down) / (lim_up - lim_down)
        if not curve:
            posval_beg, posval_end = posval_end, posval_beg
            ref_x = ((ref_x_end - ref_x_beg) * prop) + ref_x_beg

        posval = ((posval_end - posval_beg) * prop) + posval_beg
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

    def lines(self):
        self._draw_curves()
        self._draw_straights()
        self._draw_marks()

    def skater(self, adv, pos = 2.5, size=2, color="yellow", outline="black"):
        x, y = self.get_xy(adv, pos)
        self.img.ellipse((((x*self.scale)-(size*self.scale/2)),
                          ((y*self.scale)-(size*self.scale/2)),
                          ((x*self.scale)+(size*self.scale/2)),
                          ((y*self.scale)+(size*self.scale/2))),
                          fill=color,
                          outline=outline)

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
