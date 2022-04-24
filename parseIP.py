def parseIP(strIP):
    # This function takes an IP address as a string in dot decimal format and returns (intOctets[],bitstrOctets[],bitstrIP)

    intOctets = [] # IP as list of integer octals
    bitstrOctets = ["","","",""] # IP as list of zero padded binary string octals
    bitstrIP = "" # IP as 32 bit binary string
    validChars = ("0","1","2","3","4","5","6","7","8","9","10",".")
    eightBitPowers = (128,64,32,16,8,4,2,1)

    # Test 1: Enteried IP must be a string
    if type(strIP) != str:
        print("Error! Entered IP is not a string")
        return None

    # Remove any whitespace
    strIP = strIP.strip()

    # Test 2: IP should only contain decimal digits and "."
    for char in strIP:
        if char not in validChars:
            print("Error! Invalid character in IP")
            return None

    # Split strIP and store octets as int in intOctets if split element is not empty
    intOctets = [int(octet) for octet in strIP.split(".") if octet != ""]
    
    # Test 3: IP should contain exactly 4 octets
    if len(intOctets) != 4:
        print("Error! IP does not have 4 octets")
        return None
    
    # Test 4: Octets should be between 0 and 255, inclusive
    for octet in intOctets:
        if octet > 255:
            print("Error! Octet in IP larger than 255")
            return None
        elif octet < 0:
            print("Error! Octet in IP is negative")
            return None
     

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
    
    # Build 32bit bitstrIP from bitstrOctets
    for octet in bitstrOctets:
        bitstrIP += octet
    
    returnData = (intOctets, bitstrOctets, bitstrIP)
    return returnData

parsedIP = parseIP(input("Enter an IP Address: "))
print(parsedIP)