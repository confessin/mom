#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest2
import math

from mom.security.random import generate_random_bytes
from mom.builtins import \
    is_unicode, \
    is_bytes, \
    is_bytes_or_unicode, \
    to_utf8_if_unicode, \
    to_unicode_if_bytes, \
    unicode_to_utf8, \
    bytes_to_unicode, \
    bin, \
    hex, \
    long_byte_count, long_bit_length, is_sequence, bytes_to_unicode_recursive, unicode_to_utf8_recursive


random_bytes = generate_random_bytes(100)
utf8_bytes = '\xc2\xae'
unicode_string = u'\u00ae'
utf8_bytes2 = '\xe6\xb7\xb1\xe5\x85\xa5 Python'
unicode_string2 = u'深入 Python'


class Test_bin(unittest2.TestCase):
    def test_binary_0_1_and_minus_1(self):
        self.assertEqual(bin(0), '0b0')
        self.assertEqual(bin(1), '0b1')
        self.assertEqual(bin(-1), '-0b1')

    def test_binary_value(self):
        self.assertEqual(bin(12), '0b1100')
        self.assertEqual(bin(2**32), '0b100000000000000000000000000000000')

    def test_binary_negative_value(self):
        self.assertEqual(bin(-1200), '-0b10010110000')

    def test_binary_default_prefix(self):
        self.assertEqual(bin(0), '0b0')
        self.assertEqual(bin(1), '0b1')
        self.assertEqual(bin(12), '0b1100')
        self.assertEqual(bin(2**32), '0b100000000000000000000000000000000')
        self.assertEqual(bin(-1200), '-0b10010110000')

    def test_binary_custom_prefix(self):
        self.assertEqual(bin(0, 'B'), 'B0')
        self.assertEqual(bin(1, 'B'), 'B1')
        self.assertEqual(bin(12, 'B'), 'B1100')
        self.assertEqual(bin(2**32, 'B'), 'B100000000000000000000000000000000')
        self.assertEqual(bin(-1200, 'B'), '-B10010110000')

    def test_binary_no_prefix(self):
        self.assertEqual(bin(0, None), '0')
        self.assertEqual(bin(1, ''), '1')
        self.assertEqual(bin(12, None), '1100')
        self.assertEqual(bin(2**32, None), '100000000000000000000000000000000')
        self.assertEqual(bin(-1200, None), '-10010110000')

    def test_raises_TypeError_when_invalid_argument(self):
        self.assertRaises(TypeError, bin, None, None)
        self.assertRaises(TypeError, bin, "error")
        self.assertRaises(TypeError, bin, 2.0)
        self.assertRaises(TypeError, bin, object)

class Test_hex(unittest2.TestCase):
    def test_hex_0_1_and_minus_1(self):
        self.assertEqual(hex(0), '0x0')
        self.assertEqual(hex(1), '0x1')
        self.assertEqual(hex(-1), '-0x1')

    def test_hex_value(self):
        self.assertEqual(hex(12), '0xc')
        self.assertEqual(hex(2**32), '0x100000000')

    def test_hex_negative_value(self):
        self.assertEqual(hex(-1200), '-0x4b0')

    def test_hex_default_prefix(self):
        self.assertEqual(hex(0), '0x0')
        self.assertEqual(hex(1), '0x1')
        self.assertEqual(hex(12), '0xc')
        self.assertEqual(hex(2**32), '0x100000000')

    def test_hex_custom_prefix(self):
        self.assertEqual(hex(0, 'X'), 'X0')
        self.assertEqual(hex(1, 'X'), 'X1')
        self.assertEqual(hex(12, 'X'), 'Xc')
        self.assertEqual(hex(2**32, 'X'), 'X100000000')

    def test_hex_lower_case(self):
        self.assertEqual(hex(12), '0xc')

    def test_hex_no_prefix(self):
        self.assertEqual(hex(0, None), '0')
        self.assertEqual(hex(1, ''), '1')
        self.assertEqual(hex(12, None), 'c')
        self.assertEqual(hex(2**32, None), '100000000')

    def test_raises_TypeError_when_invalid_argument(self):
        self.assertRaises(TypeError, hex, None, None)
        self.assertRaises(TypeError, hex, "error")
        self.assertRaises(TypeError, hex, 2.0)
        self.assertRaises(TypeError, hex, object)


