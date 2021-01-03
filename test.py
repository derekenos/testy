
import asyncio
import sys
from decimal import Decimal

from __init__ import (
    DidNotRaise,
    assertAsyncRaises,
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
    run_tests,
)

def test_assertEqual():
    assertEqual(0, 0)
    try:
        assertEqual(0, 1)
    except AssertionError:
        pass

def test_assertFalse():
    assertFalse(False)
    try:
        assertFalse(True)
    except AssertionError:
        pass

def test_assertIsBytes():
    assertIsBytes(b'')
    try:
        assertIsBytes('')
    except AssertionError:
        pass

def test_assertIsDecimal():
    assertIsDecimal(Decimal('0'))
    try:
        assertIsDecimal(0)
    except AssertionError:
        pass

def test_assertIsFloat():
    assertIsFloat(1.0)
    try:
        assertIsFloat(0)
    except AssertionError:
        pass

def test_assertIsInstance():
    assertIsInstance((), tuple)
    assertIsInstance([], list)
    assertIsInstance({}, dict)
    assertIsInstance(set(), set)
    try:
        assertIsInstance((), list)
    except AssertionError:
        pass

def test_assertIsInt():
    assertIsInt(1)
    try:
        assertIsInt(1.0)
    except AssertionError:
        pass

def test_assertIsString():
    assertIsString('')
    try:
        assertIsString(b'')
    except AssertionError:
        pass

def test_assertNone():
    assertNone(None)
    try:
        assertNone('')
    except AssertionError:
        pass

def test_assertRaises():
    assertRaises(AttributeError, lambda: ''.bad_method)
    try:
        assertRaises(AttributeError, lambda: ''.encode)
    except DidNotRaise:
        pass

def test_assertTrue():
    # Test assertTrue
    assertTrue(True)
    try:
        assertTrue(True)
    except AssertionError:
        pass

async def test_async():
    assert True

async def test_assertAsyncRaises():
    async def f():
        raise AssertionError
    await assertAsyncRaises(AssertionError, f)

###############################################################################
# CLI
###############################################################################

def wrap(fn, fn_name, called):
    """Wrap fn to add fn_name to called on invocation.
    """
    async def async_wrapper(*args, **kwargs):
        await fn(*args, **kwargs)
        called.add(fn_name)
    def wrapper(*args, **kwargs):
        fn(*args, **kwargs)
        called.add(fn_name)
    return async_wrapper if asyncio.iscoroutinefunction(fn) else wrapper

def main():
    # Get a dict of all the test functions in this module, wrapping each
    # function with wrap()
    called = set()
    funcs_d = {
        k: wrap(v, k, called) for k, v in globals().items()
        if k.startswith('test_')
    }
    assert len(funcs_d) > 0

    # Use run_tests() to run the tests.
    run_tests(funcs_d)

    assert all(k in called for k in funcs_d)

if __name__ == '__main__':
    main()
