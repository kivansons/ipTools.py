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
    int_octets = [int(octet) for octet in str_ip.split(".")]

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
        working_octet = int_octets[i]

        # For each 8bit power of 2, subtract and append 0 or 1 to bitstring
        for j in range(len(EIGHT_BIT_POWERS)):
            if working_octet - EIGHT_BIT_POWERS[j] < 0:
                bitstr_octets[i] += "0"

            elif working_octet - EIGHT_BIT_POWERS[j] >= 0:
                working_octet -= EIGHT_BIT_POWERS[j]
                bitstr_octets[i] += "1"

        # Build 32bit Bitstr_IP from octets in Bitstr_Octets
        bitstr_ip = "".join(bitstr_octets)

    return [bitstr_ip, int_octets, bitstr_octets]


def parse_cidr(cidr_mask_param):
    """Accept a CIDR_Prefix and return a 32 bit binary mask string"""

    subnet_mask_bitstring = ""
    VALID_CHARS = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "/"}

    # Test 1: Entered mask must be a string
    if type(cidr_mask_param) != str:
        raise TypeError("Error! Entered mask is not a string")
    cidr_prefix = cidr_mask_param
    # Remove any whitespace
    cidr_prefix = cidr_prefix.strip()


    if len(cidr_prefix) == 0:
        raise ValueError("Error! Empty string passed as argument")


    # Test 2: CIDR_Prefix should only contain decimal digits and "/"
    for char in cidr_prefix:
        if char not in VALID_CHARS:
            raise ValueError("Error! Invalid character in CIDR_Prefix")


    # Test 3: First char should be "/"
    if cidr_prefix[0] != "/":
        raise ValueError("Error! CIDR_Prefix must start with a / ")

    cidr_prefix = int(cidr_prefix.strip("/"))

    # Test 4: CIDR_Prefix must be between 0 and 32
    if cidr_prefix > 32 or cidr_prefix < 0:
        raise ValueError("Error! Must be between 0 and 32")
    # Append number of "1" equal to CIDR_Prefix prefix
    for i in range(cidr_prefix):
        subnet_mask_bitstring += "1"
    # Pad with "0" until bitstring is 32 bits long
    while len(subnet_mask_bitstring) < 32:
        subnet_mask_bitstring += "0"

    return subnet_mask_bitstring


