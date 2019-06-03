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
ICMP_HEADER_LENGTH = 28
ICMP_STRUCT_FIELDS = "BBHHH"  # for use with struct.pack/unpack


class TimeoutError(Exception):
    pass


class ChecksumError(Exception):
    pass


# Named tuple for ICMP Messages
ICMPMessage = collections.namedtuple('ICMPMessage', ['type', 'code', 'checksum', 'identifier', 'sequence_number'])
# For ICMP type field
ICMPTypeCode = collections.namedtuple('ICMPTypeCode', ['type', 'code'])

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
                    type=None,  # TODO: Use appropriate argument here
                    code=None,  # TODO: Use appropriate argument here
                    checksum=host_checksum,
                    identifier=client_id,
                    sequence_number=seq_no)
        return struct.pack(ICMP_STRUCT_FIELDS, *message)


	# TODO: Please study these lines carefully,
	#       noting that "icmp_pack()" (defined above) is called *twice*
    icmp_payload = struct.pack('d', this_instant())  # double-precision float
    icmp_packet_without_checksum = icmp_header(0) + icmp_payload
    checksum = internet_checksum(icmp_packet_without_checksum)
    icmp_packet = icmp_header(checksum) + icmp_payload

    #
    # TODO: Please note that that "icmp_packet" is the
    #       payload that we'll send through for our INET raw socket
    #

    # Note: socket.gethostbyname() returns the host name
    # unchanged if it is already in IPv4 address format.
    dest_host = socket.gethostbyname(dest_host)

    #
	# TODO:
	# 1. Call sendto() on socket to send packet to destination host
    # 2. Call recvfrom() on socket to receive datagram
	#    (Note: A time-out exception might be raised here).
    # 2. Store this_instant() at which datagram was received
	# 3. Extract ICMP packet from datagram i.e. drop IP header (20 bytes)
	#     e.g. "icmp_packet = datagram[20:]"
	# 4. Compute checksum on ICMP response packet (header and payload);
	#     this will hopefully come to zero
	# 5. Raise exception if checksum is nonzero
	# 6. Extract ICMP response header from ICMP packet (8 bytes) and
	#     unpack binary response data to obtain ICMPMessage "response"
	#     that we'll return with the round-trip time (Step 9, below);
	#     notice that this namedstruct is printed in the sample
	#     command line output given in the assignment description.
	#     e.g. "Reply from 151.101.0.223 in 5ms: ICMPMessage(type=0, code=0, checksum=48791, identifier=33540, sequence_number=0)"
	# 7. Extract ICMP response payload (remaining bytes) and unpack
	#     binary data to recover "time sent"
	# 8. Compute round-trip time from "time sent"
	# 9. Return "(round-trip time in milliseconds, response)"
	#
    # If things go wrong
    # ==================
    # You might like to check ("assert") that:
    # 1. Type field of ICMP response header is ICMP echo reply type
    # 2. Code field of ICMP response header is ICMP echo reply code
    # 3. Identifier field of ICMP response header is client_id
    # 4. len() of ICMP response payload is struct.calcsize('d')
    #




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

    
    log("Pinging {} [{}] with {} bytes of data ".format(host, host_ip, 32))
    

    round_trip_times = []

    for seq_no in range(count):
        try:
            with socket.socket(family=socket.AF_INET, 
                               type=socket.SOCK_RAW, 
                               proto=socket.getprotobyname("icmp")) as sock:
                sock.settimeout(timeout/MILLISEC_PER_SEC)
                client_id = os.getpid() & RIGHT_HEXTET
                delay, response = ping(sock, host, client_id=client_id, seq_no=seq_no)

            log("Reply from {:s} in {}ms: {}".format(host_ip, delay, response))

            round_trip_times.append(delay)
            
            
        except TimeoutError as error:
    		# TODO: catch time-out error:
            #     handle time-out error i.e. log(...)
    
        except ChecksumError as error:
            # TODO: catch check-sum error
            #     handle checksum-error i.e. log(...)

        except OSError as error:
            log("OS error: {}. Please check name.".format(error.strerror))
            if isinstance(error, PermissionError):
                # Display the likely explanation for
                # TCP Socket Error Code "1 = Operation not permitted":
                log("NB: On some sytems, ICMP messages can"
                    " only be sent from processes running as root.")
            break

	#
	# TODO: Print packet statistics header
	# TODO: Compute & print packet statistics
	#       i.e. "how many packets received and lost?"
	#

	#
    # TODO: "if received more than 0 packets":
	#    TODO: Compute & print statistics on round-trip times
	#          i.e. Minimum, Maximum, Average
	#






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
