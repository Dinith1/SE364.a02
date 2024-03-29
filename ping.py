# -*- coding: utf-8 -*-
import os
import sys
import socket
import struct
import time
import collections
from checksum import internet_checksum


assert 3 <= sys.version_info[0], 'Requires Python 3'


MILLISEC_PER_SEC = 1000.0 # For readability in time conversions
RIGHT_HEXTET = 0xffff # Selects the right-most 16 bits
BUFFER_SIZE = 2 << 5 # Size in bits of buffer in which socket data is received
ICMP_PORT_PLACEHOLDER = 1 # Port number required for socket.socket, though unused by ICMP
ICMP_HEADER_LENGTH = 8
ICMP_STRUCT_FIELDS = "BBHHH"  # for use with struct.pack/unpack
IP_HEADER_LENGTH = 20

class TimeoutError(Exception):
    pass


class ChecksumError(Exception):
    pass



ICMPMessage = collections.namedtuple('ICMPMessage', ['type', 'code', 'checksum',
                                                     'identifier', 'sequence_number']) # Named tuple for ICMP Messages
ICMPTypeCode = collections.namedtuple('ICMPTypeCode', ['type', 'code']) # For ICMP type field
ECHO_REQUEST = ICMPTypeCode(8, 0)
ECHO_REPLY = ICMPTypeCode(0, 0)



def this_instant():
    return time.perf_counter()



def ping(client_socket, dest_host, client_id, seq_no=0):
    """
    Sends echo request, receives response, and returns RTT.
    """

    def icmp_header(host_checksum):
        message = ICMPMessage(
                    type=ECHO_REQUEST.type,
                    code=ECHO_REQUEST.code,
                    checksum=host_checksum,
                    identifier=client_id,
                    sequence_number=seq_no)
        return struct.pack(ICMP_STRUCT_FIELDS, *message)


    icmp_payload = struct.pack('d', this_instant())  # double-precision float
    icmp_packet_without_checksum = icmp_header(0) + icmp_payload
    checksum = internet_checksum(icmp_packet_without_checksum)
    checksum_string = hex(checksum)
    checksum_string_reversed = checksum_string[4:] + checksum_string[2:4]
    checksum_int_reversed = int(checksum_string_reversed, 16)
    
    icmp_packet = icmp_header(checksum_int_reversed) + icmp_payload


    # Get the host name (unchanged if already in IPv4 address format)
    dest_host = socket.gethostbyname(dest_host)

	# Send packet to destination host
    client_socket.sendto(icmp_packet, (dest_host, ICMP_PORT_PLACEHOLDER))
    
    # Try to get response
    datagram, addr = client_socket.recvfrom(BUFFER_SIZE)
    time_recv = this_instant()
        
	# Extract ICMP packet from datagram (drop IP Header)
    icmp_packet_recv = datagram[IP_HEADER_LENGTH:]
    
	# Compute checksum on ICMP response packet (header and payload)
    checksum_recv = internet_checksum(icmp_packet_recv)
    if checksum_recv != 0:
        raise ChecksumError()
    
	# Extract ICMP response header from ICMP packet (8 bytes) and unpack
    icmp_recv_header = icmp_packet_recv[0:ICMP_HEADER_LENGTH]
    recv_header = struct.unpack(ICMP_STRUCT_FIELDS, icmp_recv_header)
    
	# Extract ICMP response payload (remaining bytes) and unpack
    icmp_recv_payolad = icmp_packet_recv[ICMP_HEADER_LENGTH:]
    time_sent = struct.unpack('d', icmp_recv_payolad)[0]
    
	# Compute round-trip time from "time sent"
    rtt = (time_recv - time_sent) * MILLISEC_PER_SEC
    
    return (rtt, recv_header)
	

    # If things go wrong
    # ==================
    # You might like to check ("assert") that:
    # 1. Type field of ICMP response header is ICMP echo reply type
    # 2. Code field of ICMP response header is ICMP echo reply code
    # 3. Identifier field of ICMP response header is client_id
    # 4. len() of ICMP response payload is struct.calcsize('d')




def verbose_ping(host, timeout, count, log=print):
    """
    Send ping and print session details to command prompt.
    """
    try:
        host_ip = socket.gethostbyname(host)
    except OSError as error:
        log(error)
        log('Could not find host {}.'.format(host))
        log('Please check name and try again.')
        return

    
    log("Pinging {} [{}] with {} bytes of data "
        .format(host, host_ip, IP_HEADER_LENGTH + ICMP_HEADER_LENGTH + struct.calcsize('d')))
    
    round_trip_times = []

    for seq_no in range(count):
        try:
            with socket.socket(family=socket.AF_INET, type=socket.SOCK_RAW, 
                               proto=socket.getprotobyname("icmp")) as sock:
                sock.settimeout(timeout/MILLISEC_PER_SEC)
                client_id = os.getpid() & RIGHT_HEXTET
                delay, response = ping(sock, host, client_id=client_id, seq_no=seq_no)

            log("Reply from {:s} in {}ms: {}".format(host_ip, delay, response))

            round_trip_times.append(delay)
            
            
        except socket.timeout:
            log("Request timed out after {}ms".format(timeout))
    
        except ChecksumError:
            log("Message has been corrupted (checksum incorrect)")

        except OSError as error:
            log("OS error: {}. Please check name.".format(error.strerror))
            if isinstance(error, PermissionError):
                # Display the likely explanation for
                # TCP Socket Error Code "1 = Operation not permitted":
                log("NB: On some sytems, ICMP messages can"
                    " only be sent from processes running as root.")
            break


    num_sent = count
    num_recv = len(round_trip_times)
    num_lost = num_sent - num_recv
    rtts = round_trip_times
    
    
	# TODO: Compute & print packet statistics (number of packets received/lost)   
    log("Ping statistics for {}".format(host_ip))
    log("\tPackts: Sent = {}, Received = {}, Lost = {} ({}% loss)"
        .format(num_sent, num_recv, num_lost, (num_lost/num_sent)*100))


	# Compute & print statistics on round-trip times (Minimum, Maximum, Average)
    if num_recv > 0:
        log("Approximate round trip times in milli-seconds:")
        log("\tMinimum = {}, Maximimum = {}, Average = {}"
            .format(min(rtts), max(rtts), sum(rtts)/len(rtts)))
        





if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='Test a host.')
    parser.add_argument('-w', '--timeout',
                        metavar='timeout',
                        type=int,
                        default=1000,
                        help='Timeout to wait for each reply (milliseconds).')
    parser.add_argument('-c', '--count',
                        metavar='num',
                        type=int,
                        default=4,
                        help='Number of echo requests to send')
    parser.add_argument('hosts',
                        metavar='host',
                        type=str,
                        nargs='+',
                        help='URL or IPv4 address of target host(s)')
    args = parser.parse_args()

    for host in args.hosts:
        verbose_ping(host, timeout=args.timeout, count=args.count)