def parse_bitstr(bitstr_IP):
    """Accept a 32bit bitstring and return four bitstring octets"""

    bitstr_bctets = ["", "", "", ""]

    for i in range(32):
        bitstr_bctets[i // 8] += bitstr_IP[i]
    return bitstr_bctets


def bitstr_to_int(bitstr):
    """Accept a bitstring and return a decimal int"""

    int_octet = 0
    # Find the exponent of the most signifigant bit for the bitstring
    most_signifigant_exponent = len(bitstr) - 1

    for i, bit in enumerate(bitstr):
        # Add the bits decimal value calculated from it's exponent to Int_Octets accumulator
        if bit == "1":
            int_octet += 2 ** (most_signifigant_exponent - i)

    return int_octet


def and_bitstr(bitsrt_1, bitsrt_2):
    """Accept two bitsrtings and return the results of a bitwise AND."""

    AND_Result = ""

    if type(bitsrt_1) != str or type(bitsrt_2) != str:
        print("Error! bitsrtings must have type of Srt!")
        raise TypeError

    if len(bitsrt_1) != len(bitsrt_2):
        print("Error! bitstrings must be the same length")
        raise ValueError

    # Parse Bitsrt_1 and Bitsrt_2 bit by bit
    for i in range(len(bitsrt_1)):

        # if both bits in Bitsrt_1,bitstr2 are 1 append a 1 to result
        if bitsrt_1[i] == "1" and bitsrt_2[i] == "1":
            AND_Result += "1"
        # else append 0
        else:
            AND_Result += "0"

    return AND_Result


def add_ip(ip_param, summand_param):

    """Accepts IP as Int_Octet list and adds a decimal int to the IP
    while properly carrying over to the next octet if needed.
    """

    summand = summand_param
    ip = [octet for octet in ip_param]

    # Walk through IP list backwards starting with 4th octet
    for i in range(len(ip) - 1, -1, -1):
        # if octet + Summand will not overflow current octet, add Summand to octet. Break from loop
        if ip[i] + summand < 256:
            ip[i] += summand
            break
        # If octet will overflow and not indexing 1st octet
        elif ip[i] + summand >= 256 and i != 0:
            summand += ip[i]  # Add value of current octet to Summand
            ip[i] = 0  # Set octet to 0
            ip[i] = summand % 256  # Set current octet to remainder portion
            summand = summand // 256  # Floor divide Summand to carry over to next octet
        # If indexing 1st octet and octet will overflow 255, raise an OverFlowError
        elif i == 0 and ip[i] + summand >= 256:
            raise OverflowError(
                "Error! Supplied IP and Summand will result in an IP greater than 255.255.255.255"
            )
    return ip


def subtract_ip(ip_param, subtrahend_param):

    """Accepts IP as Int_Octet list, and subtracts a decimal int from the the IP
    while properly borrowing from higher octets if needed.
    """
    ip = [Int_Octet for Int_Octet in ip_param]
    subtrahend = abs(subtrahend_param)

    while subtrahend > 0:
        # If subtracting from 4th octet will result in val >= 0 no need to borrow
        if ip[3] - subtrahend >= 0:
            ip[3] -= subtrahend
            subtrahend -= subtrahend

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


def add_or_subtract_ip(ip_param, operand_param):
    """Accepts IP as a string or Int_Octet List, and a positive or negative value decimal int
    validates the input and then calls the borrowSubtractIP() or carryAddIP() fuctions depending
    on the sign of the supplied int
    """

    # if a string IP is supplied try and parse to Int_Octet list using parseIP funct
    if type(ip_param) == str:
        ip = [int_octet for int_octet in parse_ip(ip_param)[1]]
    else:
        ip = [octet for octet in ip_param]
    operand = operand_param

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
    if type(operand) != int:
        raise TypeError("Error! Summand expected int, got", type(operand))

    # if Operand is zero just return IP
    if operand == 0:
        return ip

    # If Operand is positive perform addition
    if operand > 0:
        ip = add_ip(ip, operand)
        return ip
    # If Operand is negative convert to positive int and perform subtraction
    if operand < 0:
        operand = operand * -1
        ip = subtract_ip(ip, operand)
        return ip


def subnet_calc(ip, cidr_prefix):
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
    bitsrt_ip, int_octets, bitsrt_octets = parse_ip(ip)

    # Parse CIDR_Prefix Mask and store as 32 bitstring
    subnet_mask_bitstring = parse_cidr(cidr_prefix)

    # Calculate number of IPs in subnet
    subnet_group_size = 2 ** (32 - int(cidr_prefix.strip("/")))

    # Calculate network address by bitwise ANDing IP with Mask, store as bitstrOctet list
    network_address_bitstrs = parse_bitstr(and_bitstr(bitsrt_ip, subnet_mask_bitstring))

    # Convert bitsrt list to list of ints
    network_address_ints = [bitstr_to_int(octet) for octet in network_address_bitstrs]

    # Add one to network address to find first host IP in Subnet
    first_host_ip = [octet for octet in add_or_subtract_ip(network_address_ints, 1)]

    # Find Broadcast Address by adding subnetGroupsize - 1 to network address
    broadcast_ip = [
        octet for octet in add_or_subtract_ip(network_address_ints, subnet_group_size - 1)
    ]

    # Subtract one from Broadcast_IP to find Last_Host_IP
    last_host_ip = [octet for octet in add_or_subtract_ip(broadcast_ip, -1)]

    # Subtract two from group size for usable IPs
    num_host_ip = subnet_group_size - 2

    return network_address_ints, first_host_ip, last_host_ip, broadcast_ip, num_host_ip


# User Input
def get_input():
    while True:
        usr_input = str(input("Enter a IP subnet in CIDR notation (i.e. 192.168.0.1/24) or (Q)uit: "))
        if usr_input.lower() == "q":
            break

        try:
           input_ip,input_cidr = usr_input.split("/")
        except:
            print("Invalid Subnet, Try Again")
            get_input()

        input_cidr = "/" + input_cidr

        try:
        # Get Subnet info from Subnet Calc Func
            (
                network_address,
                first_host_ip,
                last_host_ip,
                broadcast_ip,
                num_host_ip,
            ) = subnet_calc(input_ip, input_cidr)
        except Exception as error:
            print(error)
            get_input()

        # Convert Int Octets to Strings
        network_address_str = ".".join([str(octet) for octet in network_address])
        first_host_str = ".".join([str(octet) for octet in first_host_ip])
        last_host_str = ".".join([str(octet) for octet in last_host_ip])
        broadcast_str = ".".join([str(octet) for octet in broadcast_ip])

        print("Your Subnet information:\n")
        print("Network address:", network_address_str)
        print("First Host IP:", first_host_str)
        print("Last Host IP:", last_host_str)
        print("Broadcast IP:", broadcast_str)
        print("Usable IPs:", num_host_ip)

if __name__ == "__main__":
    get_input()
