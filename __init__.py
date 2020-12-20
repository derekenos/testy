"""A minimal, non-magical, non-class-based testing library.
"""
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

def run_tests(_globals, fn_names=None):
    # If fn_names is specified, run those functions, otherwise run all
    # global functions with a name that starts with "test_".
    if fn_names is None:
        fn_cls = type(run_tests)
        fn_names = [
            k for k, v in sorted(_globals.items())
            if k.startswith('test_') and isinstance(v, fn_cls)
        ]

    failure_name_exc_pairs = []
    for fn_name in fn_names:
        stdout.write('testing {}'.format(fn_name[5:]))
        stdout.flush()
        try:
            _globals[fn_name]()
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
        print('*************************')
        print('**** Failure Details ****')
        print('*************************')
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
    parser.add_argument('--test', action="append")
    args = parser.parse_args()

    if args.test is not None:
        bad_names = [x for x in args.test if not x.startswith('test_')]
        if bad_names:
            parser.error('--test args are expected to start with "test_", '\
                         f'got: {bad_names}')

    run_tests(_globals, args.test)
