
from __init__ import (
    assertEqual,
    cli,
)

def test_a_pass():
    assertEqual('this', 'this')

def test_a_fail():
    assertEqual('this', 'that')

if __name__ == '__main__':
    # Pass the globals() object to the cli() so that it can find
    # your test functions.
    cli(globals())
