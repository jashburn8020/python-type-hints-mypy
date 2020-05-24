# Python type hints using mypy

- [Python type hints using mypy](#python-type-hints-using-mypy)
  - [Introduction](#introduction)
  - [Getting started](#getting-started)
    - [Function signatures and dynamic vs static typing](#function-signatures-and-dynamic-vs-static-typing)
    - [More function signatures](#more-function-signatures)
    - [The `typing` module](#the-typing-module)
    - [Local type inference](#local-type-inference)
    - [Library stubs and typeshed](#library-stubs-and-typeshed)
    - [Configuring mypy](#configuring-mypy)
  - [Using mypy with an existing codebase](#using-mypy-with-an-existing-codebase)
    - [1. Start small](#1-start-small)
    - [2. Mypy runner script](#2-mypy-runner-script)
    - [3. Continuous Integration](#3-continuous-integration)
    - [4. Annotate widely imported modules](#4-annotate-widely-imported-modules)
    - [5. Write annotations as you go](#5-write-annotations-as-you-go)
    - [6. Automate annotation of legacy code](#6-automate-annotation-of-legacy-code)
    - [Speed up mypy runs](#speed-up-mypy-runs)
    - [Introduce stricter options](#introduce-stricter-options)
  - [Built-in types](#built-in-types)
  - [Sources](#sources)

## Introduction

- Mypy is a static type checker for Python 3 and Python 2.7
- Type annotations are just hints for mypy and don't interfere when running your program
- You can annotate your code using the Python 3 function annotation syntax (using the [PEP 484](https://www.python.org/dev/peps/pep-0484) notation) or a comment-based annotation syntax for Python 2 code

## Getting started

- See [`getting_started.py`](ch02/getting_started.py)
- See also [Type hints cheat sheet (Python 3)](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)

### Function signatures and dynamic vs static typing

- A function without type annotations is considered to be dynamically typed by mypy
  - by default, mypy will not type check dynamically typed functions
  - you can check by using the `--strict` flag

```python
def greeting_dynamic(name):
    """Dynamically typed function."""
    return "Hello " + name


greeting_dynamic("stranger")
```

```console
$ mypy --pretty --strict ch02/getting_started.py
ch02/getting_started.py:5: error: Function is missing a type annotation
    def greeting_dynamic(name):
    ^
ch02/getting_started.py:10: error: Call to untyped function "greeting_dynamic"
in typed context
    greeting_dynamic("stranger")
    ^
```

- You can add type annotations (also known as type hints) to the function
  - the function is then statically typed
  - mypy can use the provided type hints to detect incorrect usages

```python
def greeting_typed(name: str) -> str:
    """Statically typed function."""
    return "Hello " + name


greeting_typed(3)
```

```console
$ mypy --pretty --strict ch02/getting_started.py
ch02/getting_started.py:18: error: Argument 1 to "greeting_typed" has
incompatible type "int"; expected "str"
    greeting_typed(3)
                   ^
```

- Being able to pick whether you want a function to be dynamically or statically typed can be very helpful
  - if you are migrating an existing Python codebase to use static types, it's usually easier to migrate incrementally
  - similarly, when you are prototyping a new feature, it may be convenient to initially implement the code using dynamic typing and only add type hints later once the code is more stable
  - once you are finished migrating or prototyping your code, you can make mypy warn you if you add a dynamic function by mistake by using the `--disallow-untyped-defs` flag

### More function signatures

- If a function **does not explicitly return a value**, give it a return type of `None`
  - without the `None` return type, the function will be dynamically typed

```python
def no_return() -> None:
    """No return value."""
    print("hello")


some_value = no_return()
```

```console
$ mypy --pretty --strict ch02/getting_started.py
ch02/getting_started.py:26: error: "no_return" does not return a value
    some_value = no_return()
                 ^
```

- **Arguments with default values**

```python
def argument_default_value(name: str, excited: bool = False) -> str:
    # ...
```

- `*args` and `**kwargs` arguments

```python
def args_and_kwargs(*args: int, **kwargs: float) -> None:
    """Annotating `*args` and `**kwargs` arguments."""
    # 'args' has type 'Tuple[int, ...]' (a tuple of ints)
    # 'kwargs' has type 'Dict[str, float]' (a dict of strs to floats)
```

### The `typing` module

- You can find many of these more complex static types inside of the **`typing`** module

```python
from typing import List

def complex_static_type(names: List[str]) -> None:
    """Complex static type - `List`"""
    for name in names:
        print("Hello " + name)


complex_static_type(["Alice", "Bob", "Charlie"])
complex_static_type([10, 20])
complex_static_type(("Alice", "Bob", "Charlie"))
```

```console
$ mypy --pretty --strict ch02/getting_started.py
ch02/getting_started.py:56: error: List item 0 has incompatible type "int";
expected "str"
    complex_static_type([10, 20])
                         ^
ch02/getting_started.py:56: error: List item 1 has incompatible type "int";
expected "str"
    complex_static_type([10, 20])
                             ^
ch02/getting_started.py:57: error: Argument 1 to "complex_static_type" has
incompatible type "Tuple[str, str, str]"; expected "List[str]"
    complex_static_type(("Alice", "Bob", "Charlie"))
                         ^
```

- The `List` type is an example of something called a _generic type_: it can accept one or more _type parameters_
- In this case, we parameterized `List` by writing **`List[str]`**
  - `greet_all` accepts specifically lists containing strings, and not lists containing ints or any other type
- If the function would run just fine if you were to pass in a tuple, a set, or any other custom iterable, you can use the **`Iterable`** type

```python
from typing import Iterable

def complex_static_type_iterable(names: Iterable[str]) -> None:
    """Complex static type - `Iterable`"""
    for name in names:
        print("Hello " + name)


complex_static_type_iterable(["Alice", "Bob", "Charlie"])
complex_static_type_iterable(("Alice", "Bob", "Charlie"))
```

- Suppose you want to write a function that can accept either ints or strings, but no other types, you can express this using the **`Union`** type

```python
from typing import Union

def union_type(user_id: Union[int, str]) -> str:
    """`Union` type to accept both `int` and `str`"""
    if isinstance(user_id, int):
        return "user-{}".format(100000 + user_id)
    return user_id
```

- Suppose that you want the function to accept only strings or `None`, you can use the type **`Optional[str]`**
  - shorthand or alias for `Union[str, None]`

```python
from typing import Optional

def optional_type(name: Optional[str] = None) -> str:
    """`Optional` type to also accept a `None`."""
    # Optional[str] means the same thing as Union[str, None]
    if name is None:
        name = "stranger"
    return "Hello, " + name
```

- When adding types, the convention is to import types using the form **`from typing import Iterable`**

### Local type inference

- Once you have added type hints to a function, mypy will
  - automatically type check that function's body
  - try and infer as many details as possible
- Mypy will warn you if it is unable to determine the type of some variable

```python
untyped_global_dict = {}
```

```console
$ mypy --pretty --strict ch02/getting_started.py
ch02/getting_started.py:85: error: Need type annotation for
'untyped_global_dict' (hint: "untyped_global_dict: Dict[<type>, <type>] = ...")
    untyped_global_dict = {}
    ^
```

- You could annotate it using either variable annotations (introduced in Python 3.6 by [PEP 526](https://www.python.org/dev/peps/pep-0526)) or using a comment-based syntax

```python
# If you're using Python 3.6+
annotated_global_dict: Dict[int, float] = {}

# If you want compatibility with older versions of Python
comment_typed_global_dict = {}  # type: Dict[int, float]
```

### Library stubs and typeshed

- Mypy uses library stubs to type check code interacting with library modules, including the Python standard library
- A library stub defines a skeleton of the public interface of the library, including classes, variables and functions, and their types
- Mypy ships with stubs from the [typeshed](https://github.com/python/typeshed) project
  - contains library stubs for the Python builtins, the standard library, and selected third-party packages
- Mypy complains if it can't find a stub (or a real module) for a library module that you import
  - you can install a 3rd party module with additional stubs

### Configuring mypy

- Suppose you want to make sure all functions within your codebase are using static typing
  - run mypy with the **`--disallow-untyped-defs`** flag
- Another potentially useful flag is **`--strict`**
  - enables many (though not all) of the available strictness options – including `--disallow-untyped-defs`
  - mostly useful if you're starting a new project from scratch
  - will probably be too aggressive if you either plan on using many untyped third party libraries or are trying to add static types to a large, existing codebase

## Using mypy with an existing codebase

### 1. Start small

- If your codebase is large, pick a subset of your codebase and run mypy only on this subset at first, without any annotations
- You'll likely need to fix some mypy errors, either by
  - inserting annotations requested by mypy, or
  - adding `# type: ignore` comments to silence errors you don't want to fix now
- Mypy often generates errors about modules that it can’t find or that don’t have stub files
- You can also use a mypy configuration file, which is convenient if there are a large number of errors to ignore
  - e.g., to disable errors about importing `frobnicate`:

```ini
[mypy-frobnicate.*]
ignore_missing_imports = True
```

- Mypy follows imports by default
  - can result in a few files passed on the command line causing mypy to process a large number of imported files
    - resulting in lots of errors you don't want to deal with at the moment
  - config file option to disable this behavior
    - this can hide errors, it's not recommended for most users

### 2. Mypy runner script

- Introduce a mypy runner script that runs mypy, so that every developer will use mypy consistently
  - ensure that the correct version of mypy is installed
  - specify mypy config file or command-line options
  - provide set of files to type check
    - you may want to implement inclusion and exclusion filters for full control of the file list

### 3. Continuous Integration

- Set up your Continuous Integration (CI) system to run mypy to ensure that developers won't introduce bad annotations

### 4. Annotate widely imported modules

- It's a good idea to annotate widely imported modules pretty early on
  - this allows code using these modules to be type checked more effectively

### 5. Write annotations as you go

- Consider adding something like these in your code style conventions:
  - add annotations for any new code
  - write annotations when you modify existing code

### 6. Automate annotation of legacy code

- There are tools for automatically adding draft annotations based on type profiles collected at runtime
  - [MonkeyType](https://monkeytype.readthedocs.io/en/latest/index.html) (Python 3)
  - [PyAnnotate](https://github.com/dropbox/pyannotate) (type comments only).
- A simple approach is to collect types from test runs
  - may work well if your test coverage is good
- Another approach is to enable type collection for a small, random fraction of production network requests
  - requires more care, as type collection could impact the reliability or the performance of your service

### Speed up mypy runs

- You can use mypy daemon to get much faster incremental mypy runs
- If your project has at least 100,000 lines of code or so, you may also want to set up remote caching for further speedups

### Introduce stricter options

- Once you get started with static typing, you may want to explore the various strictness options mypy provides to catch more bugs

## Built-in types

- See:
  - https://mypy.readthedocs.io/en/stable/builtin_types.html
  - [`typing`](https://docs.python.org/3/library/typing.html) module
- The type `Dict` is a **generic class**, signified by type arguments within `[...]`
  - e.g., `Dict[int, str]` is a dictionary from integers to strings
- `List` is another generic class
- `Dict` and `List` are aliases for the built-ins `dict` and `list`, respectively
- `Iterable`, `Sequence`, and `Mapping` are generic types that correspond to **Python protocols** ([PEP 544](https://www.python.org/dev/peps/pep-0544/))
  - e.g., a `str` object or a `List[str]` object is valid when `Iterable[str]` or `Sequence[str]` is expected
  - note that even though they are similar to abstract base classes defined in [`collections.abc`](https://docs.python.org/3/library/collections.abc.html#module-collections.abc) (Python 3.8), they are not identical
    - the built-in collection type objects do not support indexing

## Sources

- "Welcome to Mypy Documentation!" _Mypy Documentation_, mypy.readthedocs.io/en/stable/index.html.
