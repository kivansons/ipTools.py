def parse_ip(str_ip_param):
    """Accepts an IP address as a string in dot decimal format and returns (Bitstr_IP,Int_Octets[],Bitstr_Octets[],)"""
    str_ip = str_ip_param
    int_octets = []  # IP as list of integer octets
    bitstr_octets = [
        "",
        "",
        "",
        "",
    ]  # IP as list of zero padded 8bit binary string octets
    bitstr_ip = ""  # IP as 32 bit binary string
    VALID_CHARS = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".")
    EIGHT_BIT_POWERS = (128, 64, 32, 16, 8, 4, 2, 1)

    # Test 1: Entered IP must be a string
    if type(str_ip) != str:
        raise TypeError("Error! Entered IP is not a string")

    # Remove whitespace
    str_ip = str_ip.strip()

    # Test 2: IP should only contain decimal digits and "."
    for char in str_ip:
        if char not in VALID_CHARS:
            raise ValueError("Error! Invalid character in IP")

    # Split Str_IP and store octets as int in Int_Octets if split element is not empty
    int_octets = [int(octet) for octet in str_ip.split(".") if octet != ""]

    # Test 3: IP should contain exactly 4 octets
    if len(int_octets) != 4:
        raise ValueError("Error! IP does not have 4 octets")

    # Test 4: Octets should be between 0 and 255, inclusive
    for octet in int_octets:
        if octet > 255:
            raise ValueError("Error! Octet in IP larger than 255")
        elif octet < 0:
            raise ValueError("Error! Octet in IP is negative")

    # Convert Int_Octets to Bitstr_Octets
    for i in range(len(int_octets)):
        workingOctet = int_octets[i]

        # For each 8bit power of 2, subtract and append 0 or 1 to bitstring
        for j in range(len(EIGHT_BIT_POWERS)):
            if workingOctet - EIGHT_BIT_POWERS[j] < 0:
                bitstr_octets[i] += "0"

            elif workingOctet - EIGHT_BIT_POWERS[j] >= 0:
                workingOctet -= EIGHT_BIT_POWERS[j]
                bitstr_octets[i] += "1"

        # Build 32bit Bitstr_IP from octets in Bitstr_Octets
        bitstr_ip = "".join(bitstr_octets)

    return bitstr_ip, int_octets, bitstr_octets


def parse_cidr(CIDR_Mask_param):
    """Accept a CIDR_Prefix and return a 32 bit binary mask string"""

    Subnet_Mask_Bitstring = ""
    Valid_Chars = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "/"}

    # Test 1: Entered mask must be a string
    if type(CIDR_Mask_param) != str:
        raise TypeError("Error! Entered mask is not a string")
    CIDR_Prefix = CIDR_Mask_param
    # Remove any whitespace
    CIDR_Prefix = CIDR_Prefix.strip()

    # Test 2: CIDR_Prefix should only contain decimal digits and "/"
    for char in CIDR_Prefix:
        if char not in Valid_Chars:
            raise ValueError("Error! Invalid character in CIDR_Prefix")

    # Test 3: First char should be "/"
    if CIDR_Prefix[0] != "/":
        raise ValueError("Error! CIDR_Prefix must start with a / ")

    CIDR_Prefix = int(CIDR_Prefix.strip("/"))

    # Test 4: CIDR_Prefix must be between 0 and 32
    if CIDR_Prefix > 32 or CIDR_Prefix < 0:
        raise ValueError("Error! Must be between 0 and 32")
    # Append number of "1" equal to CIDR_Prefix prefix
    for i in range(CIDR_Prefix):
        Subnet_Mask_Bitstring += "1"
    # Pad with "0" until bitstring is 32 bits long
    while len(Subnet_Mask_Bitstring) < 32:
        Subnet_Mask_Bitstring += "0"

    return Subnet_Mask_Bitstring


