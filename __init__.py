"""A minimal, non-magical, non-class-based testing library.
"""
import asyncio
from argparse import ArgumentParser
from decimal import Decimal
from sys import stdout

###############################################################################
# Custom Exceptions
###############################################################################

class Skip(Exception): pass
class DidNotRaise(AssertionError): pass

###############################################################################
# Testing helpers
###############################################################################

def assertTrue(x):
    if x is not True:
        raise AssertionError(f'{x} is not True')

def assertFalse(x):
    if x is not False:
        raise AssertionError(f'{x} is not False')

def assertNone(x):
    if x is not None:
        raise AssertionError(f'{x} is not None')

def assertEqual(result, expected):
    if result != expected:
        raise AssertionError(
            f'Expected ({repr(expected)}), got ({repr(result)})'
        )

def assertRaises(exc, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except exc as e:
        return e
    else:
        raise DidNotRaise(f'{exc.__name__} not raised')

async def assertAsyncRaises(exc, fn, *args, **kwargs):
    try:
        await fn(*args, **kwargs)
    except exc as e:
        return e
    else:
        raise DidNotRaise(f'{exc.__name__} not raised')

def assertIsInstance(v, cls):
    if not isinstance(v, cls):
        raise AssertionError(
            f'Value ({repr(v)}) is not of type ({repr(cls)})'
        )

_get_assertIsInstance = lambda t: lambda v: assertIsInstance(v, t)
assertIsInt = _get_assertIsInstance(int)
assertIsFloat = _get_assertIsInstance(float)
assertIsDecimal = _get_assertIsInstance(Decimal)
assertIsString = _get_assertIsInstance(str)
assertIsBytes = _get_assertIsInstance(bytes)

###############################################################################
# Test Runner
###############################################################################

_fn_cls = type(lambda: None)

# Define a helper to return the names of functions in _globals that start with
# "test_" and satisfy a predicate.
get_test_func_names = lambda _globals, pred: [
    k for k, v in sorted(_globals.items())
    if k.startswith('test_') and pred(k) and isinstance(v, _fn_cls)
]

def run_tests(_globals, fn_names=None, fn_name_prefixes=None):
    # If fn_names is specified, run those functions, otherwise run all
    # global functions with a name that starts with "test_".
    if fn_names:
        # Get all the function names that match a name in fn_names.
        fn_names = get_test_func_names(_globals, lambda x: x in fn_names)
    elif fn_name_prefixes:
        # Get all the function names that match a prefix in fn_name_prefixes.
        fn_names = get_test_func_names(
            _globals,
            lambda x: any(x.startswith(y) for y in fn_name_prefixes)
        )
    else:
        # Get all the function names that start with "test_".
        fn_names = get_test_func_names(_globals, lambda x: True)

    event_loop = asyncio.get_event_loop()

    failure_name_exc_pairs = []
    for fn_name in fn_names:
        stdout.write(fn_name)
        stdout.flush()
        fn = _globals[fn_name]
        try:
            # If test function is a coroutine, execute it with the event loop.
            if asyncio.iscoroutinefunction(fn):
                event_loop.run_until_complete(fn())
            else:
                fn()
        except Skip:
            stdout.write(' - SKIPPED\n')
        except Exception as e:
            stdout.write(' - FAILED\n')
            failure_name_exc_pairs.append((fn_name, e))
        else:
            stdout.write(' - ok\n')
        finally:
            stdout.flush()

    if failure_name_exc_pairs:
        print()
        print('Failure details')
        print('---------------')
        print()
        for fn_name, exc in failure_name_exc_pairs:
            print(f'{fn_name} - FAILED')
            print(f'{type(exc)} - "{str(exc)}"')
            print()
        # Exit with a non-zero code.
        exit(1)

###############################################################################
# Command line interface
###############################################################################

def cli(_globals):
    parser = ArgumentParser()
    # Add a --test argument to allow the specification of individual test
    # function names to run.
    g = parser.add_mutually_exclusive_group()
    g.add_argument('--test', action='append',
                   help='The name of a test function to run')
    g.add_argument('--test-prefix', action='append',
                   help='The prefix of the function names to run')
    args = parser.parse_args()

    run_tests(_globals, args.test, args.test_prefix)
