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
        list(
            "192.168.0.1",
        ),
        list([192, 168, 0, 1]),
        list(["foo", "bar", "eggs", "spam"]),
        tuple(
            "192,168.0.1",
        ),
        tuple((192, 168, 0, 1)),
        tuple(("foo", "bar", "eggs", "spam")),
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
    """Make sure parse_ip() raises ValueError when arguments containing not 4 octets are passed"""
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
    """ "Make sure parse_ip() raises ValueError if passed
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


def test_parse_ip_returns_correct_output():
    """Make sure parse_ip() returns the correct results for a known dot decimal IP input and known results"""
    test_inputs = [
        {
            "input": "192.168.0.1",
            "output": {
                "bitsrt_ip": "11000000101010000000000000000001",
                "int_octets": [192, 168, 0, 1],
                "bitsrt_octets": ["11000000", "10101000", "00000000", "00000001"],
            },
        },
        {
            "input": "0.221.9.166",
            "output": {
                "bitsrt_ip": "00000000110111010000100110100110",
                "int_octets": [0, 221, 9, 166],
                "bitsrt_octets": ["00000000", "11011101", "00001001", "10100110"],
            },
        },
        {
            "input": "121.255.26.157",
            "output": {
                "bitsrt_ip": "01111001111111110001101010011101",
                "int_octets": [121,255,26,157],
                "bitsrt_octets": ["01111001", "11111111", "00011010", "10011101"],
            },
        },
        {
            "input": "255.255.255.255",
            "output": {
                "bitsrt_ip": "11111111111111111111111111111111",
                "int_octets": [255,255,255,255],
                "bitsrt_octets": ["11111111", "11111111", "11111111", "11111111"],
            },
        },
        {
            "input": "0.0.0.0",
            "output": {
                "bitsrt_ip": "00000000000000000000000000000000",
                "int_octets": [0,0,0,0],
                "bitsrt_octets": ["00000000", "00000000", "00000000", "00000000"],
            },
        },
    ]
    for test in test_inputs:
        input = test["input"]
        output = test["output"]
        output_list = [
            output["bitsrt_ip"],
            output["int_octets"],
            output["bitsrt_octets"],
        ]
        assert parse_ip(input) == output_list
    return