def parse_bitstr(Bitstr_IP):
    """Accept a 32bit bitstring and return four bitstring octets"""

    Bitstr_Octets = ["", "", "", ""]

    for i in range(32):
        Bitstr_Octets[i // 8] += Bitstr_IP[i]
    return Bitstr_Octets


def bitstr_to_int(Bitstr):
    """Accept a bitstring and return a decimal int"""

    Int_Octet = 0
    # Find the exponent of the most signifigant bit for the bitstring
    Most_Signifigant_Exponent = len(Bitstr) - 1

    for i, bit in enumerate(Bitstr):
        # Add the bits decimal value calculated from it's exponent to Int_Octets accumulator
        if bit == "1":
            Int_Octet += 2 ** (Most_Signifigant_Exponent - i)

    return Int_Octet


def and_bitstr(Bitsrt_1, Bitsrt_2):
    """Accept two bitsrtings and return the results of a bitwise AND."""

    AND_Result = ""

    if type(Bitsrt_1) != str or type(Bitsrt_2) != str:
        print("Error! bitsrtings must have type of Srt!")
        raise TypeError

    if len(Bitsrt_1) != len(Bitsrt_2):
        print("Error! bitstrings must be the same length")
        raise ValueError

    # Parse Bitsrt_1 and Bitsrt_2 bit by bit
    for i in range(len(Bitsrt_1)):

        # if both bits in Bitsrt_1,bitstr2 are 1 append a 1 to result
        if Bitsrt_1[i] == "1" and Bitsrt_2[i] == "1":
            AND_Result += "1"
        # else append 0
        else:
            AND_Result += "0"

    return AND_Result


def add_ip(IP_Param, Summand_Param):

    """Accepts IP as Int_Octet list and adds a decimal int to the IP
    while properly carrying over to the next octet if needed.
    """

    Summand = Summand_Param
    ip = [octet for octet in IP_Param]

    # Walk through IP list backwards starting with 4th octet
    for i in range(len(ip) - 1, -1, -1):
        # if octet + Summand will not overflow current octet, add Summand to octet. Break from loop
        if ip[i] + Summand < 256:
            ip[i] += Summand
            break
        # If octet will overflow and not indexing 1st octet
        elif ip[i] + Summand >= 256 and i != 0:
            Summand += ip[i]  # Add value of current octet to Summand
            ip[i] = 0  # Set octet to 0
            ip[i] = Summand % 256  # Set current octet to remainder portion
            Summand = Summand // 256  # Floor divide Summand to carry over to next octet
        # If indexing 1st octet and octet will overflow 255, raise an OverFlowError
        elif i == 0 and ip[i] + Summand >= 256:
            raise OverflowError(
                "Error! Supplied IP and Summand will result in an IP greater than 255.255.255.255"
            )
    return ip


def subtract_ip(IP_Param, Subtrahend_Param):

    """Accepts IP as Int_Octet list, and subtracts a decimal int from the the IP
    while properly borrowing from higher octets if needed.
    """
    ip = [Int_Octet for Int_Octet in IP_Param]
    Subtrahend = abs(Subtrahend_Param)

    while Subtrahend > 0:
        # If subtracting from 4th octet will result in val >= 0 no need to borrow
        if ip[3] - Subtrahend >= 0:
            ip[3] -= Subtrahend
            Subtrahend -= Subtrahend

        # Else we need to borrow until 4th octet is equal to or larger than subtrahend
        else:
            for i in range(2, -1, -1):
                if (ip[i] - 1) >= 0:
                    ip[i] -= 1
                    ip[i + 1] += 256
                    break
                # Raise a ValueError, if borrowing from 1st octet would result in a negative,
                elif i == 0 and ip[i] - 1 == -1:
                    raise ValueError("Error! Result is negative IP")
    return ip

    """
    NOTES:
    Abandond method. May want to try to use digit magnatude idea to reduce number of loops needed for
    for borrowSubtractIP() when subtracting numbers in the 10^9 range.
    
    for i in range(len(ip)):

        # Calculate current octet's digit magnatude
        # 1st = 16,581,375, 2nd = 65536, 3rd = 256, 4th = 1
        octetMagnatude = 256 ** (3 - i)
        # if Subtrahend is large enough to effect current octet
        if Subtrahend // octetMagnatude > 0:
            # calculate current magntude Subtrahend
            workingSubtrahend = Subtrahend // octetMagnatude
            # calculate remaining Subtrahend
            Subtrahend = Subtrahend % octetMagnatude
            
            #If subtraction from first octet will result in negative, raise an error
            if i == 0 and ip[i] - workingSubtrahend < 0:
                raise ValueError("Error! Resulting subtraction results in a negative IP")

            #If subtraction from current octet will not result in negative, perform operation
            elif ip[i] - workingSubtrahend >= 0:
                ip[i] -= workingSubtrahend

            # if subtraction from current octet will be negative, borrow from higher octet
            # 
            # Does not properly handle borrowing from multible neighboring octets!
            # Example 192.0.0.0 - 1024 results in 192.-1.252.0
            # Need to find better logic!
            elif ip[i] - workingSubtrahend < 0:
                # Needed logic... 
                # if borrowing from left neighbor will not result in a negative
                if ip[i-1] - 1 >= 0:
                    ip[i-1] -= 1 # Borrow from left neighbor octet
                    ip[i] += 256 # Add to current octet
                    ip[i] -= workingSubtrahend # Perform subtraction
                # else borrow from i-2 octet or i-3 octet if needed
                
    return ip
    """


def add_or_subtract_ip(IP_Param, Operand_Param):
    """Accepts IP as a string or Int_Octet List, and a positive or negative value decimal int
    validates the input and then calls the borrowSubtractIP() or carryAddIP() fuctions depending
    on the sign of the supplied int
    """

    # if a string IP is supplied try and parse to Int_Octet list using parseIP funct
    if type(IP_Param) == str:
        ip = [Int_Octet for Int_Octet in parse_ip(IP_Param)[1]]
    else:
        ip = [octet for octet in IP_Param]
    Operand = Operand_Param

    # IP should contain exactly 4 octets
    if len(ip) != 4:
        raise ValueError("Error! IP does not have 4 octets")

    # Octets should be ints
    for octet in ip:
        if type(octet) != int:
            raise TypeError("Error! octet in IP is not of type int")

    # Octets should be between 0 and 255, inclusive
    for octet in ip:
        if octet > 255:
            raise ValueError("Error! Octet in IP larger than 255")
        elif octet < 0:
            raise ValueError("Error! Octet in IP is negative")

    # Supplied Operand should be type of int
    if type(Operand) != int:
        raise TypeError("Error! Summand expected int, got", type(Operand))

    # if Operand is zero just return IP
    if Operand == 0:
        return ip

    # If Operand is positive perform addition
    if Operand > 0:
        ip = add_ip(ip, Operand)
        return ip
    # If Operand is negative convert to positive int and perform subtraction
    if Operand < 0:
        Operand = Operand * -1
        ip = subtract_ip(ip, Operand)
        return ip


def subnet_calc(ip, CIDR_Prefix):
    """Accepts IP and CIDR_Prefix slash prefex and returns subnetting information"""
    """
    Todo:
    Write IP add function *Done*
    Write IP subtract function *Done
    Write function to find subnet group size from CIDR_Prefix *Done
    Calc First_Host_IP *Done
    Calc First_Host_IPIP *Done
    Calc BroadcastIP *Done
    Calc Num_Host_IPs *Done

    Write function to convert CIDR_Prefix to Subnet Mask
    """

    # get IP working information to calculate subnet information
    Bitsrt_IP, Int_Octets, Bitsrt_Octets = parse_ip(ip)

    # Parse CIDR_Prefix Mask and store as 32 bitstring
    Subnet_Mask_Bitstring = parse_cidr(CIDR_Prefix)

    # Calculate number of IPs in subnet
    Subnet_Group_Size = 2 ** (32 - int(CIDR_Prefix.strip("/")))

    # Calculate network address by bitwise ANDing IP with Mask, store as bitstrOctet list
    Network_Address_Bitstrs = parse_bitstr(and_bitstr(Bitsrt_IP, Subnet_Mask_Bitstring))

    # Convert bitsrt list to list of ints
    Network_Address_Ints = [bitstr_to_int(octet) for octet in Network_Address_Bitstrs]

    # Add one to network address to find first host IP in Subnet
    First_Host_IP = [octet for octet in add_or_subtract_ip(Network_Address_Ints, 1)]

    # Find Broadcast Address by adding subnetGroupsize - 1 to network address
    Broadcast_IP = [
        octet for octet in add_or_subtract_ip(Network_Address_Ints, Subnet_Group_Size - 1)
    ]

    # Subtract one from Broadcast_IP to find Last_Host_IP
    Last_Host_IP = [octet for octet in add_or_subtract_ip(Broadcast_IP, -1)]

    # Subtract two from group size for usable IPs
    Num_Host_IPs = Subnet_Group_Size - 2

    return Network_Address_Ints, First_Host_IP, Last_Host_IP, Broadcast_IP, Num_Host_IPs


# User Input
def get_input():
    while True:
        Input_IP = input("Enter an IP address or (Q)uit: ")

        if Input_IP.lower() == "q":
            break

        Input_CIDR = input("Enter a subnet as CIDR slash prefix: ")

        # Get Subnet info from Subnet Calc Func
        (
            Network_Address,
            First_Host_IP,
            Last_Host_IP,
            Broadcast_IP,
            Num_Host_IPs,
        ) = subnet_calc(Input_IP, Input_CIDR)

        # Convert Int Octets to Strings
        Network_Address_Str = ".".join([str(octet) for octet in Network_Address])
        First_Host_Str = ".".join([str(octet) for octet in First_Host_IP])
        Last_Host_Str = ".".join([str(octet) for octet in Last_Host_IP])
        Broadcast_Str = ".".join([str(octet) for octet in Broadcast_IP])

        print("Your Subnet information:\n")
        print("Network address:", Network_Address_Str)
        print("First Host IP:", First_Host_Str)
        print("Last Host IP:", Last_Host_Str)
        print("Broadcast IP:", Broadcast_Str)
        print("Usable IPs:", Num_Host_IPs)


get_input()