class Test_long_byte_count(unittest2.TestCase):
    def test_byte_count_zero_if_zero(self):
        self.assertEqual(long_byte_count(0), 0)

    def test_byte_count_correct(self):
        numbers = [-12, 12, 1200, 120091, 123456789]
        for num in numbers:
            if num < 0:
                bit_length = len(bin(num, None)) - 1
            else:
                bit_length = len(bin(num, None))
            count = int(math.ceil(bit_length / 8.0))
            self.assertEqual(long_byte_count(num), count)

    def test_raises_TypeError_when_invalid_argument(self):
        self.assertRaises(TypeError, long_byte_count, None)
        self.assertRaises(TypeError, long_byte_count, object)


class Test_long_bit_length(unittest2.TestCase):
    def test_bit_length_zero_if_zero(self):
        self.assertEqual(long_bit_length(0), 0)

    def test_bit_length_correct(self):
        numbers = [
            -12,
            12,
            1200,
            120091,
            123456789,
        ]
        for num in numbers:
            if num < 0:
                length = len(bin(num, None)) - 1
            else:
                length = len(bin(num, None))
            self.assertEqual(long_bit_length(num), length)

    def test_raises_TypeError_when_invalid_argument(self):
        self.assertRaises(TypeError, long_bit_length, None)
        self.assertRaises(TypeError, long_bit_length, object)



class Test_is_bytes(unittest2.TestCase):
    def test_accepts_bytes(self):
        self.assertTrue(is_bytes(random_bytes))
        self.assertTrue(is_bytes(utf8_bytes))
        self.assertTrue(is_bytes(utf8_bytes2))

    def test_rejects_non_bytes(self):
        self.assertFalse(is_bytes(unicode_string))
        self.assertFalse(is_bytes(unicode_string2))
        self.assertFalse(is_bytes(False))
        self.assertFalse(is_bytes(5))
        self.assertFalse(is_bytes(None))
        self.assertFalse(is_bytes([]))
        self.assertFalse(is_bytes(()))
        self.assertFalse(is_bytes([]))
        self.assertFalse(is_bytes(object))


class Test_is_unicode(unittest2.TestCase):

    def test_accepts_unicode(self):
        self.assertTrue(is_unicode(unicode_string))
        self.assertTrue(is_unicode(unicode_string2))

    def test_rejects_non_unicode(self):
        self.assertFalse(is_unicode(random_bytes))
        self.assertFalse(is_unicode(utf8_bytes))
        self.assertFalse(is_unicode(utf8_bytes2))
        self.assertFalse(is_unicode(False))
        self.assertFalse(is_unicode(5))
        self.assertFalse(is_unicode(None))
        self.assertFalse(is_unicode([]))
        self.assertFalse(is_unicode(()))
        self.assertFalse(is_unicode({}))
        self.assertFalse(is_unicode(object))


class Test_is_bytes_or_unicode(unittest2.TestCase):
    def test_accepts_any_string(self):
        self.assertTrue(is_bytes_or_unicode(random_bytes))
        self.assertTrue(is_bytes_or_unicode(utf8_bytes))
        self.assertTrue(is_bytes_or_unicode(utf8_bytes2))
        self.assertTrue(is_bytes_or_unicode(unicode_string))
        self.assertTrue(is_bytes_or_unicode(unicode_string2))

    def test_rejects_non_string(self):
        self.assertFalse(is_bytes_or_unicode(False))
        self.assertFalse(is_bytes_or_unicode(5))
        self.assertFalse(is_bytes_or_unicode(None))
        self.assertFalse(is_bytes_or_unicode([]))
        self.assertFalse(is_bytes_or_unicode(()))
        self.assertFalse(is_bytes_or_unicode({}))
        self.assertFalse(is_bytes_or_unicode(object))


