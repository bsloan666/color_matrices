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
This is a command-line utility for generating 3x3 matrices from a pair of arrays
containing primaries and white points (expressed as xy chromaticity coordinates)
of a source and destination gamut.

example command:
python color_matrix.py AWG AP0 
"""

import os
import sys
import numpy as np
import json
import math
from optparse import OptionParser
import primaries_db as pdb

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
    b_to_xyz = primaries_to_XYZ(b)
    return b_to_xyz.I * a_to_xyz


if __name__ in "__main__":
    srcname = sys.argv[1]
    dstname = sys.argv[2]

    src = pdb.name_to_param_array(srcname) 
    dst = pdb.name_to_param_array(dstname) 

    src = promote_xyz(src)
    dst = promote_xyz(dst)

    out = a_to_b(src, dst)
    np.set_printoptions(precision=6, suppress=True)
    print(out) 
