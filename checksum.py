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
    for i in range(len(data)):
        toSum[i] = bin((data[i]<<8) + data[i+1])
        i += 2

    # Add 16-bit sequences
    sum = 0
    for j in range(len(toSum)):
        sum += int(toSum[i], 2)
        if (len(bin(sum)) > 18):
            sum += 1 # Carry out bit must be 1 if it exists
            
    return int(hextet_complement(sum), 2)
