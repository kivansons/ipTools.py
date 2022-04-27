def parseIP(strIP):
    """Accepts an IP address as a string in dot decimal format and returns (bitstrIP,intOctets[],bitstrOctets[],)"""

    intOctets = []  # IP as list of integer octets
    bitstrOctets = ["", "", "", ""]  # IP as list of zero padded binary string octets
    bitstrIP = ""  # IP as 32 bit binary string
    validChars = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".")
    eightBitPowers = (128, 64, 32, 16, 8, 4, 2, 1)

    # Test 1: Entered IP must be a string
    if type(strIP) != str:
        raise TypeError("Error! Entered IP is not a string")

    # Remove whitespace
    strIP = strIP.strip()

    # Test 2: IP should only contain decimal digits and "."
    for char in strIP:
        if char not in validChars:
            raise ValueError("Error! Invalid character in IP")

    # Split strIP and store octets as int in intOctets if split element is not empty
    intOctets = [int(octet) for octet in strIP.split(".") if octet != ""]

    # Test 3: IP should contain exactly 4 octets
    if len(intOctets) != 4:
        raise ValueError("Error! IP does not have 4 octets")

    # Test 4: Octets should be between 0 and 255, inclusive
    for octet in intOctets:
        if octet > 255:
            raise ValueError("Error! Octet in IP larger than 255")
        elif octet < 0:
            raise ValueError("Error! Octet in IP is negative")

    # Convert intOctets to bitstrOctets
    for i in range(len(intOctets)):
        workingOctet = intOctets[i]

        # For each 8bit power of 2, subtract and append 0 or 1 to bitstring
        for j in range(len(eightBitPowers)):
            if workingOctet - eightBitPowers[j] < 0:
                bitstrOctets[i] += "0"

            elif workingOctet - eightBitPowers[j] >= 0:
                workingOctet -= eightBitPowers[j]
                bitstrOctets[i] += "1"

        # Build 32bit bitstrIP from octets in bitstrOctets
        bitstrIP = "".join(bitstrOctets)

    return bitstrIP, intOctets, bitstrOctets


def parseCIDR(CIDR):
    """Accept a CIDR prefix and return a 32 bit binary mask string"""

    bitstrMask = ""
    validChars = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "/"}

    # Test 1: Entered mask must be a string
    if type(CIDR) != str:
        raise TypeError("Error! Entered mask is not a string")

    # Remove any whitespace
    CIDR = CIDR.strip()

    # Test 2: CIDR should only contain decimal digits and "/"
    for char in CIDR:
        if char not in validChars:
            raise ValueError("Error! Invalid character in CIDR")

    # Test 3: First char should be "/"
    if CIDR[0] != "/":
        raise ValueError("Error! CIDR must start with a / ")

    CIDR = int(CIDR.strip("/"))

    # Test 4: CIDR must be between 0 and 32
    if CIDR > 32 or CIDR < 0:
        raise ValueError("Error! Must be between 0 and 32")

    for i in range(CIDR):
        bitstrMask += "1"
    while len(bitstrMask) < 32:
        bitstrMask += "0"

    return bitstrMask


def parseBitstr(bitstrIP):
    """Accept a 32bit bitstring and return four bitstring octets"""

    bitstrOctets = ["", "", "", ""]

    for i in range(32):
        bitstrOctets[i // 8] += bitstrIP[i]
    return bitstrOctets


def bitstrToInt(bitstr):
    """Accept a bitstring and return a decimal int"""

    intOctet = 0
    most_signifigant_exponent = len(bitstr) - 1

    i = 0
    for char in bitstr:

        # If bit is 1 add that bits decimal value to intOctets accumulator
        if char == "1":
            intOctet += 2 ** (most_signifigant_exponent - i)
            i += 1
        else:
            i += 1
    return intOctet


def andBitstrs(bitsrt1, bitsrt2):
    """Accept two bitsrtings and return the results of a bitwise AND"""

    andResult = ""

    if type(bitsrt1) != Str or type(bitsrt2) != Srt:
        print("Error! bitsrtings must have type of Srt!")
        raise TypeError

    if len(bitsrt1) != len(bitsrt2):
        print("Error! bitstrings must be the same length")
        raise ValueError

    # Parse bitsrt1 and bitsrt2 bit by bit
    for i in range(len(bitsrt1)):

        # if both bits in bitsrt1,bitstr2 are 1 append a 1 to result
        if bitsrt1[i] == "1" and bitsrt2[i] == "1":
            andResult += "1"
        # else append 0
        else:
            andResult += "0"

    return andResult


def subnetCalc(ip, CIDR):
    """Accepts IP and CIDR slash prefex and returns subnetting information"""

    networkNumber = ""  # The Subnet's Network number
    firstHostIP = ""  # First Usable host IP
    lastHostIP = ""  # Last Usable Host IP
    broadcastIP = ""  # Broadcast IP
    numHostIPs = ""  # Number of usable host IPs in network
    subnetMask = ""  # Dot Decimal subnet mask

    # get IP working information to calculate subnet information
    bitsrtIP, intOctets, bitsrtOctets = parseIP(ip)
    bitstrMask = parseCIDR(CIDR)

    # Calculate network number by bitwise ANDing IP with Mask, store as bitstrOctet list
    networkNumberBitstrs = parseBitstr(andBitstrs(bitsrtIP, bitstrMask))

    # Convert bitsrt list to list of ints
    networkNumberInts = [bitstrToInt(octet) for octet in networkNumberBitstrs]

    # Convert bitstr list to list of decimal strings
    networkNumberStrs = [str(octet) for octet in networkNumberInts]

    # Join strings to final dotdecimal IP string
    networkNumber = ".".join(networkNumberStrs)

    return networkNumber



"""
ipAddress = input("Enter an IP address: ")
prefix = input("Enter a CIDR Prefix ")

print("The network number is:", subnetCalc(ipAddress,prefix))
"""
