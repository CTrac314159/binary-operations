# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 12:45:06 2019

@author: Chris Tracy
"""

"""
This function involves a hypothetical space-based instrument that uses four different
CCDs to take measurements. An "event" is taken to be a single measurement at a pixel.
Unsigned four-byte integers can be used to represent these measurements. The relevant
data stream information and their respective integer bit positions are listed below:
    Bits 18-31: event amplitude (value range of 0-16383)
    Bits 11-17: event x-coordinate (value range of 0-127)
    Bits 4-10: event y-coordinate (value range of 0-127)
    Bits 2-3: event CCD number (value range of 0-3)
    Bit 1: fatal flag (value range of 0-1)
    Bit 0: warning flag (value range of 0-1)
    
Parameters
--------------------
number: The input number to extract the above information from. It can be either an
        integer or a float of any sign (the conversion to an unsigned 32-bit integer works for
        either type). Maximum input allowed = 4294967295, minimum input allowed = -2147483648.
        
Returns
--------------------
value_dict: A dictionary of the extracted data stream values.

Example Usage: >>> data_stream(123456)
"""

def data_stream(number):
    
    import numpy as np
    
    #Convert the input integer type into unsigned/32-bit (4 bytes) for the compiler to interpret.
    #Get the four integer byte values and reverse their order.
    print('Converting to a 32-bit unsigned integer...')
    x = np.uint32(number)
    print('Converted!')
    ints = list(x.tobytes())
    ints.reverse()
    
    #Define the event amplitude bits by shifting the leftmost 14 bits all the way to the right.
    amp = x >> np.uint8(18)
    
    #Define the x-coordinate bits by masking the appropriate integer bits and shifting to the right.
    x_coord = (x & (2**11 + 2**12 + 2**13 + 2**14 + 2**15 + 2**16 + 2**17)) >> np.uint8(11)
    
    #Define the y-coordinate bits by masking the appropriate integer bits and shifting to the right.
    y_coord = (x & (2**4 + 2**5 + 2**6 + 2**7 + 2**8 + 2**9 + 2**10)) >> np.uint8(4)
    
    #Define the CCD number bits by masking the appropriate integer bits and shifting to the right.
    ccd = (x & (2**3 + 2**2)) >> np.uint8(2)
    
    #Define the fatal flag as a single bit and shift to the right.
    f = (x & 2**1) >> np.uint8(1)
    
    #Define the warning flag as the rightmost bit.
    w = x & 2**0
    
    #Make a dictionary to store the output.
    value_dict = {'Event Amplitude': amp, 'Event x-coordinate': x_coord, 'Event y-coordinate': y_coord, 
                  'CCD Number': ccd, 'Fatal Flag': f, 'Warning Flag': w, 'Bytes': ints}
    
    return value_dict