class Test_to_utf8_if_unicode(unittest2.TestCase):
    def test_encodes_unicode_strings(self):
        self.assertEqual(to_utf8_if_unicode(unicode_string), utf8_bytes)
        self.assertTrue(is_bytes(to_utf8_if_unicode(unicode_string)))

        self.assertEqual(to_utf8_if_unicode(unicode_string2), utf8_bytes2)
        self.assertTrue(is_bytes(to_utf8_if_unicode(unicode_string2)))


    def test_does_not_encode_else_to_utf8(self):
        self.assertEqual(to_utf8_if_unicode(utf8_bytes), utf8_bytes)
        self.assertTrue(is_bytes(to_utf8_if_unicode(utf8_bytes)))

        self.assertEqual(to_utf8_if_unicode(utf8_bytes2), utf8_bytes2)
        self.assertTrue(is_bytes(to_utf8_if_unicode(utf8_bytes2)))

        self.assertEqual(to_utf8_if_unicode(None), None)
        self.assertEqual(to_utf8_if_unicode(False), False)
        self.assertEqual(to_utf8_if_unicode(5), 5)
        self.assertEqual(to_utf8_if_unicode([]), [])
        self.assertEqual(to_utf8_if_unicode(()), ())
        self.assertEqual(to_utf8_if_unicode({}), {})
        self.assertEqual(to_utf8_if_unicode(object), object)


class Test_to_unicode_if_bytes(unittest2.TestCase):
    def test_encodes_bytes_to_unicode(self):
        self.assertEqual(to_unicode_if_bytes(utf8_bytes), unicode_string)
        self.assertTrue(is_unicode(to_unicode_if_bytes(utf8_bytes)))

        self.assertEqual(to_unicode_if_bytes(utf8_bytes2), unicode_string2)
        self.assertTrue(is_unicode(to_unicode_if_bytes(utf8_bytes2)))

    def test_does_not_encode_else_to_unicode(self):
        self.assertEqual(to_unicode_if_bytes(unicode_string), unicode_string)
        self.assertTrue(is_unicode(to_unicode_if_bytes(unicode_string)))

        self.assertEqual(to_unicode_if_bytes(unicode_string2), unicode_string2)
        self.assertTrue(is_unicode(to_unicode_if_bytes(unicode_string2)))

        self.assertEqual(to_unicode_if_bytes(None), None)
        self.assertEqual(to_unicode_if_bytes(False), False)
        self.assertEqual(to_unicode_if_bytes(5), 5)
        self.assertEqual(to_unicode_if_bytes([]), [])
        self.assertEqual(to_unicode_if_bytes(()), ())
        self.assertEqual(to_unicode_if_bytes({}), {})
        self.assertEqual(to_unicode_if_bytes(object), object)


class Test_bytes_to_unicode(unittest2.TestCase):
    def test_converts_bytes_to_unicode(self):
        self.assertEqual(bytes_to_unicode(utf8_bytes), unicode_string)
        self.assertTrue(is_unicode(bytes_to_unicode(utf8_bytes)))

        self.assertEqual(bytes_to_unicode(utf8_bytes2), unicode_string2)
        self.assertTrue(is_unicode(bytes_to_unicode(utf8_bytes2)))

    def test_does_not_encode_unicode_and_None_to_unicode(self):
        self.assertEqual(bytes_to_unicode(unicode_string), unicode_string)
        self.assertTrue(is_unicode(bytes_to_unicode(unicode_string)))

        self.assertEqual(bytes_to_unicode(unicode_string2), unicode_string2)
        self.assertTrue(is_unicode(bytes_to_unicode(unicode_string2)))

        self.assertEqual(bytes_to_unicode(None), None)

    def test_raises_error_when_not_string_or_None(self):
        self.assertRaises(AssertionError, bytes_to_unicode, 5)
        self.assertRaises(AssertionError, bytes_to_unicode, False)
        self.assertRaises(AssertionError, bytes_to_unicode, True)
        self.assertRaises(AssertionError, bytes_to_unicode, [])
        self.assertRaises(AssertionError, bytes_to_unicode, ())
        self.assertRaises(AssertionError, bytes_to_unicode, {})
        self.assertRaises(AssertionError, bytes_to_unicode, object)

