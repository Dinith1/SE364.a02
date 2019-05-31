# SE364.a02

- 1.1 dijkstra_generalized() to return predecessors + distances
- 1.1 Visualize least-cost path for network shown

---

- 1.2 forwarding() to produce forwarding table for a predecessor map
- 1.2 Verify output


- 2.1 hextet_complement(x) to compute one's complement int (fixed-width hextet - 16 bits)
- 2.1 USE INVERT OPERATOR (~) AND SUITABLE MASK (see lab)
- 2.1 DON'T WORRY ABOUT CASE WHERE ARGUMENT ITSELF OCCUPIES MORE THAN ONE HEXTET


- 2.2 Implement Internet Checksum
- 2.2 Use hextet_complement()
- 2.2 Function should work for any Python sequence whose elements are bytes
- 2.2 Reproduce calculation in Section 3 of IETF 1071
- 2.2 COMPARE TO C CODE (SEE NOTE ON BOTTOM OF PAGE 4 OF ASSIGNMENT BRIEF)


- 2.3 Implement a function to perform CRC checks with a given generator on an arbitrary sequence of bytes
- 2.3 Verify calculation with slide 6-15
- 2.3 Don't need to store quotient
- 2.3 Use crc.py, which contains test cases
- 2.3 Sample code from lab does long division ("please ensure you are happy with this")


- 3 Re-implement ping in Python
- 3 SEE CODE ON PAGE 5 OF ASSIGNMENT BRIEF
- 3 Use struct and collections.namedtuple libraries to to de/serialize ICMP messages to/from byte sequences
- 3 Use 'with' to guarantee sockets are closed gracefully
- 3 Use suitable function from time module to estimate round-trip time
- 3 Each ICMP echo request should carry the time instant at which it was created/sent
- 3 Use exceptions to signal checksum errors and timeouts (handle all exceptions in verbose_ping())
- 3 Use built-in functions to calculate the minimum, maximum, and mean of the calculated round-trip times
- 3 Study the template and replace each "TODO" with suitable code
- 3 The type specifiers passed to struct.pack and struct.unpack must be consistent with the ICMP protocol's packet format (SEE page 6)
- 3 SEE PAGE 6 OF ASSIGNMENT BRIEF
