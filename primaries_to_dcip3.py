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


import os
import sys
import numpy as np
import json
import math
from optparse import OptionParser

def promote_xyz(a):
    for p in a:
        p.append(1.0-p[0]-p[1])
    return a

def xyz_to_XYZ(v):
    V = [(1.0/v[1])*v[0], (1.0/v[1])*v[1],(1.0/v[1])*v[2]]
    return V

def primaries_to_XYZ(b):
    c = b[0:3]
    bb = np.matrix(c)
    d  =  bb.T.I
    w =  np.matrix(xyz_to_XYZ(b[3])).transpose()
    v =  d*w
    diag_w = np.diagflat(v)
    return bb.T * diag_w 

def a_to_b(a, b):
    a_to_xyz = primaries_to_XYZ(a)
    b_to_xyz = primaries_to_XYZ(b)
    return b_to_xyz.I * a_to_xyz


if __name__ in "__main__":

    test_dcip3_rgbw =  [[0.68, 0.32], [0.265, 0.69], [0.15,0.06], [0.314, 0.351]]
    test_left_rgbw =  [[0.62, 0.34], [0.31, 0.54], [0.18,0.07], [0.3201, 0.314]]
    test_right_rgbw = [[0.65, 0.32], [0.29, 0.61], [0.17,0.04], [0.3100, 0.332]]

    # The following values are used to scale the resulting matrices
    # Not sure if they're derived, measured or given, But without them
    # results don't match the spreadsheet.
    left_scale =  0.88871
    right_scale = 0.97961


    left = promote_xyz(test_left_rgbw)
    right = promote_xyz(test_right_rgbw)
    p3 = promote_xyz(test_dcip3_rgbw)

    print "left\n",np.matrix(left)
    print "right\n",np.matrix(right)
    print "DCI-P3\n",np.matrix(p3)

    left_to_p3  = a_to_b(test_left_rgbw, p3)
    right_to_p3 = a_to_b(test_right_rgbw, p3)

    print "left_to_p3"
    print left_to_p3.I * left_scale 
    print "right_to_p3"
    print right_to_p3.I * right_scale
