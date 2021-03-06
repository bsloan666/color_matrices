#!/usr/bin/env python

# Copyright (c) 2016, Blake G. Sloan 
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

#   1.Redistributions of source code must retain the above copyright notice, 
#     this list of conditions and the following disclaimer.

#   2.Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation 
#     and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.

"""
This is a command-line utility for generating 3x3 matrices to transform linear 
RGB values from each eye of a Dolby Stereo 3D projector to P3 color space.

Measurements of CIE xy chromaticity pairs for R,G,B and W for each eye are 
provided through a json file (see test/measurements.json).

Resulting matrices are printed to the terminal output and can optionally by
written to their own json file. 
"""

import os
import sys
import numpy as np
import json
import math
from optparse import OptionParser

def parse_cmdline():
    parser = OptionParser()
    
    parser.add_option("-i", "--input", dest="infname",
                      help="Read left and right primaries and white point from json file")
    parser.add_option("-o", "--output", dest="outfname",
                      help="Write left and right compensation matrices to json file")
    parser.add_option("-t", "--test", dest="test", action="store_false",
                      help="Use dummy left/right primaries to test the program")

    return parser.parse_args()

def promote_xyz(a):
    """
    Add a 'z' coordinate to each xy pair
    """
    for p in a:
        p.append(1.0-p[0]-p[1])
    return a

def xyz_to_XYZ(v):
    """
    convert xyz to XYZ
    """
    V = [(1.0/v[1])*v[0], 1.0,(1.0/v[1])*v[2]]
    #print "XYZ val:",V
    return V

def primaries_to_XYZ(b):
    """
    Linear algebra bit. 
    Reference: http://www.ryanjuckett.com/programming/rgb-color-space-conversion/
    """
    c = b[0:3]
    bb = np.matrix(c)
    d  =  bb.T.I
    w =  np.matrix(xyz_to_XYZ(b[3])).transpose()
    v =  d*w
    diag_w = np.diagflat(v)
    return bb.T * diag_w 

def compute_norm(mat):
    m = mat.tolist()
    a = m[0][0]+m[0][1]+m[0][2]
    b = m[1][0]+m[1][1]+m[1][2]
    c = m[2][0]+m[2][1]+m[2][2]
    if a > b:
        if a > c:
            return a
        else:
            return c
    else:
        return b
    

def a_to_b(a, b):
    """
    Make a colorspace conversion matrix between two sets of primaries.
    """
    a_to_xyz = primaries_to_XYZ(a)
    #print "ToXYZ:",a_to_xyz
    b_to_xyz = primaries_to_XYZ(b)
    return a_to_xyz.I * b_to_xyz


if __name__ in "__main__":

    # To test the program, run with --test 
    test_dcip3_rgbw =  [[0.68, 0.32], [0.265, 0.69], [0.15,0.06], [0.314, 0.351]]
    test_left_rgbw =  [[0.62, 0.34], [0.31, 0.54], [0.18,0.07], [0.3201, 0.314]]
    test_right_rgbw = [[0.65, 0.32], [0.29, 0.61], [0.17,0.04], [0.3100, 0.332]]

    options,args = parse_cmdline()

    if options.infname != '':
        handle = open(options.infname, 'r')
        data = json.load(handle)
        handle.close()
        test_left_rgbw = data['left_primaries_and_wp']
        test_right_rgbw = data['right_primaries_and_wp']

    # Let's add the 'z' component
    left = promote_xyz(test_left_rgbw)
    right = promote_xyz(test_right_rgbw)
    p3 = promote_xyz(test_dcip3_rgbw)

    print "left\n",np.matrix(left)
    print "right\n",np.matrix(right)
    print "DCI-P3\n",np.matrix(p3)

    left_to_p3  = a_to_b(test_left_rgbw, p3)
    right_to_p3 = a_to_b(test_right_rgbw, p3)

    left_norm = compute_norm(left_to_p3)
    right_norm = compute_norm(right_to_p3)
    left_to_p3 = left_to_p3 / left_norm
    right_to_p3 = right_to_p3 / right_norm

    print "left_to_p3"
    print left_to_p3  
    print "right_to_p3"
    print right_to_p3

    if options.outfname != '':
        handle = open(options.outfname, 'w')
        handle.write(json.dumps({'left':(left_to_p3).tolist(), 'right':(right_to_p3).tolist()}))
    handle.close() 

