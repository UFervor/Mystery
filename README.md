# Mystery - Automatic Recursion Parser

Mystery is an handy tool designed for analyzing and generating International Baccalaureate (IB) format traces through automatic recursion parsing. This tool is ideal for educators, students, and programmers who work with recursive functions and need a structured way to trace and analyze their behavior.

## Prerequisites

- Python 3.7 or higher

## Requirements

- `pip3 install astor`

## Get Started

### Import Analysis Kit

Start by importing the necessary functions from the analyzer module:

```Python
from analyzer import analyze, trace
```

### Setup Recursion Tracking

Define a list to keep track of the recursion stack:

```Python
stack = []
```

### Define and Decorate Your Function

Write your recursive function. Use the `@trace` decorator to enable tracing:

```Python
@trace(stack)
def mystery(x):
    if x > 0:
        return mystery(x-1) * x
    else:
        return 1
```

### Execute and Analyze

Call your function with desired parameters and analyze the trace:

```Python
mystery(5)
analyze(mystery, stack)  # This will print and return the result in list format
```

### Example Output

```
mystery(5)
= mystery(4) * 5
= mystery(3) * 4 * 5
= mystery(2) * 3 * 4 * 5
= mystery(1) * 2 * 3 * 4 * 5
= mystery(0) * 1 * 2 * 3 * 4 * 5
= 1 * 1 * 2 * 3 * 4 * 5
= 120
```
