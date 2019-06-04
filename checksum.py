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
    
    # Handle odd number of bytes in data (one extra byte on the end)
    if i + 1 == len(data):
        toSum.append(bin(data[i]<<8))
    
    # Add 16-bit sequences
    for b in toSum:
        total += int(b, 2)
        # Wrap around carry bit
        if (total > 65535):
            total -= 65535
            
    return int(hextet_complement(total), 2)