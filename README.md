# testy
A minimal, non-magical, non-class-based testing library.

## Usage

### Define your tests
#### `test.py`

```
from testy import (
    assertEqual,
    cli,
)

def test_a_pass():
    assertEqual('this', 'this')

def test_a_fail():
    assertEqual('this', 'that')
    
if __name__ == '__main__':
    # Pass the globals() object to the cli() so that it can find
    # your functions with a name like "test_*".
    cli(globals())
```

### Run all tests
```
python3 test.py
```
#### Output
```
test_a_fail - FAILED
test_a_pass - ok

Failure details
---------------

test_a_fail - FAILED
<class 'AssertionError'> - "Expected ('that'), got ('this')"
```

### Run specific tests
#### Run a single test
```
python3 test.py --test test_a_pass
```
##### Output
```
test_a_pass - ok
```

#### Run multiple tests
```
python3 test.py --test test_a_pass --test test_a_fail
```
##### Output
```
test_a_pass - ok
test_a_fail - FAILED

Failure details
---------------

test_a_fail - FAILED
<class 'AssertionError'> - "Expected ('that'), got ('this')"
```
