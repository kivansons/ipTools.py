import pytest
from subnet_calc import parse_ip

def test_parse_ip_raises_TypeError_for_invalid_types():
    """Make sure parse_ip() raises TypeError when an invalid argument type is passed"""
    type_arguements = [
        int(1),
        int(-1),
        int(0),
        float(1.1),
        float(-1.1),
        float(0.0),
        list("192.168.0.1",),
        list([192,168,0,1]),
        list(["foo","bar","eggs","spam"]),
        tuple("192,168.0.1",),
        tuple((192,168,0,1)),
        tuple(("foo","bar","eggs","spam")),
    ]
    for argument in type_arguements:
        with pytest.raises(TypeError):
            parse_ip(argument)
    return 

def test_parse_ip_raises_ValueError_for_invalid_chars():
    """Make sure parse_ip() raises ValueError when unsupported chars in str are passed as arguments"""
    invalid_char_arguments = [
        "fe80:0000:000:000:000:0000",
        "192.168.a.1",
        "Foobar",
        "This is a string.",
        " . .",
        "192.168.0.1/24",
    
    ]
    for argument in invalid_char_arguments:
        with pytest.raises(ValueError):
            parse_ip(argument)
    return

def test_parse_ip_raises_ValueError_for_not_containing_four_octets():
    """Make sure parse_ip() raises ValueError when arguments containing not 4 octets are passes"""
    invalid_num_of_octets_arguments = [
        "192.168.0",
        "10.0.0.0.1",
        "102..1.3.4",
    ]
    for argument in invalid_num_of_octets_arguments:
        with pytest.raises(ValueError):
            parse_ip(argument)
    return

def test_parse_ip_raises_ValueError_for_octets_out_of_range():
    """"Make sure parse_ip() raises ValueError if passed
    an IP with an octet below 0 or above 255"""
    invalid_ip_octet_arguments = [
        "-1.0.0.0",
        "0.-1.0.0",
        "0.0.-1.0",
        "0.0.0.-1",
        "-1.-1.-1,-1",
        "256.0.0.0",
        "0.256.0.0",
        "0.0.256.0",
        "0.0.0.256",
        "1000.2000.3000.4000",
    ]
    for argument in invalid_ip_octet_arguments:
        with pytest.raises(ValueError):
            parse_ip(argument)
    return
"""Todo: 
    [] Add tests for parse_ip() to validate correct output
"""