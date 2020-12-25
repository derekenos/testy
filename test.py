
from decimal import Decimal

from __init__ import (
    DidNotRaise,
    assertEqual,
    assertFalse,
    assertIsBytes,
    assertIsDecimal,
    assertIsFloat,
    assertIsInstance,
    assertIsInt,
    assertIsString,
    assertNone,
    assertRaises,
    assertTrue,
)

if __name__ == '__main__':
    # Test assertEqual
    assertEqual(0, 0)
    try:
        assertEqual(0, 1)
    except AssertionError:
        pass

    # Test assertFalse
    assertFalse(False)
    try:
        assertFalse(True)
    except AssertionError:
        pass

    # Test assertIsBytes
    assertIsBytes(b'')
    try:
        assertIsBytes('')
    except AssertionError:
        pass

    # Test assertIsDecimal
    assertIsDecimal(Decimal('0'))
    try:
        assertIsDecimal(0)
    except AssertionError:
        pass

    # Test assertIsfloat
    assertIsFloat(1.0)
    try:
        assertIsFloat(0)
    except AssertionError:
        pass

    # Test assertIsInstance
    assertIsInstance((), tuple)
    assertIsInstance([], list)
    assertIsInstance({}, dict)
    assertIsInstance(set(), set)
    try:
        assertIsInstance((), list)
    except AssertionError:
        pass

    # Test assertIsInt
    assertIsInt(1)
    try:
        assertIsInt(1.0)
    except AssertionError:
        pass

    # Test assertIsString
    assertIsString('')
    try:
        assertIsString(b'')
    except AssertionError:
        pass

    # Test assertNone
    assertNone(None)
    try:
        assertNone('')
    except AssertionError:
        pass

    # Test assertRaises
    assertRaises(AttributeError, lambda: ''.bad_method)
    try:
        assertRaises(AttributeError, lambda: ''.encode)
    except DidNotRaise:
        pass

    # Test assertTrue
    assertTrue(True)
    try:
        assertTrue(True)
    except AssertionError:
        pass

    print('All tests passed')