class Test_unicode_to_utf8(unittest2.TestCase):
    def test_encodes_only_unicode_to_utf8(self):
        self.assertEqual(unicode_to_utf8(unicode_string), utf8_bytes)
        self.assertTrue(is_bytes(unicode_to_utf8(unicode_string)))

        self.assertEqual(unicode_to_utf8(unicode_string2), utf8_bytes2)
        self.assertTrue(is_bytes(unicode_to_utf8(unicode_string2)))

    def test_does_not_encode_bytes_or_None_to_utf8(self):
        self.assertEqual(unicode_to_utf8(None), None)
        self.assertEqual(unicode_to_utf8(utf8_bytes), utf8_bytes)
        self.assertTrue(is_bytes(unicode_to_utf8(utf8_bytes)))

        self.assertEqual(unicode_to_utf8(utf8_bytes2), utf8_bytes2)
        self.assertTrue(is_bytes(unicode_to_utf8(utf8_bytes2)))

    def test_raises_error_when_not_string_or_None(self):
        self.assertRaises(AssertionError, unicode_to_utf8, 5)
        self.assertRaises(AssertionError, unicode_to_utf8, False)
        self.assertRaises(AssertionError, unicode_to_utf8, True)
        self.assertRaises(AssertionError, unicode_to_utf8, [])
        self.assertRaises(AssertionError, unicode_to_utf8, ())
        self.assertRaises(AssertionError, unicode_to_utf8, {})
        self.assertRaises(AssertionError, unicode_to_utf8, object)


class Test_is_sequence(unittest2.TestCase):
    def test_detects_sequences(self):
        self.assertTrue(is_sequence([1,]))
        self.assertTrue(is_sequence((1,)))
        self.assertTrue(is_sequence(""))
        self.assertTrue(is_sequence({}))
        self.assertTrue(is_sequence(dict()))
        self.assertTrue(is_sequence(set([1, 2])))
        self.assertTrue(is_sequence(frozenset([1, 2])))

    def test_rejects_non_sequences(self):
        self.assertFalse(is_sequence(False))
        self.assertFalse(is_sequence(True))
        self.assertFalse(is_sequence(None))
        self.assertFalse(is_sequence(5))
        self.assertFalse(is_sequence(Test_is_sequence))


class Test_bytes_to_unicode_recursive(unittest2.TestCase):
    def test_converts_all_bytes_to_unicode_recursively(self):
        p = dict(
            l=[utf8_bytes2, utf8_bytes],
            t=(utf8_bytes2, utf8_bytes),
            d=dict(another=[utf8_bytes, utf8_bytes2]),
            b=utf8_bytes,
            n=None
        )
        e = dict(
            l=[unicode_string2, unicode_string],
            t=(unicode_string2, unicode_string),
            d=dict(another=[unicode_string, unicode_string2]),
            b=unicode_string,
            n=None
        )
        self.assertDictEqual(bytes_to_unicode_recursive(p), e)

class Test_unicode_to_utf8_recursive(unittest2.TestCase):
    def test_converts_all_unicode_to_utf8_bytes_recursively(self):
        p = dict(
            l=[utf8_bytes2, utf8_bytes],
            t=(utf8_bytes2, utf8_bytes),
            d=dict(another=[utf8_bytes, utf8_bytes2]),
            b=utf8_bytes,
            n=None
        )
        e = dict(
            l=[unicode_string2, unicode_string],
            t=(unicode_string2, unicode_string),
            d=dict(another=[unicode_string, unicode_string2]),
            b=unicode_string,
            n=None
        )
        self.assertDictEqual(unicode_to_utf8_recursive(e), p)


if __name__ == "__main__":
    unittest2.main()

