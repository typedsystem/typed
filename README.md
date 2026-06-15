```python
   /00                                         /00
  | 00                                        | 00
 /000000   /00   /00  /000000   /000000   /0000000
|_  00_/  | 00  | 00 /00__  00 /00__  00 /00__  00
  | 00    | 00  | 00| 00  \ 00| 00000000| 00  | 00
  | 00 /00| 00  | 00| 00  | 00| 00_____/| 00  | 00
  |  0000/|  0000000| 0000000/|  0000000|  0000000
   \___/   \____  00| 00____/  \_______/ \_______/
           /00  | 00| 00|                          
          |  000000/| 00|                          
           \______/ |__/
```

# About

`typed` is the main library of [typesystem](https://github.com/typedsystem.com), a Python framework focused in providing type safety and allowing universal constructions.

# Overview

The library allows the construction of custom type systems (actually, sub-type systems of Python builtin type system), being strongly influenced by the Type Theory dialect. This means:

1. to allow the definition of new _stratified universes_
2. which extend _abstract types_
3. from which one can create _types_
4. being associated to _terms_.

# Install

The stable version can be installed from `pypi`:

With `pip`:

```bash
pip install typedsystem
```

The in-development version can be obtained from this repository:

```bash
pip install git+https://github.com/typedsystem/typed
```

# Documentation

Please, see [typedsystem.com](https://typedsystem.com).
