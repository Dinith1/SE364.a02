# -*- coding: utf-8 -*-

def hextet_complement(x):
    '''
    Compute the one's complement of a Python int regarded as a fixed-width hextet (16 bits)
    '''
    mask = 0xffff
    return bin(~x & mask)



def internet_checksum(data, total=0x0):
    '''
    Internet Checksum of a bytes array. Returns an integer version of the checksum.
    '''    
    toSum = []
    # Convert data to 16-bit sequences
    for i in range(0, len(data), 2):
        toSum.append(bin((data[i]<<8) + data[i+1]))
        i += 2

    # Add 16-bit sequences
    sum = 0
    for b in toSum:
        sum += int(b, 2)
        if (len(bin(sum)) > 18):
            sum += 1 # Carry out bit must be 1 if it exists
            
#    return int(hextet_complement(sum), 2)
    return hextet_complement(sum)
