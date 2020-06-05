# Python type hints using mypy

- [Python type hints using mypy](#python-type-hints-using-mypy)
  - [1. Introduction](#1-introduction)
  - [2. Getting started](#2-getting-started)
    - [Function signatures and dynamic vs static typing](#function-signatures-and-dynamic-vs-static-typing)
    - [More function signatures](#more-function-signatures)
    - [The `typing` module](#the-typing-module)
    - [Local type inference](#local-type-inference)
    - [Library stubs and typeshed](#library-stubs-and-typeshed)
    - [Configuring mypy](#configuring-mypy)
  - [3. Using mypy with an existing codebase](#3-using-mypy-with-an-existing-codebase)
    - [1. Start small](#1-start-small)
    - [2. Mypy runner script](#2-mypy-runner-script)
    - [3. Continuous Integration](#3-continuous-integration)
    - [4. Annotate widely imported modules](#4-annotate-widely-imported-modules)
    - [5. Write annotations as you go](#5-write-annotations-as-you-go)
    - [6. Automate annotation of legacy code](#6-automate-annotation-of-legacy-code)
    - [Speed up mypy runs](#speed-up-mypy-runs)
    - [Introduce stricter options](#introduce-stricter-options)
  - [4. Built-in types](#4-built-in-types)
  - [5. Type inference and type annotations](#5-type-inference-and-type-annotations)
    - [Type inference](#type-inference)
    - [Explicit types for variables](#explicit-types-for-variables)
    - [Explicit types for collections](#explicit-types-for-collections)
    - [Compatibility of container types](#compatibility-of-container-types)
    - [Context in type inference](#context-in-type-inference)
    - [Declaring multiple variable types at a time](#declaring-multiple-variable-types-at-a-time)
    - [Starred expressions](#starred-expressions)
  - [6. Kinds of types](#6-kinds-of-types)
    - [Class types](#class-types)
    - [The `Any` type](#the-any-type)
    - [`Tuple` types](#tuple-types)
    - [`Callable` types (and lambdas)](#callable-types-and-lambdas)
    - [`Union` types](#union-types)
    - [`Optional` types and the `None` type](#optional-types-and-the-none-type)
    - [Disabling strict optional checking](#disabling-strict-optional-checking)
    - [Class name forward references](#class-name-forward-references)
    - [Type aliases](#type-aliases)
    - [Named tuples](#named-tuples)
    - [The type of class objects](#the-type-of-class-objects)
    - [`Text` and `AnyStr`](#text-and-anystr)
    - [Generators](#generators)
  - [7. Class basics](#7-class-basics)
    - [Instance and class attributes](#instance-and-class-attributes)
    - [Annotating `__init__` methods](#annotating-init-methods)
    - [Class attribute annotations](#class-attribute-annotations)
    - [Overriding statically typed methods](#overriding-statically-typed-methods)
    - [Abstract base classes and multiple inheritance](#abstract-base-classes-and-multiple-inheritance)
  - [8. Protocols and structural subtyping](#8-protocols-and-structural-subtyping)
    - [Predefined protocols](#predefined-protocols)
    - [Simple user-defined protocols](#simple-user-defined-protocols)
    - [Defining subprotocols and subclassing protocols](#defining-subprotocols-and-subclassing-protocols)
    - [Recursive protocols](#recursive-protocols)
    - [Using `isinstance()` with protocols](#using-isinstance-with-protocols)
    - [Callback protocols](#callback-protocols)
  - [10. Dynamically typed code](#10-dynamically-typed-code)
    - [Operations on `Any` values](#operations-on-any-values)
    - [`Any` vs. `object`](#any-vs-object)
  - [11. Casts and type assertions](#11-casts-and-type-assertions)
  - [12. Duck type compatibility](#12-duck-type-compatibility)
  - [13. Creating a stub](#13-creating-a-stub)
    - [Stub file syntax](#stub-file-syntax)
    - [Using stub file syntax at runtime](#using-stub-file-syntax-at-runtime)
  - [14. Generics](#14-generics)
    - [Defining generic classes](#defining-generic-classes)
    - [Generic class internals](#generic-class-internals)
    - [Defining sub-classes of generic classes](#defining-sub-classes-of-generic-classes)
    - [Generic functions](#generic-functions)
    - [Generic methods and generic self](#generic-methods-and-generic-self)
    - [Variance of generic types](#variance-of-generic-types)
    - [Type variables with value restriction](#type-variables-with-value-restriction)
    - [Type variables with upper bounds](#type-variables-with-upper-bounds)
    - [Declaring decorators](#declaring-decorators)
      - [Decorator factories](#decorator-factories)
    - [Generic protocols](#generic-protocols)
    - [Generic type aliases](#generic-type-aliases)
  - [14.1 PEP 483 -- The Theory of Type Hints](#141-pep-483----the-theory-of-type-hints)
    - [Background](#background)
      - [Subtype relationships](#subtype-relationships)
    - [Summary of gradual typing](#summary-of-gradual-typing)
      - [Types vs. Classes](#types-vs-classes)
    - [Generic types](#generic-types)
      - [Covariance and Contravariance](#covariance-and-contravariance)
  - [15. More types](#15-more-types)
    - [The `NoReturn` type](#the-noreturn-type)
    - [`NewType`s](#newtypes)
    - [Function overloading](#function-overloading)
      - [Runtime behavior](#runtime-behavior)
      - [Type checking calls to overloads](#type-checking-calls-to-overloads)
      - [Type checking the variants](#type-checking-the-variants)
      - [Type checking the implementation](#type-checking-the-implementation)
    - [Advanced uses of self-types](#advanced-uses-of-self-types)
      - [Restricted methods in generic classes](#restricted-methods-in-generic-classes)
      - [Mixin classes](#mixin-classes)
      - [Precise typing of alternative constructors](#precise-typing-of-alternative-constructors)
    - [Typing `async`/`await`](#typing-asyncawait)
    - [`TypedDict`](#typeddict)
      - [Totality](#totality)
      - [Supported operations](#supported-operations)
      - [Class-based syntax](#class-based-syntax)
      - [Mixing required and non-required items](#mixing-required-and-non-required-items)
      - [Unions of `TypedDict`s](#unions-of-typeddicts)
  - [16. Literal types](#16-literal-types)
    - [Parameterizing Literals](#parameterizing-literals)
    - [Declaring literal variables](#declaring-literal-variables)
    - [Intelligent indexing](#intelligent-indexing)
    - [Tagged unions](#tagged-unions)
    - [Limitations](#limitations)
  - [Sources](#sources)

## 1. Introduction

- Mypy is a static type checker for Python 3 and Python 2.7
- Type annotations are just hints for mypy and don't interfere when running your program
- You can annotate your code using the Python 3 function annotation syntax (using the [PEP 484](https://www.python.org/dev/peps/pep-0484) notation) or a comment-based annotation syntax for Python 2 code

## 2. Getting started

- See also [Type hints cheat sheet (Python 3)](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)

### Function signatures and dynamic vs static typing

- See [`function_signatures_dynamic_static.py`](ch02/function_signatures_dynamic_static.py)
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
$ mypy --pretty --strict ch02/function_signatures_dynamic_static.py
ch02/function_signatures_dynamic_static.py:4: error: Function is missing a type
annotation
    def greeting_dynamic(name):
    ^
ch02/function_signatures_dynamic_static.py:9: error: Call to untyped function
"greeting_dynamic" in typed context
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
$ mypy --pretty --strict ch02/function_signatures_dynamic_static.py
ch02/function_signatures_dynamic_static.py:17: error: Argument 1 to
"greeting_typed" has incompatible type "int"; expected "str"
    greeting_typed(3)
                   ^
```

- Being able to pick whether you want a function to be dynamically or statically typed can be very helpful
  - if you are migrating an existing Python codebase to use static types, it's usually easier to migrate incrementally
  - similarly, when you are prototyping a new feature, it may be convenient to initially implement the code using dynamic typing and only add type hints later once the code is more stable
  - once you are finished migrating or prototyping your code, you can make mypy warn you if you add a dynamic function by mistake by using the `--disallow-untyped-defs` flag

### More function signatures

- See [`more_function_signatures.py`](ch02/more_function_signatures.py)
- If a function **does not explicitly return a value**, give it a return type of `None`
  - without the `None` return type, the function will be dynamically typed

```python
def no_return() -> None:
    """No return value."""
    print("hello")


some_value = no_return()
```

```console
$ mypy --pretty --strict ch02/more_function_signatures.py
ch02/more_function_signatures.py:9: error: "no_return" does not return a value
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

- See [`the_typing_module.py`](ch02/the_typing_module.py)
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
$ mypy --pretty --strict ch02/the_typing_module.py
ch02/the_typing_module.py:13: error: List item 0 has incompatible type "int";
expected "str"
    complex_static_type([10, 20])
                         ^
ch02/the_typing_module.py:13: error: List item 1 has incompatible type "int";
expected "str"
    complex_static_type([10, 20])
                             ^
ch02/the_typing_module.py:14: error: Argument 1 to "complex_static_type" has
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

- See [`local_type_inference.py`](ch02/local_type_inference.py)
- Once you have added type hints to a function, mypy will
  - automatically type check that function's body
  - try and infer as many details as possible
- Mypy will warn you if it is unable to determine the type of some variable

```python
untyped_global_dict = {}
```

```console
$ mypy --pretty --strict ch02/local_type_inference.py
ch02/local_type_inference.py:3: error: Need type annotation for
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

## 3. Using mypy with an existing codebase

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
- Since mypy supports gradual typing, it's okay to leave some of these modules unannotated

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

## 4. Built-in types

- See:
  - <https://mypy.readthedocs.io/en/stable/builtin_types.html>
  - [`typing`](https://docs.python.org/3/library/typing.html) module
- The type `Dict` is a **generic class**, signified by type arguments within `[...]`
  - e.g., `Dict[int, str]` is a dictionary from integers to strings
- `List` is another generic class
- `Dict` and `List` are aliases for the built-ins `dict` and `list`, respectively
- `Iterable`, `Sequence`, and `Mapping` are generic types that correspond to **Python protocols** ([PEP 544](https://www.python.org/dev/peps/pep-0544/))
  - e.g., a `str` object or a `List[str]` object is valid when `Iterable[str]` or `Sequence[str]` is expected
  - note that even though they are similar to abstract base classes defined in [`collections.abc`](https://docs.python.org/3/library/collections.abc.html#module-collections.abc), they are not identical
    - the built-in collection type objects do not support indexing

## 5. Type inference and type annotations

### Type inference

- Mypy considers the initial assignment as the definition of a variable
- If you do not explicitly specify the type of the variable, mypy infers the type based on the static type of the value expression:

```python
i = 1           # Infer type "int" for i
l = [1, 2]      # Infer type "List[int]" for l
```

- Type inference is not used in dynamically typed functions (those without a function type annotation)
  - every local variable type defaults to `Any` in such functions

### Explicit types for variables

- See [`explicit_types_vars.py`](ch05/explicit_types_vars.py)
- You can override the inferred type of a variable by using a **variable type annotation**
- Mypy checks that the type of the initializer is compatible with the declared type

```python
invalid_initializer: Union[int, str] = 1.1  # Error!
```

```console
$ mypy --pretty --strict ch05/explicit_types_vars.py
ch05/explicit_types_vars.py:6: error: Incompatible types in assignment
(expression has type "float", variable has type "Union[int, str]")
    invalid_initializer: Union[int, str] = 1.1
                                           ^
```

- The variable annotation syntax is available starting from Python 3.6
- In earlier Python versions, you can use a special comment after an assignment statement to declare the type of a variable:

```python
special_comment_type = 1  # type: Union[int, str]
```

- Variable annotation syntax allows defining the type of a variable without initialization:

```python
x: str
```

### Explicit types for collections

- See [`explicit_types_collections.py`](ch05/explicit_types_collections.py)
- The type checker cannot always infer the type of a list or a dictionary
  - often arises when creating an empty list or dictionary
  - give the type explicitly using a type annotation

```python
empty_list: List[int] = []
empty_dict: Dict[str, int] = {}
empty_set: Set[int] = set()
```

### Compatibility of container types

- See [`compatibility_container_types.py`](ch05/compatibility_container_types.py)
- The following program generates a mypy error since `List[int]` is not compatible with `List[object]`:
  - allowing the assignment could result in non-`int` values stored in a list of `int`

```python
def incompatible_lists(object_list: List[object], int_list: List[int]) -> None:
    """Incompatible container types."""
    object_list = int_list
```

```console
$ mypy --pretty --strict ch05/compatibility_container_types.py
ch05/compatibility_container_types.py:8: error: Incompatible types in
assignment (expression has type "List[int]", variable has type "List[object]")
        object_list = int_list
                      ^
ch05/compatibility_container_types.py:8: note: "List" is invariant -- see http://mypy.readthedocs.io/en/latest/common_issues.html#variance
ch05/compatibility_container_types.py:8: note: Consider using "Sequence" instead, which is covariant
```

- Other container types like `Dict` and `Set` behave similarly

### Context in type inference

- See [`context_type_inference.py`](ch05/context_type_inference.py)
- Type inference is bidirectional and takes context into account
- In an assignment, the type context is determined by the assignment target

```python
def type_context_assignment_target(object_list: List[object]) -> None:
    """Type context is determined by the assignment target."""
    object_list = [1, 2]  # Infer type List[object] for [1, 2], not List[int]
```

- Declared argument types are also used for type context

```python
def declared_arg_type_context(int_list: List[int]) -> None:
    """Declared argument types are used for type context."""
    print("Items:", "".join(str(a) for a in int_list))


declared_arg_type_context([])  # OK
```

### Declaring multiple variable types at a time

- See [`declaring_multiple_var_types.py`](ch05/declaring_multiple_var_types.py)
- You can declare more than a single variable at a time, but only with a type comment

```python
multiple_vars_int, multiple_vars_bool = 0, False  # type: int, bool
```

### Starred expressions

- See [`starred_expressions.py`](ch05/starred_expressions.py)
- Mypy can infer the type of starred expressions from the right-hand side of an assignment, but not always:

```python
int_1, *ints_a = 1, 2, 3  # OK
int_2, int_3, *ints_b = 1, 2  # Error: Type of ints_b cannot be inferred
```

```console
$ mypy --pretty --strict ch05/starred_expressions.py
ch05/starred_expressions.py:5: error: Need type annotation for 'ints_b' (hint:
"ints_b: List[<type>] = ...")
    int_2, int_3, *ints_b = 1, 2  # Error: Type of ints_b cannot be inferr...
                   ^
```

- Mypy cannot infer the type of `ints_b`, because there is no right-hand side value for `ints_b` to infer the type from

## 6. Kinds of types

### Class types

- See [`class_types.py`](ch06/class_types.py)
- Every class is also a valid type
- Any instance of a subclass is also compatible with all superclasses
  - every value is compatible with the `object` type
- Mypy analyzes the bodies of classes to determine which methods and attributes are available in instances

```python
class SuperClass:
    def method_a(self) -> int:  # Type of self inferred (SuperClass)
        return 2


class SubClass(SuperClass):
    def method_a(self) -> int:
        return 3

    def method_b(self) -> int:
        return 4


def print_methods(clazz: SuperClass) -> None:
    print(clazz.method_a())  # 3
    clazz.method_b()  # Error: "SuperClass" has no attribute "method_b"


print_methods(SubClass())  # OK (SubClass is a subclass of SuperClass)
```

```console
$ mypy --pretty --strict ch06/class_types.py
ch06/class_types.py:19: error: "SuperClass" has no attribute "method_b"; maybe
"method_a"?
        clazz.method_b()  # Error: "SuperClass" has no attribute "method_b...
        ^
```

### The `Any` type

- A value with the `Any` type is dynamically typed
- `Any` is compatible with every other type, and vice versa
- If you do not define a function return value or argument types, these default to `Any`

### `Tuple` types

- See [`tuple_types.py`](ch06/tuple_types.py)

```python
def tuple_type(some_tuple: Tuple[int, str]) -> None:
    """Fixed-length tuple."""
    some_tuple = 1, "foo"  # OK
    some_tuple = "foo", 1  # Type check error
```

```console
$ mypy --pretty --strict ch06/tuple_types.py
ch06/tuple_types.py:9: error: Incompatible types in assignment (expression has
type "Tuple[str, int]", variable has type "Tuple[int, str]")
        some_tuple = "foo", 1  # Type check error
                     ^
```

- A tuple type of this kind has exactly a specific number of items
- Tuples can also be used as immutable, varying-length sequences
  - use the type `Tuple[T, ...]` (with a literal `...`)

```python
def var_length_tuple(some_tuple: Tuple[int, ...]) -> None:
    """Variable length tuple."""
    for elem in some_tuple:
        print(elem, elem ** 2)


var_length_tuple(())  # OK
var_length_tuple((1, 3, 5))  # OK
var_length_tuple([1, 2])  # Error: only a tuple is valid
```

```console
$ mypy --pretty --strict ch06/tuple_types.py
ch06/tuple_types.py:20: error: Argument 1 to "var_length_tuple" has
incompatible type "List[int]"; expected "Tuple[int, ...]"
    var_length_tuple([1, 2])  # Error: only a tuple is valid
                     ^
```

- Note: Usually it's a better idea to use `Sequence[T]` instead of `Tuple[T, ...]`, as `Sequence` is also compatible with lists and other non-tuple sequences

### `Callable` types (and lambdas)

- See [`callable_types_lambdas.py`](ch06/callable_types_lambdas.py)
- You can pass around function objects and bound methods in statically typed code
- The type of a function that accepts arguments `A1`, …, `An` and returns `Rt` is `Callable[[A1, ..., An], Rt]`

```python
def callable_type(num: int, a_callable: Callable[[int], int]) -> int:
    """Callable type."""
    return a_callable(a_callable(num))


def some_callable(num: int) -> int:
    return num + 1


print(callable_type(3, some_callable))  # 5
```

- In callable types, you can only have positional arguments, and only ones without default values
- Mypy recognizes a special form `Callable[..., T]` (with a literal `...`)
  - compatible with arbitrary callable objects that return a type compatible with `T`
    - independent of the number, types or kinds of arguments
  - the arguments are treated similar to a `(*args: Any, **kwargs: Any)` function signature

```python
def arbitrary_call(arbitrary_args_callable: Callable[..., int]) -> int:
    """Callable type with arbitrary arguments."""
    return arbitrary_args_callable("x") + arbitrary_args_callable(y=2)


arbitrary_call(ord)  # No static error, but fails at runtime
arbitrary_call(open)  # Error: does not return an int
arbitrary_call(1)  # Error: 'int' is not callable
```

```console
$ mypy --pretty --strict ch06/callable_types_lambdas.py
ch06/callable_types_lambdas.py:24: error: Argument 1 to "arbitrary_call" has
incompatible type
"Callable[[Union[str, bytes, int, _PathLike[Any]], str, int, Optional[str], Optional[str], Optional[str], bool, Optional[Callable[[str, int], int]]], IO[Any]]";
expected "Callable[..., int]"
    arbitrary_call(open)  # Error: does not return an int
                   ^
ch06/callable_types_lambdas.py:25: error: Argument 1 to "arbitrary_call" has
incompatible type "int"; expected "Callable[..., int]"
    arbitrary_call(1)  # Error: 'int' is not callable
                   ^
```

- In situations where more precise or complex types of callbacks are necessary one can use flexible callback protocols
- **Lambdas** are also supported
  - lambda argument and return value types cannot be given explicitly; they are always inferred based on context using bidirectional type inference
- If you want to give the argument or return value types explicitly, use an ordinary, perhaps nested function definition

```python
# Infer x as int and some_iterator as Iterator[int]
some_iterator = map(lambda x: x + 1, [1, 2, 3])
```

### `Union` types

- See [`union_types.py`](ch06/union_types.py)
- Python functions often accept values of two or more different types
- Use the `Union[T1, ..., Tn]` type constructor to construct a union type

```python
def union_type(arg: Union[int, str]) -> None:
    """Union type."""
    print(arg + 1)  # Error: str + int is not valid
    if isinstance(arg, int):
        print(arg + 1)  # OK
    else:
        print(arg + "a")  # OK


union_type(1)  # OK
union_type("x")  # OK
union_type(1.1)  # Error
```

```console
$ mypy --pretty --strict ch06/union_types.py
ch06/union_types.py:8: error: Unsupported operand types for + ("str" and "int")
        print(arg + 1)  # Error: str + int is not valid
                    ^
ch06/union_types.py:8: note: Left operand is of type "Union[int, str]"
ch06/union_types.py:17: error: Argument 1 to "union_type" has incompatible type
"float"; expected "Union[int, str]"
    union_type(1.1)  # Error
               ^
```

### `Optional` types and the `None` type

- See [`optional_none_types.py`](ch06/optional_none_types.py)
- You can use the `Optional` type modifier to define a type variant that allows `None`
  - `Optional[X]` is the preferred shorthand for `Union[X, None]`
- Mypy recognizes regular Python idioms to guard against `None` values
  - `if x is None`
  - `if x is not None`
  - `if x`
  - `if not x`

```python
def optional_arg_return(some_str: Optional[str]) -> Optional[int]:
    """Optional type in argument and return value."""
    if not some_str:
        return None  # OK
    # Mypy will infer the type of some_str to be str due to the check against None
    return len(some_str)
```

- Sometimes mypy doesn't realize that a value is never `None`
  - happens when a class instance can exist in a partially defined state
    - some attribute is initialized to `None` during object construction
    - a method assumes that the attribute is no longer `None`
  - mypy will complain about the possible `None` value
  - use `assert x is not None` to work around this

```python
class Resource:
    """Mypy does not realize that if initialize() is called, self.path is never None."""

    path: Optional[str] = None

    def initialize(self, path: str) -> None:
        self.path = path

    def read(self) -> str:
        # We require that the object has been initialized.
        # assert self.path is not None
        with open(self.path) as file_obj:  # OK if assert above is uncommented
            return file_obj.read()


resource = Resource()
resource.initialize("/foo/bar")
resource.read()
```

```console
$ mypy --pretty --strict ch06/optional_none_types.py
ch06/optional_none_types.py:24: error: Argument 1 to "open" has incompatible
type "Optional[str]"; expected "Union[str, bytes, int, _PathLike[Any]]"
            with open(self.path) as file_obj:  # OK if assert above is unc...
                      ^
```

- Mypy generally uses the first assignment to a variable to infer the type of the variable
  - if you assign both a `None` value and a non-`None` value in the same scope, mypy can usually do the right thing without an annotation

```python
def same_scope_assignment(i: int) -> None:
    """Type inference when further assignment is done in the same scope."""
    num = None  # Inferred type Optional[int] because of the assignment below
    if i > 0:
        num = i

    print(num)
```

### Disabling strict optional checking

- Mypy has an option to treat `None` as a valid value for every type
  - in case you don't want to introduce optional types to your codebase yet
  - through the `--no-strict-optional` command line option
  - in this mode `None` is also valid for primitive types such as `int` and `float`, and `Optional` types are not required
  - it will cause mypy to silently accept some buggy code – not recommended
- You can use the mypy configuration file to migrate your code to strict optional checking one file at a time
  - using the per-module flag `strict_optional`

### Class name forward references

- See [`class_name_forward_refs.py`](ch06/class_name_forward_refs.py)
- Python does not allow references to a class object before the class is defined
  - you can enter the type as a string literal - this is a _forward reference_
  - string literal types must be defined (or imported) later in the _same module_

```python
def no_forward_reference(clazz: SomeClass) -> None:
    """Python does not allow references to a class object before the class is defined.
    """


def forward_reference(clazz: "SomeClass") -> None:
    """Enter the type as a string literal - forward reference."""


class SomeClass:
    """Class defined after references."""
```

### Type aliases

- Type names may end up being long and painful to type
- You can define a type alias by simply assigning the type to a variable

```python
AliasType = Union[List[Dict[Tuple[int, str], Set[int]]], Tuple[str, List[str]]]

# Now we can use AliasType in place of the full name:

def f() -> AliasType:
    ...
```

### Named tuples

- See [`named_tuples.py`](ch06/named_tuples.py)
- Mypy recognizes named tuples and can type check code that defines or uses them
- If you use `namedtuple` to define your named tuple, all the items are assumed to have `Any` types
- You can use **`NamedTuple`** to define item types
- Python 3.6 introduced an alternative, class-based syntax for named tuples with types

```python
# namedtuple - all the items are assumed to have Any types
Point = namedtuple("Point", ["x", "y"])
point = Point(x=1, y="two")

# Use NamedTuple to also define item types
TypedPoint = NamedTuple("TypedPoint", [("x", int), ("y", int)])
# Argument has incompatible type "str"; expected "int"
typed_point = TypedPoint(x=1, y="two")


class ClassBasedPoint(NamedTuple):
    """Class-based syntax for named tuples with types."""

    x: int
    y: int


# # Argument has incompatible type "str"; expected "int"
class_based_point = ClassBasedPoint(x=1, y="two")
```

```console
$ mypy --pretty --strict ch06/named_tuples.py
ch06/named_tuples.py:13: error: Argument "y" to "TypedPoint" has incompatible
type "str"; expected "int"
    typed_point = TypedPoint(x=1, y="two")
                                    ^
ch06/named_tuples.py:24: error: Argument "y" to "ClassBasedPoint" has
incompatible type "str"; expected "int"
    class_based_point = ClassBasedPoint(x=1, y="two")
                                               ^
```

### The type of class objects

- See [`type_of_class_objects.py`](ch06/type_of_class_objects.py)
- Sometimes you want to talk about class objects that inherit from a given class
- Can be spelled as `Type[C]` where `C` is a class
  - using `C` to annotate an argument declares that the argument is an instance of `C` (or of a subclass of `C`)
  - using `Type[C]` as an argument annotation declares that the argument is a class object deriving from `C` (or `C` itself)

```python
class User:
    # Defines fields like name, email
    pass


class BasicUser(User):
    def upgrade(self) -> None:
        """Upgrade to Pro"""


class ProUser(User):
    def pay(self) -> None:
        """Pay bill"""


def new_user(user_class: type) -> User:
    """The best we can do without Type."""
    user = user_class()
    # (Here we could write the user object to a database)
    return user


buyer = new_user(ProUser)
buyer.pay()  # Rejected, not a method on User


U = TypeVar("U", bound=User)


def typed_new_user(user_class: Type[U]) -> U:
    user = user_class()
    # (Here we could write the user object to a database)
    return user


beginner = typed_new_user(BasicUser)  # Inferred type is BasicUser
beginner.upgrade()  # OK
```

```console
$ mypy --pretty --strict ch06/type_of_class_objects.py
ch06/type_of_class_objects.py:25: error: Returning Any from function declared
to return "User"
        return user
        ^
ch06/type_of_class_objects.py:29: error: "User" has no attribute "pay"
    buyer.pay()  # Rejected, not a method on User
    ^
```

### `Text` and `AnyStr`

- See [`text_and_anystr.py`](ch06/text_and_anystr.py)
- You may want to write a function which will accept only unicode strings
  - challenging to do in a codebase intended to run in both Python 2 and Python 3
    - `str` means something different in both versions
    - `unicode` is not a keyword in Python 3
- Use `Text`, which is aliased to
  - `unicode` in Python 2
  - `str` in Python 3
- Use **`AnyStr`**
  - to write a function that will work with any kind of string but will not let you mix two different string types

```python
def unicode_only(unicode_str: Text) -> Text:
    """Accept only unicode strings in a cross-compatible way."""
    return unicode_str + u"\u2713"


def concat(str1: AnyStr, str2: AnyStr) -> AnyStr:
    """Works with any kind of strings, but not mix different types."""
    return str1 + str2


concat("a", "b")  # Okay
concat(b"a", b"b")  # Okay
concat("a", b"b")  # Error: cannot mix bytes and unicode
```

```console
$ mypy --pretty --strict ch06/text_and_anystr.py
ch06/text_and_anystr.py:18: error: Value of type variable "AnyStr" of "concat"
cannot be "object"
    concat("a", b"b")  # Error: cannot mix bytes and unicode
    ^
```

### Generators

- See [`generators.py`](ch06/generators.py)
- A basic generator that only yields values can be annotated as having a return type of either `Iterator[YieldType]` or `Iterable[YieldType]`

```python
def squares(num: int) -> Iterator[int]:
    """Basic generator that only yields values."""
    for i in range(num):
        yield i * i
```

- If you want your generator to accept values via the `send()` method or return a value
  - use the `Generator[YieldType, SendType, ReturnType]` generic type
  - note that unlike many other generics in the typing module, the `SendType` of `Generator` behaves contravariantly, not covariantly or invariantly

```python
def echo_round() -> Generator[int, float, str]:
    """Generator to accept values via the `send()` method or return a value."""
    sent = yield 0
    while sent >= 0:
        sent = yield round(sent)
    return "Done"
```

- If you do not plan on receiving or returning values, then set the `SendType` or `ReturnType` to `None`, as appropriate
  - slightly different from using `Iterable[int]` or `Iterator[int]`, since generators have `close()`, `send()`, and `throw()` methods that generic iterables don't
  - if you will call these methods on the returned generator, use the `Generator` type instead of `Iterable` or `Iterator`

## 7. Class basics

### Instance and class attributes

- See [`instance_class_attrs.py`](ch07/instance_class_attrs.py)
- Mypy detects if you are trying to access a missing attribute
  - mypy infers the types of attributes

```python
class SingleAttribute:
    """Class with a single `present` attribute."""

    def __init__(self, present: int) -> None:
        self.present = present  # inferred attribute of type 'int'


single = SingleAttribute(1)
single.present = 2  # OK
single.absent = 3  # Error
```

```console
$ mypy --pretty --strict ch07/instance_class_attrs.py
ch07/instance_class_attrs.py:15: error: "SingleAttribute" has no attribute
"absent"
    single.absent = 3  # Error
    ^
```

- You can declare types of variables in the class body explicitly using a type annotation
  - as in Python generally, a variable defined in the class body can be used as a class or an instance variable

```python
class DeclaredAttribute:
    """Class with declared attribute."""

    attr: List[int]  # Declare attribute 'x' of type List[int]


declared = DeclaredAttribute()
declared.attr = [1]  # OK
```

- You can give explicit types to instance variables defined in a method

```python
class InstanceVarDefinedInMethod:
    """Explicit types to instance variables defined in a method."""

    def __init__(self) -> None:
        self.x: List[int] = []

    def some_func(self) -> None:
        self.y: Any = 0
```

### Annotating `__init__` methods

- See [`annotating_init_methods.py`](ch07/annotating_init_methods.py)
- The `__init__` method doesn't return a value
  - best expressed as `-> None`
  - it is allowed to omit the return type declaration if at least one argument is annotated
  - in the following classes, `__init__` is considered fully annotated

```python
class InitNoneReturn:
    """`__init__` `None` return type declared."""

    def __init__(self) -> None:
        self.var = 42


class InitNoNoneReturn:
    """`__init__` return type not declared, but argument is annotated."""

    def __init__(self, arg: int):
        self.var = arg
```

- If `__init__` has no annotated arguments and no return type annotation, it is considered an untyped method

### Class attribute annotations

- See [`class_attr_annotations.py`](ch07/class_attr_annotations.py)
- You can use a `ClassVar[t]` annotation to explicitly declare that a particular attribute should not be set on instances
- It's not necessary to annotate all class variables using `ClassVar`
  - an attribute without the `ClassVar` annotation can still be used as a class variable
  - mypy won't prevent it from being used as an instance variable
- Note: A `ClassVar` type parameter cannot include type variables
  - `ClassVar[T]` and `ClassVar[List[T]]` are both invalid if `T` is a type variable

```python
class ClassVariable:
    """`ClassVar` annotation."""

    var: ClassVar[int] = 0  # Class variable only


ClassVariable.var += 1  # OK

class_var = ClassVariable()
class_var.var = 1  # Error
print(class_var.var)  # OK -- can be read through an instance
```

```console
$ mypy --pretty --strict ch07/class_attr_annotations.py
ch07/class_attr_annotations.py:15: error: Cannot assign to class variable "var"
via instance
    class_var.var = 1  # Error
    ^
```

### Overriding statically typed methods

- See [`overriding_methods.py`](ch07/overriding_methods.py)
- When overriding a statically typed method, mypy checks that the override has a compatible signature

```python
class Base:
    def some_func(self, x: int) -> None:
        pass


class Derived1(Base):
    def some_func(self, x: str) -> None:  # Error: type of 'x' incompatible
        pass


class Derived2(Base):
    def some_func(self, x: int, y: int) -> None:  # Error: too many arguments
        pass


class Derived3(Base):
    def some_func(self, x: int) -> None:  # OK
        pass


class Derived4(Base):
    def some_func(self, x: float) -> None:  # OK: mypy treats int as a subtype of float
        pass


class Derived5(Base):
    def some_func(self, x: int, y: int = 0) -> None:  # OK: accepts more than the base
        pass  #     class method
```

```console
$ mypy --pretty --strict ch07/overriding_methods.py
ch07/overriding_methods.py:10: error: Argument 1 of "some_func" is incompatible
with supertype "Base"; supertype defines the argument type as "int"
        def some_func(self, x: str) -> None:  # Error: type of 'x' incompa...
        ^
ch07/overriding_methods.py:15: error: Signature of "some_func" incompatible
with supertype "Base"
        def some_func(self, x: int, y: int) -> None:  # Error: too many ar...
        ^
```

- You can vary return types _covariantly_ in overriding
  - you could override the return type `Iterable[int]` with a subtype such as `List[int]`
- You can vary argument types _contravariantly_
  - subclasses can have more general argument types
- You can override a statically typed method with a dynamically typed one
  - allows dynamically typed code to override methods defined in library classes without worrying about their type signatures

```python
class StaticBase:
    def inc(self, x: int) -> int:
        return x + 1


class DynamicDerived(StaticBase):
    def inc(self, x):  # Override, dynamically typed
        return "hello"  # Incompatible with 'StaticBase', but no mypy error
```

### Abstract base classes and multiple inheritance

- See [`abstract_base_class_multiple_inheritance.py`](ch07/abstract_base_class_multiple_inheritance.py)
- Mypy supports Python [abstract base classes](https://docs.python.org/3/library/abc.html) (ABCs)
  - abstract classes have at least one abstract method or property that must be implemented by any concrete (non-abstract) subclass
  - you can define abstract base classes using the `abc.ABCMeta` metaclass and the `@abc.abstractmethod` function decorator

```python
class Animal(metaclass=ABCMeta):
    @abstractmethod
    def eat(self, food: str) -> None:
        pass

    @property
    @abstractmethod
    def can_walk(self) -> bool:
        pass


class Cat(Animal):
    def eat(self, food: str) -> None:
        pass  # Body omitted

    @property
    def can_walk(self) -> bool:
        return True


x = Animal()  # Error: 'Animal' is abstract due to 'eat' and 'can_walk'
y = Cat()  # OK
```

```console
$ mypy --pretty --strict ch07/abstract_base_class_multiple_inheritance.py
ch07/abstract_base_class_multiple_inheritance.py:26: error: Cannot instantiate
abstract class 'Animal' with abstract attributes 'can_walk' and 'eat'
    x = Animal()  # Error: 'Animal' is abstract due to 'eat' and 'can_walk...
        ^
```

- Since you can't create instances of ABCs, they are most commonly used in type annotations
- Whether a particular class is abstract or not is somewhat implicit
  - in the example below, `Derived` is treated as an abstract base class
    - `Derived` inherits an abstract `base_method` method from `Base` and doesn't explicitly implement it
  - the definition of `Derived` generates no errors from mypy, since it's a valid ABC
  - attempting to create an instance of `Derived` will be rejected

```python
class Base(metaclass=ABCMeta):
    @abstractmethod
    def base_method(self, x: int) -> None:
        pass


class Derived(Base):  # No error -- Derived is implicitly abstract
    def derived_method(self) -> None:
        pass


d = Derived()  # Error: 'Derived' is abstract
```

```console
$ mypy --pretty --strict ch07/abstract_base_class_multiple_inheritance.py
ch07/abstract_base_class_multiple_inheritance.py:41: error: Cannot instantiate
abstract class 'Derived' with abstract attribute 'base_method'
    d = Derived()  # Error: 'Derived' is abstract
        ^
```

## 8. Protocols and structural subtyping

- Mypy supports two ways of deciding whether two classes are compatible as types
  - **nominal subtyping** is strictly based on the class hierarchy
    - if class `D` inherits class `C`, it's also a subtype of `C`
    - instances of `D` can be used when `C` instances are expected
  - **structural subtyping**
    - class `D` is a structural subtype of class `C` if `D` has all attributes and methods of `C`, and with compatible types
    - can be seen as a static equivalent of duck typing
    - Mypy provides support for structural subtyping via **protocol classes**
    - see [PEP 544](https://www.python.org/dev/peps/pep-0544/) for the detailed specification of protocols and structural subtyping

### Predefined protocols

- The `typing` module defines various protocol classes that correspond to common Python protocols, such as `Iterable[T]`
- If a class defines a suitable `__iter__` method, mypy understands that it implements the iterable protocol and is compatible with `Iterable[T]`

```python
class IntList:
    def __init__(self, value: int, next: Optional["IntList"]) -> None:
        self.value = value
        self.next = next

    def __iter__(self) -> Iterator[int]:
        current: Optional[IntList] = self
        while current:
            yield current.value
            current = current.next


def print_numbered(items: Iterable[int]) -> None:
    for n, x in enumerate(items):
        print(n + 1, x)


x = IntList(3, IntList(5, None))
print_numbered(x)  # OK
print_numbered([4, 5])  # Also OK
```

- See <https://mypy.readthedocs.io/en/stable/protocols.html#predefined-protocols> for all built-in protocols defined in `typing` and the signatures of the corresponding methods you need to define to implement each protocol
- Iteration protocols
  - e.g., they allow iteration of objects in `for` loops
  - `Iterable[T]`
  - `Iterator[T]`
- Collection protocols
  - many of these are implemented by built-in container types such as `list` and `dict`, and these are also useful for user-defined collection objects
  - `Sized`
    - type for objects that support `len(x)`
  - `Container[T]`
    - type for objects that support the `in` operator
  - `Collection[T]`
- One-off protocols
  - these protocols are typically only useful with a single standard library function or class
  - `Reversible[T]`
    - type for objects that support `reversed(x)`
  - `SupportsAbs[T]`
    - type for objects that support `abs(x)`, which returns a value of type `T`
  - `SupportsBytes`
    - type for objects that support `bytes(x)`
  - `SupportsComplex`
    - type for objects that support `complex(x)`
    - note that no arithmetic operations are supported
  - `SupportsFloat`
    - type for objects that support `float(x)`
    - note that no arithmetic operations are supported
  - `SupportsInt`
    - type for objects that support `int(x)`
    - note that no arithmetic operations are supported
  - `SupportsRound[T]`
    - type for objects that support `round(x)`
- Async protocols
  - these protocols can be useful in async code
  - `Awaitable[T]`
  - `AsyncIterable[T]`
  - `AsyncIterator[T]`
- Context manager protocols
  - there are two protocols for context managers
    - for regular context managers
    - for async ones
  - these allow defining objects that can be used in `with` and `async with` statements
  - `ContextManager[T]`
  - `AsyncContextManager[T]`

### Simple user-defined protocols

- See [`user_defined_protocols.py`](ch08/user_defined_protocols.py), [`greeting_protocol.py`](ch08/greeting_protocol.py)
- You can define your own protocol class by inheriting the special **`Protocol`** class

```python
class SupportsClose(Protocol):
    def close(self) -> None:
        pass  # Empty method body (explicit '...')


class Resource:  # No SupportsClose base class!
    # ... some methods ...

    def close(self) -> None:
        self.resource.release()


def close_all(items: Iterable[SupportsClose]) -> None:
    for item in items:
        item.close()


close_all([Resource(), open("some/file")])  # Okay!
```

- `Resource` is a subtype of the `SupportsClose` protocol since it defines a compatible `close` method
- Regular file objects returned by `open()` are similarly compatible with the protocol, as they support `close()`

### Defining subprotocols and subclassing protocols

- See [`subprotocols.py`](ch08/subprotocols.py)
- You can also define subprotocols
- Existing protocols can be extended and merged using multiple inheritance

```python
# ... continuing from previous example


class SupportsRead(Protocol):
    def read(self, amount: int) -> bytes:
        ...


class TaggedReadableResource(SupportsClose, SupportsRead, Protocol):
    label: str


class AdvancedResource(Resource):
    def __init__(self, label: str) -> None:
        self.label = label

    def read(self, amount: int) -> bytes:
        # some implementation
        ...


resource: TaggedReadableResource
resource = AdvancedResource("handle with care")  # OK
```

- Note that inheriting from an existing protocol does not automatically turn the subclass into a protocol
  - it just creates a regular (non-protocol) class or ABC that implements the given protocol (or protocols)
  - the `Protocol` base class must always be explicitly present if you are defining a protocol

```python
class NotAProtocol(SupportsClose):  # This is NOT a protocol
    new_attr: int


class Concrete:
    new_attr: int = 0

    def close(self) -> None:
        ...


# Error: nominal subtyping used by default
x: NotAProtocol = Concrete()  # Error!
```

```console
$ mypy --pretty --strict ch08/subprotocols.py
ch08/subprotocols.py:61: error: Incompatible types in assignment (expression
has type "Concrete", variable has type "NotAProtocol")
    x: NotAProtocol = Concrete()  # Error!
                      ^
```

- You can include default implementations of methods in protocols
  - if you explicitly subclass these protocols you can inherit these default implementations
- Explicitly including a protocol as a base class is also a way of documenting that your class implements a particular protocol
  - forces mypy to verify that your class implementation is actually compatible with the protocol

### Recursive protocols

- See [`recursive_protocols.py`](ch08/recursive_protocols.py)
- Protocols can be recursive (self-referential) and mutually recursive
  - useful for declaring abstract recursive collections such as trees and linked lists

```python
class TreeLike(Protocol):
    value: int

    @property
    def left(self) -> Optional["TreeLike"]:
        ...

    @property
    def right(self) -> Optional["TreeLike"]:
        ...


class SimpleTree:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Optional["SimpleTree"] = None
        self.right: Optional["SimpleTree"] = None


root: TreeLike = SimpleTree(0)  # OK
```

### Using `isinstance()` with protocols

- See [`isinstance_with_protocols.py`](ch08/isinstance_with_protocols.py)
- You can use a protocol class with `isinstance()` if you decorate it with the `@runtime_checkable` class decorator
  - the decorator adds support for basic runtime structural checks
  - `isinstance()` also works with the predefined protocols in `typing` such as `Iterable`
  - `isinstance()` with protocols is not completely safe at runtime
    - e.g., signatures of methods are not checked
    - the runtime implementation only checks that all protocol members are defined

```python
@runtime_checkable
class Portable(Protocol):
    handles: int


class Mug:
    def __init__(self) -> None:
        self.handles = 1


mug = Mug()
if isinstance(mug, Portable):
    use(mug.handles)  # Works statically and at runtime
```

### Callback protocols

- See [`callback_protocols.py`](ch08/callback_protocols.py)
- Protocols can be used to define flexible callback types that are hard (or even impossible) to express using the `Callable[...]` syntax
  - such as variadic, overloaded, and complex generic callbacks
  - they are defined with a special `__call__` member

```python
class Combiner(Protocol):
    def __call__(self, *vals: bytes, maxlen: Optional[int] = None) -> List[bytes]:
        ...


def batch_proc(data: Iterable[bytes], cb_results: Combiner) -> bytes:
    for item in data:
        ...


def good_cb(*vals: bytes, maxlen: Optional[int] = None) -> List[bytes]:
    ...


def bad_cb(*vals: bytes, maxitems: Optional[int]) -> List[bytes]:
    ...


batch_proc([], good_cb)  # OK
# Error! Argument 2 has incompatible type because of different name and kind in the
# callback
batch_proc([], bad_cb)
```

```console
$ mypy --pretty --strict ch08/callback_protocols.py
ch08/callback_protocols.py:28: error: Argument 2 to "batch_proc" has
incompatible type
"Callable[[VarArg(bytes), NamedArg(Optional[int], 'maxitems')], List[bytes]]";
expected "Combiner"
    batch_proc([], bad_cb)
                   ^
```

- Callback protocols and `Callable` types can be used interchangeably
  - keyword argument names in `__call__` methods must be identical, unless a double underscore prefix is used

```python
T = TypeVar("T")


class Copy(Protocol):
    def __call__(self, __origin: T) -> T:
        ...


copy_a: Callable[[T], T]
copy_b: Copy

copy_a = copy_b  # OK
copy_b = copy_a  # Also OK
```

## 10. Dynamically typed code

- See [`dynamically_typed_code.py`](ch10/dynamically_typed_code.py)
- Bodies of functions that don't have any explicit types in their function annotation are dynamically typed
- Code outside functions is statically typed by default, and types of variables are inferred
  - you can also make any variable dynamically typed by defining it explicitly with the type `Any`

```python
s = 1  # Statically typed (type int)
s = "x"  # Type check error

d: Any = 1  # Dynamically typed (type Any)
d = "x"  # OK
```

```console
$ mypy --pretty --strict ch10/dynamically_typed_code.py
ch10/dynamically_typed_code.py:6: error: Incompatible types in assignment
(expression has type "str", variable has type "int")
    s = "x"  # Type check error
        ^
```

### Operations on `Any` values

- You can do anything using a value with type `Any`, and type checker does not complain
- Values derived from an `Any` value also often have the type `Any` implicitly, as mypy can't infer a more precise result type
  - e.g., if you get the attribute of an `Any` value or call a `Any` value the result is `Any`

```python
def f(x: Any) -> None:
    y = x.foo()  # y has type Any
    y.bar()      # Okay as well!
```

### `Any` vs. `object`

- The type `object` is another type that can have an instance of arbitrary type as a value
- Unlike `Any`, `object` is an ordinary static type, and only operations valid for all types are accepted for `object` values
- You can use `cast()` or `isinstance()` to go from a general type such as `object` to a more specific type (subtype) such as `int`
  - `cast()` is not needed with dynamically typed values (values with type `Any`)

## 11. Casts and type assertions

- See [`casts_type_assertions.py`](ch11/casts_type_assertions.py)
- Mypy supports type casts that are usually used to coerce a statically typed value to a subtype
- Mypy casts are only used as hints for the type checker, and they don't perform a runtime type check
- Use the function **`cast()`** to perform a cast

```python
o: object = [1]
x = cast(List[int], o)  # OK
y = cast(List[str], o)  # OK (cast performs no actual runtime check)
```

- Casts are used to silence spurious type checker warnings and give the type checker a little help when it can't quite understand what is going on
- You can use an assertion if you want to perform an actual runtime check

```python
def foo(o: object) -> None:
    print(o + 5)  # Error: can't add 'object' and 'int'
    assert isinstance(o, int)
    print(o + 5)  # OK: type of 'o' is 'int' here
```

- You don't need a cast for expressions with type `Any`, or when assigning to a variable with type `Any`
- You can also use `Any` as the cast target type - this lets you perform any operations on the result

```python
x_str = 1
x_str.whatever()  # Type check error
y_any = cast(Any, x_str)
y_any.whatever()  # Type check OK (runtime error)
```

```console
$ mypy --pretty --strict ch11/casts_type_assertions.py
ch11/casts_type_assertions.py:17: error: "int" has no attribute "whatever"
    x_str.whatever()  # Type check error
    ^
```

## 12. Duck type compatibility

- Certain types are compatible even though they aren't subclasses of each other
- Mypy supports this idiom via duck type compatibility
- This is supported for a small set of built-in types:
  - `int` is duck type compatible with `float` and `complex`
  - `float` is duck type compatible with `complex`
  - in Python 2, `str` is duck type compatible with `unicode`

```python
def degrees_to_radians(degrees: float) -> float:
    return math.pi * degrees / 180

n = 90  # Inferred type 'int'
print(degrees_to_radians(n))  # Okay!
```

- You can also often use protocols and structural subtyping to achieve a similar effect in a more principled and extensible fashion

## 13. Creating a stub

- How to create a stub file:
  - write a stub file for the library (or an arbitrary module) and store it as a `.pyi` file in the same directory as the library module
  - alternatively, put your stubs (`.pyi` files) in a directory reserved for stubs (e.g., `myproject/stubs`)
    - set the environment variable `MYPYPATH` to refer to the directory
- Use the normal Python file name conventions for **modules**, e.g. `csv.pyi` for module `csv`
- Use a subdirectory with `__init__.pyi` for **packages**
  - note that [PEP 561](https://www.python.org/dev/peps/pep-0561) stub-only packages must be installed, and may not be pointed at through the `MYPYPATH`
- If a directory contains both a `.py` and a `.pyi` file for the same module, the `.pyi` file takes precedence
  - you can add annotations for a module even if you don't want to modify the source code
  - useful if you use 3rd party open source libraries in your program (and there are no stubs in typeshed yet)

### Stub file syntax

- Stub files are written in normal Python 3 syntax
  - leaving out runtime logic like variable initializers, function bodies, and default arguments
  - if not possible to completely leave out some piece of runtime logic, replace or elide them with ellipsis expressions (`...`)

```python
# Variables with annotations do not need to be assigned a value.
# So by convention, we omit them in the stub file.
x: int

# Function bodies cannot be completely removed. By convention,
# we replace them with `...` instead of the `pass` statement.
def func_1(code: str) -> int: ...

# We can do the same with default arguments.
def func_2(a: int, b: int = ...) -> int: ...
```

### Using stub file syntax at runtime

- You may also elide actual logic in regular Python code – for example, when writing methods in overload variants or custom protocols
  - use ellipses to do so, just like in stub files
  - stylistically acceptable to throw a `NotImplementedError` in cases where the user of the code may accidentally call functions with no actual logic
- You can also elide default arguments as long as the function body also contains no runtime logic:
  - the function body only contains a single ellipsis
  - the `pass` statement
  - or a raise `NotImplementedError()`
  - acceptable for the function body to contain a docstring

```python
from typing import List
from typing_extensions import Protocol

class Resource(Protocol):
    def ok_1(self, foo: List[str] = ...) -> None: ...

    def ok_2(self, foo: List[str] = ...) -> None:
        raise NotImplementedError()

    def ok_3(self, foo: List[str] = ...) -> None:
        """Some docstring"""
        pass

    # Error: Incompatible default for argument "foo" (default has
    # type "ellipsis", argument has type "List[str]")
    def not_ok(self, foo: List[str] = ...) -> None:
        print(foo)
```

## 14. Generics

### Defining generic classes

- See [`defining_generic_classes.py`](ch14/defining_generic_classes.py)
- The built-in collection classes are generic classes
- Generic types have one or more type parameters, which can be arbitrary types
  - `Dict[int, str]`
  - `List[int]`
- Programs can also define new generic classes

```python
T = TypeVar("T")


class Stack(Generic[T]):
    def __init__(self, content: Optional[List[T]] = None) -> None:
        if content is None:
            self.items = []
        else:
            self.items = content

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()

    def empty(self) -> bool:
        return not self.items
```

- The `Stack` class can be used to represent a stack of any type
- Using `Stack` is similar to built-in container types
- Type inference works for user-defined generic types

```python
# Construct an empty Stack[int] instance
stack = Stack[int]()
stack.push(2)
stack.pop()
assert stack.empty()
stack.push("x")  # Type error


def process(stack: Stack[int]) -> None:
    ...


process(Stack())  # Argument has inferred type Stack[int]


str_stack = Stack(["a", "b"])  # OK, inferred type is Stack[str]
assert not stack.empty()
str_stack.push(2)  # Type error
```

```console
$ mypy --pretty --strict ch14/defining_generic_classes.py
ch14/defining_generic_classes.py:30: error: Argument 1 to "push" of "Stack" has
incompatible type "str"; expected "int"
    stack.push("x")  # Type error
               ^
ch14/defining_generic_classes.py:42: error: Argument 1 to "push" of "Stack" has
incompatible type "int"; expected "str"
    str_stack.push(2)  # Type error
                   ^
```

### Generic class internals

- Indexing `Stack` returns essentially a copy of `Stack` that returns instances of the original class on instantiation
  - ([`__class__`](https://docs.python.org/3/library/stdtypes.html#instance.__class__) contains the class to which a class instance belongs)

```text
>>> print(Stack)
__main__.Stack
>>> print(Stack[int])
__main__.Stack[int]
>>> print(Stack[int]().__class__)
__main__.Stack
```

- Note that built-in types `list`, `dict` and so on do not support indexing in Python
  - this is why we have the aliases `List`, `Dict` and so on in the `typing` module
  - indexing these aliases gives you a class that directly inherits from the target class in Python
  - ([`__bases__`](https://docs.python.org/3/library/stdtypes.html#class.__bases__) contains a tuple of base classes of a class object)

```text
>>> from typing import List
>>> List[int]
typing.List[int]
>>> List[int].__bases__
(<class 'list'>, typing.MutableSequence)
```

- Generic types could be instantiated or subclassed as usual classes, but the above examples illustrate that type variables are erased at runtime
- Generic `Stack` instances are just ordinary Python objects
  - have no extra runtime overhead or magic due to being generic, other than a metaclass that overloads the indexing operator (`[]`)

### Defining sub-classes of generic classes

- See [`subclasses_of_generic.py`](ch14/subclasses_of_generic.py)
- User-defined generic classes and generic classes defined in `typing` can be used as base classes for other classes, both generic and non-generic

```python
KT = TypeVar("KT")
VT = TypeVar("VT")


class MyMap(Mapping[KT, VT]):
    """This is a generic subclass of Mapping."""

    def __getitem__(self, k: KT) -> VT:
        ...  # Implementations omitted

    def __iter__(self) -> Iterator[KT]:
        ...

    def __len__(self) -> int:
        ...


items: MyMap[str, int]  # Okay


class StrDict(Dict[str, str]):
    """This is a non-generic subclass of Dict."""

    def __str__(self) -> str:
        return "StrDict({})".format(super().__str__())


data: StrDict[int, int]  # Error! StrDict is not generic
data2: StrDict  # OK

T = TypeVar("T")


class Receiver(Generic[T]):
    def accept(self, value: T) -> None:
        ...


class AdvancedReceiver(Receiver[T]):
    ...
```

```console
$ mypy --pretty --strict ch14/subclasses_of_generic.py
ch14/subclasses_of_generic.py:32: error: "StrDict" expects no type arguments,
but 2 given
    data: StrDict[int, int]  # Error! StrDict is not generic
          ^
```

- Note: You have to add an explicit `Mapping` base class if you want mypy to consider a user-defined class as a mapping (and `Sequence` for sequences, etc.)
  - mypy doesn't use structural subtyping for these ABCs, unlike simpler protocols like `Iterable`
- `Generic` can be omitted from bases if there are other base classes that include type variables, such as `Mapping[KT, VT]` in the above example
  - if you include `Generic[...]` in bases, then it should list all type variables present in other bases (or more, if needed)
  - the order of type variables is defined by the following rules:
    - if `Generic[...]` is present, then the order of variables is always determined by their order in `Generic[...]`
    - if there are no `Generic[...]` in bases, then all type variables are collected in the lexicographic order (i.e. by first appearance)

```python
S = TypeVar("S")
U = TypeVar("U")
V = TypeVar("V")


class One(Generic[V]):
    ...


class Another(Generic[V]):
    ...


class First(One[V], Another[S]):
    ...


class Second(One[V], Another[S], Generic[S, U, V]):
    ...


x: First[int, str]  # Here V is bound to int, S is bound to str
y: Second[int, str, Any]  # Here S is int, U is str, and V is Any
```

### Generic functions

- See [`generic_functions.py`](ch14/generic_functions.py)
- Generic type variables can also be used to define generic functions
- A single definition of a type variable (such as `T`) can be used in multiple generic functions or classes
- A variable cannot have a type variable in its type unless the type variable is bound in a containing generic class or function

```python
T = TypeVar("T")  # Declare type variable


def first(seq: Sequence[T]) -> T:  # Generic function
    return seq[0]


def last(seq: Sequence[T]) -> T:
    """Type variable `T` is reused."""
    return seq[-1]


s = first("foo")  # s has type str.
assert s == "f"
n = first([1, 2, 3])  # n has type int.
assert n == 1
c = last((1 + 2j, 3 + 4j))  # c has type complex.
assert c == 3 + 4j
```

### Generic methods and generic self

- See [`generic_methods_self.py`](ch14/generic_methods_self.py)
- You can define generic methods
  - use a type variable in the method signature that is different from class type variables
  - `self` may also be generic, allowing a method to return the most precise type known at the point of access

```python
# Defines that `Shape` is the upper bound, i.e., an actual type substituted (explicitly
# or implicitly) for the type variable must be a subclass of the boundary type.
T = TypeVar("T", bound="Shape")


class Shape:
    def set_scale(self: T, scale: float) -> T:
        self.scale = scale
        return self


class Circle(Shape):
    def set_radius(self, r: float) -> "Circle":
        self.radius = r
        return self


class Square(Shape):
    def set_width(self, w: float) -> "Square":
        self.width = w
        return self


circle = Circle().set_scale(0.5).set_radius(2.7)  # type: Circle
square = Square().set_scale(0.5).set_width(3.2)  # type: Square
```

- Other uses are factory methods, such as copy and deserialization
- For **class methods**, you can also define generic `cls`, using `Type[T]`

```python
U = TypeVar("U", bound="Friend")


class Friend:
    other = None  # type: Friend

    @classmethod
    def make_pair(cls: Type[U]) -> Tuple[U, U]:
        a, b = cls(), cls()
        a.other = b
        b.other = a
        return a, b


class SuperFriend(Friend):
    pass


a, b = SuperFriend.make_pair()
assert isinstance(a, SuperFriend)
```

- Note that when overriding a method with generic `self`, you must either
  - return a generic `self` too, or
  - return an instance of the current class
    - in the latter case, you must implement this method in all future subclasses

### Variance of generic types

- There are 3 main kinds of generic types with respect to subtype relations between them: invariant, covariant, and contravariant
- See [Covariance and Contravariance](#covariance-and-contravariance)

### Type variables with value restriction

- See [`type_vars_value_restriction.py`](ch14/type_vars_value_restriction.py)
- By default, a type variable can be replaced with any type
- Sometimes it's useful to have a type variable that can only have some specific types as its value
- A typical example is a type variable that can only have values `str` and `bytes`:

```python
from typing import TypeVar

AnyStr = TypeVar('AnyStr', str, bytes)
```

- This is actually such a common type variable that `AnyStr` is defined in `typing`
- We can use `AnyStr` to define a function that can concatenate two strings or bytes objects
  - this is different from a union type, since combinations of `str` and `bytes` are not accepted

```python
def concat(x: AnyStr, y: AnyStr) -> AnyStr:
    return x + y


concat("a", "b")  # Okay
concat(b"a", b"b")  # Okay
concat(1, 2)  # Error!
concat("string", b"bytes")  # Error!


def union_concat(x: Union[str, bytes], y: Union[str, bytes]) -> Union[str, bytes]:
    return x + y  # Error: can't concatenate str and bytes
```

```console
$ mypy --pretty --strict ch14/type_vars_value_restriction.py
ch14/type_vars_value_restriction.py:10: error: Value of type variable "AnyStr"
of "concat" cannot be "int"
    concat(1, 2)        # Error!
    ^
ch14/type_vars_value_restriction.py:11: error: Value of type variable "AnyStr"
of "concat" cannot be "object"
    concat('string', b'bytes')   # Error!
    ^
ch14/type_vars_value_restriction.py:14: error: Unsupported operand types for +
("str" and "bytes")
        return x + y  # Error: can't concatenate str and bytes
               ^
ch14/type_vars_value_restriction.py:14: error: Unsupported operand types for +
("bytes" and "str")
        return x + y  # Error: can't concatenate str and bytes
               ^
ch14/type_vars_value_restriction.py:14: note: Both left and right operands are unions
```

- Another interesting special case is calling `concat()` with a subtype of `str`
  - you may expect that the type of `ss` is `S`, but the type is actually `str`
  - a subtype gets promoted to one of the valid values for the type variable, which in this case is `str`

```python
class S(str): pass

ss = concat(S('foo'), S('bar'))
assert isinstance(ss, str)
```

### Type variables with upper bounds

- See [`type_vars_upper_bounds.py`](ch14/type_vars_upper_bounds.py)
- A type variable can be restricted to having values that are subtypes of a specific type
- This type is called the upper bound of the type variable, and is specified with the `bound=...` keyword argument to `TypeVar`
- In the definition of a generic function that uses such a type variable `T`, the type represented by `T` is assumed to be a subtype of its upper bound, so the function can use methods of the upper bound on values of type `T`
  - in a call to such a function, the type `T` must be replaced by a type that is a subtype of its upper bound

```python
T = TypeVar("T", bound=SupportsAbs[float])


def largest_in_absolute_value(*xs: T) -> T:
    return max(xs, key=abs)  # Okay, because T is a subtype of SupportsAbs[float].


largest_in_absolute_value(-3.5, 2)  # Okay, has type float.
largest_in_absolute_value(5 + 6j, 7)  # Okay, has type complex.
# Error: 'str' is not a subtype of SupportsAbs[float].
largest_in_absolute_value("a", "b")
```

```console
$ mypy --pretty --strict ch14/type_vars_upper_bounds.py
ch14/type_vars_upper_bounds.py:15: error: Value of type variable "T" of
"largest_in_absolute_value" cannot be "str"
    largest_in_absolute_value("a", "b")
    ^
```

- Type parameters of generic classes may also have upper bounds, which restrict the valid values for the type parameter in the same way
- A type variable may not have both a value restriction

### Declaring decorators

- See [`declaring_decorators.py`](ch14/declaring_decorators.py)
- One common application of type variable upper bounds is in declaring a decorator that preserves the signature of the function it decorates, regardless of that signature
- Note that class decorators are handled differently than function decorators in mypy
  - decorating a class does not erase its type, even if the decorator has incomplete type annotations

```python
F = TypeVar("F", bound=Callable[..., Any])

# A decorator that preserves the signature.
def my_decorator(func: F) -> F:
    def wrapper(*args, **kwds):
        print("Calling", func)
        return func(*args, **kwds)

    return cast(F, wrapper)


# A decorated function.
@my_decorator
def foo(a: int) -> str:
    return str(a)


a = foo(12)
reveal_type(a)  # str
foo("x")  # Type check error: incompatible type "str"; expected "int"
```

```console
$ mypy --pretty --strict ch14/declaring_decorators.py
ch14/declaring_decorators.py:9: error: Function is missing a type annotation
        def wrapper(*args, **kwds):
        ^
ch14/declaring_decorators.py:23: note: Revealed type is 'builtins.str'
ch14/declaring_decorators.py:24: error: Argument 1 to "foo" has incompatible
type "str"; expected "int"
    foo("x")  # Type check error: incompatible type "str"; expected "int"
        ^
```

- The bound on `F` is used so that calling the decorator on a non-function (e.g. `my_decorator(1)`) will be rejected
- Note that the `wrapper()` function is not type-checked
  - wrapper functions are typically small enough that this is not a big problem
  - also the reason for the `cast()` call in the return statement in `my_decorator()`

#### Decorator factories

- See [`decorator_factories.py`](ch14/decorator_factories.py)
- Functions that take arguments and return a decorator (also called second-order decorators), are similarly supported via generics

```python
F = TypeVar("F", bound=Callable[..., Any])


def route(url: str) -> Callable[[F], F]:
    ...


@route(url="/")
def index(request: Any) -> str:
    return "Hello world"
```

- Sometimes the same decorator supports both bare calls and calls with arguments
  - achieved by combining with `@overload`

```python
F = TypeVar("F", bound=Callable[..., Any])


# Bare decorator usage
@overload
def atomic(__func: F) -> F:
    ...


# Decorator with arguments
@overload
def atomic(*, savepoint: bool = True) -> Callable[[F], F]:
    ...


# Implementation
def atomic(__func: Callable[..., Any] = None, *, savepoint: bool = True):
    def decorator(func: Callable[..., Any]):
        ...  # Code goes here

    if __func is not None:
        return decorator(__func)
    else:
        return decorator


# Usage
@atomic
def func1() -> None:
    ...


@atomic(savepoint=False)
def func2() -> None:
    ...
```

### Generic protocols

- See [`generic_protocols.py`](ch14/generic_protocols.py)
- Mypy supports generic protocols
  - see also [8. Protocols and structural subtyping](#8-protocols-and-structural-subtyping)
- Several predefined protocols are generic, such as `Iterable[T]`
- You can define additional generic protocols
  - generic protocols mostly follow the normal rules for generic classes

```python
T = TypeVar("T")


class Box(Protocol[T]):
    content: T


def do_stuff(one: Box[str], other: Box[bytes]) -> None:
    ...


class StringWrapper:
    def __init__(self, content: str) -> None:
        self.content = content


class BytesWrapper:
    def __init__(self, content: bytes) -> None:
        self.content = content


do_stuff(StringWrapper("one"), BytesWrapper(b"other"))  # OK

x: Box[float] = ...
y: Box[int] = ...
x = y  # Error -- Box is invariant
```

```console
$ mypy --pretty --strict ch14/generic_protocols.py
ch14/generic_protocols.py:31: error: Incompatible types in assignment
(expression has type "Box[int]", variable has type "Box[float]")
    x = y  # Error -- Box is invariant
        ^
```

- The main difference between generic protocols and ordinary generic classes is that mypy checks that the declared variances of generic type variables in a protocol match how they are used in the protocol definition

```python
T = TypeVar("T")

class ReadOnlyBoxInv(Protocol[T]):  # Error: covariant type variable expected
    def content(self) -> T:
        ...


T_co = TypeVar("T_co", covariant=True)


class ReadOnlyBoxCov(Protocol[T_co]):  # OK
    def content(self) -> T_co:
        ...


class CovFloatWrapper:
    def content(self) -> float:
        ...


class CovIntWrapper:
    def content(self) -> int:
        ...


ax: ReadOnlyBoxCov[float] = CovFloatWrapper()
ay: ReadOnlyBoxCov[int] = CovIntWrapper()
ax = ay  # OK -- ReadOnlyBoxCov is covariant

az: ReadOnlyBoxCov[float] = CovIntWrapper()  # OK
aerr: ReadOnlyBoxCov[int] = CovFloatWrapper()  # Error
```

```console
$ mypy --pretty --strict ch14/generic_protocols.py
ch14/generic_protocols.py:34: error: Invariant type variable 'T' used in
protocol where covariant one is expected
    class ReadOnlyBoxInv(Protocol[T]):  # Error: covariant type variable e...
    ^
ch14/generic_protocols.py:62: error: Incompatible types in assignment
(expression has type "CovFloatWrapper", variable has type "ReadOnlyBoxCov[int]")
    aerr: ReadOnlyBoxCov[int] = CovFloatWrapper()  # Error
                                ^
ch14/generic_protocols.py:62: note: Following member(s) of "CovFloatWrapper" have conflicts:
ch14/generic_protocols.py:62: note:     Expected:
ch14/generic_protocols.py:62: note:         def content(self) -> int
ch14/generic_protocols.py:62: note:     Got:
ch14/generic_protocols.py:62: note:         def content(self) -> float
```

- Generic protocols can also be recursive

```python
T = TypeVar("T")

class Linked(Protocol[T]):
    """Generic protocols can be recursive."""

    val: T

    def next(self) -> "Linked[T]":
        ...


class L:
    val: int

    ...  # details omitted

    def next(self) -> "L":
        ...  # details omitted


def last(seq: Linked[T]) -> T:
    ...  # implementation omitted


result = last(L())  # Inferred type of 'result' is 'int'
```

### Generic type aliases

- See [`generic_type_aliases.py`](ch14/generic_type_aliases.py)
- [Type aliases](#type-aliases) can be generic
- They can be used in two ways:
  - subscripted aliases are equivalent to original types with substituted type variables, so the number of type arguments must match the number of free type variables in the generic type alias
  - unsubscripted aliases are treated as original types with free variables replaced with `Any`

```python
S = TypeVar("S")

TInt = Tuple[int, S]
UInt = Union[S, int]
CBack = Callable[..., S]


def response(query: str) -> UInt[str]:  # Same as Union[str, int]
    ...


def activate(cb: CBack[S]) -> S:  # Same as Callable[..., S]
    ...


table_entry: TInt  # Same as Tuple[int, Any]

T = TypeVar("T", int, float, complex)

Vec = Iterable[Tuple[T, T]]


def inproduct(v: Vec[T]) -> T:
    return sum(x * y for x, y in v)


def dilate(v: Vec[T], scale: T) -> Vec[T]:
    return ((x * scale, y * scale) for x, y in v)


v1: Vec[int] = []  # Same as Iterable[Tuple[int, int]]
v2: Vec = []  # Same as Iterable[Tuple[Any, Any]]
v3: Vec[int, int] = []  # Error: Invalid alias, too many type arguments!
```

## 14.1 PEP 483 -- The Theory of Type Hints

### Background

- Here we assume that type is a set of values and a set of functions that one can apply to these values
- There are several ways to define a particular type:
  - by explicitly listing all values
    - e.g., `True` and `False` form the type `bool`
  - by specifying functions which can be used with variables of a type
    - e.g., all objects that have a `__len__` method form the type `Sized`
    - both `[1, 2, 3]` and `abc` belong to this type, since one can call `len` on them
      - `len([1, 2, 3]) # OK`
      - `len('abc') # also OK`
      - `len(42) # not a member of Sized`
  - by a simple class definition - all instances of a class also form a type
    - e.g., `class UserID(int)`
  - complex types
    - e.g., one can define the type `FancyList` as all lists containing only instances of `int`, `str` or their subclasses
    - the value `[1, 'abc', UserID(42)]` has this type

#### Subtype relationships

- See [`subtype_relationships.py`](ch14.1/subtype_relationships.py)
- The _subtype relation_ arises from the question:
  - if `first_var` has type `first_type`, and `second_var` has type `second_type`
    - is it safe to assign `first_var = second_var`?
    - is `second_type` a subtype of `first_type`?
- A strong criterion for when it should be safe is:
  1. every value from `second_type` (subtype) is also in the set of values of `first_type` (supertype); and
  2. every function from `first_type` (supertype) is also in the set of functions of `second_type` (subtype)
- By this definition:
  - every type is a subtype of itself
  - the set of values becomes smaller in the process of subtyping, while the set of functions becomes larger
- Example: Integers are _subtype_ of real numbers
  - every integer is of course also a real number
  - integers support more operations, such as, e.g., bitwise shifts `<<` and `>>`
- Tricky example: If `List[int]` denotes the type formed by all lists containing only integer numbers, then it is _not a subtype_ of `List[float]`, formed by all lists that contain only real numbers
  - the first condition of subtyping holds
  - but appending a real number only works with `List[float]` so that the second condition fails

```python
def append_pi(lst: List[float]) -> None:
    lst += [3.14]


my_list = [1, 3, 5]  # type: List[int]
append_pi(my_list)  # Naively, this should be safe...
my_list[-1] << 5  # ... but this fails
```

```console
$ python ch14.1/subtype_relationships.py
Traceback (most recent call last):
  File "ch14.1/subtype_relationships.py", line 21, in <module>
    my_list[-1] << 5  # ... but this fails
TypeError: unsupported operand type(s) for <<: 'float' and 'int'

$ mypy --pretty --strict ch14.1/subtype_relationships.py
ch14.1/subtype_relationships.py:20: error: Argument 1 to "append_pi" has
incompatible type "List[int]"; expected "List[float]"
    append_pi(my_list)  # Naively, this should be safe...
              ^
ch14.1/subtype_relationships.py:20: note: "List" is invariant -- see http://mypy.readthedocs.io/en/latest/common_issues.html#variance
ch14.1/subtype_relationships.py:20: note: Consider using "Sequence" instead, which is covariant
```

### Summary of gradual typing

- Gradual typing allows one to annotate only part of a program, thus leverage desirable aspects of both dynamic and static typing
- The **is-consistent-with** relationship is similar to is-subtype-of
  - not transitive when the `Any` type is involved
  - is not symmetric
  - assigning `a_value` to `a_variable` is OK if the type of `a_value` is consistent with the type of `a_variable`
  - defined by three rules:
    - a type `t1` is consistent with a type `t2` if `t1` is a subtype of `t2` (but not the other way around)
    - `Any` is consistent with every type (but `Any` is not a subtype of every type)
    - every type is consistent with `Any` (but every type is not a subtype of `Any`)
- `Any` declares a fallback to dynamic typing and shuts up complaints from the static checker

#### Types vs. Classes

- Classes are object factories defined by the `class` statement, and returned by the `type(obj)` built-in function
  - a dynamic, runtime concept
- Type concept is described above
  - types appear in variable and function type annotations
  - used by static type checkers
- Every class is a type, but it is tricky and error prone to implement a class that exactly represents semantics of a given type:
  - `int` is a class and a type
  - `UserID` is a class and a type
  - `Union[str, int]` is a type but not a proper class

### Generic types

- Generic type constructor
  - e.g., `Tuple` can take a concrete type `float` and make a concrete type `Vector = Tuple[float, ...]`
    - can take another type `UserID` and make another concrete type `Registry = Tuple[UserID, ...]`
  - similar to semantics of functions
    - a function takes a value and returns a value
    - generic type constructor takes a type and "returns" a type

#### Covariance and Contravariance

- See [`covariance_contravariance.py`](ch14.1/covariance_contravariance.py)
- If `t2` is a subtype of `t1`, then a generic type constructor `GenType` is called:
  - _covariant_, if `GenType[t2]` is a subtype of `GenType[t1]` for all such `t1` and `t2`
  - _contravariant_, if `GenType[t1]` is a subtype of `GenType[t2]` for all such `t1` and `t2`
  - _invariant_, if neither of the above is true
- **Covariant**
  - `Union` behaves covariantly in all its arguments
    - `Union[t1, t2, ...]` is a subtype of `Union[u1, u2, ...]`, if `t1` is a subtype of `u1`, etc
  - `FrozenSet[T]` is also covariant
    - consider `int` and `float` in place of `T`
    - `int` is a subtype of `float`
    - set of values of `FrozenSet[int]` is clearly a subset of values of `FrozenSet[float]`
    - set of functions from `FrozenSet[float]` is a subset of set of functions from `FrozenSet[int]`
    - by definition `FrozenSet[int]` is a subtype of `FrozenSet[float]`
- **Invariant**
  - `List[T]` is invariant
  - although set of values of `List[int]` is a subset of values of `List[float]`, only `int` could be appended to a `List[int]`
    - `List[int]` is not a subtype of `List[float]`
  - mutable types are typically invariant

```python
class Shape:
    pass

class Circle(Shape):
    def rotate(self) -> None:
        ...

def add_one(things: List[Shape]) -> None:
    things.append(Shape())

my_things: List[Circle] = []
add_one(my_things)     # This may appear safe, but...
my_things[0].rotate()  # ...this will fail
```

```console
$ mypy --pretty --strict ch14.1/covariance_contravariance.py
ch14.1/covariance_contravariance.py:18: error: Argument 1 to "add_one" has
incompatible type "List[Circle]"; expected "List[Shape]"
    add_one(my_things)     # This may appear safe, but...
            ^
ch14.1/covariance_contravariance.py:18: note: "List" is invariant -- see http://mypy.readthedocs.io/en/latest/common_issues.html#variance
ch14.1/covariance_contravariance.py:18: note: Consider using "Sequence" instead, which is covariant
```

- **Contravariant**
  - the callable type is covariant in the return type, but contravariant in the arguments
  - for two callable types that differ only in the **return type**, the subtype relationship for the callable types follows that of the return types, e.g.,
    - `Callable[[], int]` is a subtype of `Callable[[], float]`
  - for two callable types that differ only in the type of **one argument**, the subtype relationship for the callable types goes in the opposite direction as for the argument types, e.g.,
    - `Callable[[float], None]` is a subtype of `Callable[[int], None]`
    - if `Manager` is a subtype of `Employee`, and we have `def calculate_all(lst: List[Manager], salary: Callable[[Manager], Decimal]): ...`
      - a function that can calculate the salary of a manager is expected
      - a function that can calculate the salary of an employee is acceptable
        - `Callable[[Employee], Decimal]`
        - a function that operates on an `Employee` can also operate on a `Manager`
          - every value of `Manager` is also a value of `Employee`
          - every function of `Employee` is also a function of `Manager`
      - `Callable[[Employee], Decimal]` is a subtype of `Callable[[Manager], Decimal]`
  - to make more precise type annotations for functions:
    - choose the most general type for every argument
    - and the most specific type for the return value
- It is possible to declare the variance for user defined generic types by using special keywords `covariant` and `contravariant` in the definition of type variables used as parameters
  - types are invariant by default

```python
T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)

class LinkedList(Generic[T]):  # invariant by default
    ...
    def append(self, element: T) -> None:
        ...

class Box(Generic[T_co]):      #  this type is declared covariant
    def __init__(self, content: T_co) -> None:
        self._content = content
    def get_content(self) -> T_co:
        return self._content

class Sink(Generic[T_contra]): # this type is declared contravariant
    def send_to_nowhere(self, data: T_contra) -> None:
        with open(os.devnull, 'w') as devnull:
            print(data, file=devnull)
```

## 15. More types

### The `NoReturn` type

- See [`noreturn_type.py`](ch15/noreturn_type.py)
- Mypy provides support for functions that never return
  - e.g., a function that unconditionally raises an exception
- Mypy will ensure that functions annotated as returning `NoReturn` truly never return, either implicitly or explicitly
- Mypy will also recognize that the code after calls to such functions is unreachable and will behave accordingly

```python
def stop() -> NoReturn:
    raise Exception("no way")


def f(x: int) -> int:
    if x == 0:
        return x
    stop()
    return "whatever works"  # No error in an unreachable block
```

### `NewType`s

- See [`newtypes.py`](ch15/newtypes.py)
- There are situations where you may want to avoid programming errors by creating simple derived classes that are only used to distinguish certain values from base class instances

```python
class UserId(int):
    pass

def get_by_user_id(user_id: UserId):
    ...
```

- However, this approach introduces some runtime overhead
- To avoid this, the `typing` module provides a _helper function_ `NewType` that creates simple unique types with almost zero runtime overhead
- Mypy will treat the statement `Derived = NewType('Derived', Base)` as being roughly equivalent to the following definition:

```python
class Derived(Base):
    def __init__(self, _x: Base) -> None:
        ...
```

- At runtime, `NewType('Derived', Base)` will return a dummy function that simply returns its argument:

```python
def Derived(_x):
    return _x
```

- Mypy will require explicit casts from `int` where `UserId` is expected, while implicitly casting from `UserId` where `int` is expected

```python
UserId = NewType("UserId", int)


def name_by_id(user_id: UserId) -> str:
    ...


UserId("user")  # Fails type check

name_by_id(42)  # Fails type check
name_by_id(UserId(42))  # OK

num = UserId(5) + 1  # type: int
```

```console
$ mypy --pretty --strict ch15/newtypes.py
ch15/newtypes.py:12: error: Argument 1 to "UserId" has incompatible type "str";
expected "int"
    UserId("user")  # Fails type check
           ^
ch15/newtypes.py:14: error: Argument 1 to "name_by_id" has incompatible type
"int"; expected "UserId"
    name_by_id(42)  # Fails type check
               ^
```

- The function returned by `NewType` accepts only one argument; this is equivalent to supporting only one constructor accepting an instance of the base class

```python
class PacketId:
    def __init__(self, major: int, minor: int) -> None:
        self._major = major
        self._minor = minor


TcpPacketId = NewType("TcpPacketId", PacketId)

packet = PacketId(100, 100)
tcp_packet = TcpPacketId(packet)  # OK

tcp_packet = TcpPacketId(127, 0)  # Fails in type checker and at runtime
```

```console
ch15/newtypes.py:31: error: Too many arguments for "TcpPacketId"
    tcp_packet = TcpPacketId(127, 0)  # Fails in type checker and at runti...
                 ^
ch15/newtypes.py:31: error: Argument 1 to "TcpPacketId" has incompatible type
"int"; expected "PacketId"
    tcp_packet = TcpPacketId(127, 0)  # Fails in type checker and at runti...
                             ^
```

- You cannot use `isinstance()` or `issubclass()` on the object returned by `NewType()`, because function objects don't support these operations
- You cannot create subclasses of these objects either
- Unlike _type aliases_, `NewType` will create an entirely new and unique type when used
  - the intended purpose of `NewType` is to help you detect cases where you accidentally mixed together the old base type and the new derived type
  - e.g., the following will successfully typecheck when using type aliases

```python
UserId = int

def name_by_id(user_id: UserId) -> str:
    ...

name_by_id(3)  # ints and UserId are synonymous
```

### Function overloading

- See [`function_overloading.py`](ch15/function_overloading.py)
- Sometimes the arguments and types in a function depend on each other in ways that can't be captured with a `Union`
- For example, suppose we want to write a function that can accept x-y coordinates
  - if we pass in just a single x-y coordinate, we return a `ClickEvent` object
  - if we pass in two x-y coordinates, we return a `DragEvent` object

```python
def mouse_event(
    x1: int, y1: int, x2: Optional[int] = None, y2: Optional[int] = None
) -> Union[ClickEvent, DragEvent]:
```

- This function signature is too loose
  - implies `mouse_event` could return either object regardless of the number of arguments we pass in
  - does not prohibit a caller from passing in the wrong number of `int`s
- Use overloading, which lets us give the same function multiple type annotations (signatures) to more accurately describe the function's behavior

```python
# Overload *variants* for 'mouse_event'. These variants give extra information to the
# type checker. They are ignored at runtime.


@overload
def mouse_event(x1: int, y1: int) -> ClickEvent:
    ...


@overload
def mouse_event(x1: int, y1: int, x2: int, y2: int) -> DragEvent:
    ...


# The actual *implementation* of 'mouse_event'. The implementation contains the actual
# runtime logic.


def mouse_event(
    x1: int, y1: int, x2: Optional[int] = None, y2: Optional[int] = None
) -> Union[ClickEvent, DragEvent]:
    if x2 is None and y2 is None:
        return ClickEvent(x1, y1)
    elif x2 is not None and y2 is not None:
        return DragEvent(x1, y1, x2, y2)
    else:
        raise TypeError("Bad arguments")


click_event = mouse_event(1, 2)  # OK
click_event = mouse_event(1, 2, 3, 4)  # Error

drag_event = mouse_event(1, 2, 3, 4)  # OK
drag_event = mouse_event(1, 2)  # Error
drag_event = mouse_event(1, 2, 3)  # Error
```

```console
$ mypy --pretty --strict ch15/function_overloading.py
ch15/function_overloading.py:46: error: Incompatible types in assignment
(expression has type "DragEvent", variable has type "ClickEvent")
    click_event = mouse_event(1, 2, 3, 4)  # Error
                  ^
ch15/function_overloading.py:49: error: Incompatible types in assignment
(expression has type "ClickEvent", variable has type "DragEvent")
    drag_event = mouse_event(1, 2)  # Error
                 ^
ch15/function_overloading.py:50: error: No overload variant of "mouse_event"
matches argument types "int", "int", "int"
    drag_event = mouse_event(1, 2, 3)  # Error
                 ^
ch15/function_overloading.py:50: note: Possible overload variants:
ch15/function_overloading.py:50: note:     def mouse_event(x1: int, y1: int) -> ClickEvent
ch15/function_overloading.py:50: note:     def mouse_event(x1: int, y1: int, x2: int, y2: int) -> DragEvent
```

- Another example:

```python
T = TypeVar("T")


class MyList(Sequence[T]):
    def __init__(self, content: Sequence[T]) -> None:
        self.content = content

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[T]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[T, Sequence[T]]:
        if isinstance(index, int):
            # Return a T here
            return self.content[index]
        elif isinstance(index, slice):
            # Return a sequence of Ts here
            return self.content[index]
        else:
            raise TypeError("Invalid arguments")

    def __len__(self) -> int:
        return len(self.content)


my_list = MyList([1, 2, 3])
my_elem = my_list[1]  # OK
my_elem = my_list[:]  # Error

my_seq = my_list[:]  # OK
my_seq = my_list[1]  # Error
```

```console
$ mypy --pretty --strict ch15/function_overloading.py
ch15/function_overloading.py:84: error: Incompatible types in assignment
(expression has type "Sequence[int]", variable has type "int")
    my_elem = my_list[:]  # Error
              ^
ch15/function_overloading.py:87: error: Incompatible types in assignment
(expression has type "int", variable has type "Sequence[int]")
    my_seq = my_list[1]  # Error
             ^
```

#### Runtime behavior

- An overloaded function must consist of two or more overload variants followed by an implementation
  - the variants and the implementations must be adjacent in the code
  - think of them as _one indivisible unit_
- The variant bodies must all be empty; only the implementation is allowed to contain code
  - using the `pass` keyword, but the more common convention is to use the ellipsis (`...`) literal
  - at runtime, the variants are completely ignored - overridden by the final implementation function
- An overloaded function is still an ordinary Python function
  - no automatic dispatch handling
  - you must manually handle the different types in the implementation (e.g. by using `if` statements and `isinstance` checks)

#### Type checking calls to overloads

- See [`type_checking_calls.py`](ch15/type_checking_calls.py)
- When you call an overloaded function, mypy will infer the correct return type by picking the best matching variant
  - after taking into consideration both the argument types and arity
  - a call is never type checked against the implementation
- If there are multiple equally good matching variants, mypy will select the variant that was defined first
  - make sure your overload variants are listed in the same order as the runtime checks (e.g. `isinstance` checks) in your implementation
  - order your variants and runtime checks from most to least specific
- 2 exceptions to the "pick the first match" rule
  - if multiple variants match due to an argument being of type `Any`, mypy will make the inferred type also be `Any`
  - if multiple variants match due to one or more of the arguments being a union, mypy will make the inferred type be the union of the matching variant returns

```python
@overload
def summarize(data: List[int]) -> float:
    ...


@overload
def summarize(data: List[str]) -> str:
    ...


def summarize(data):
    if not data:
        return 0.0
    elif isinstance(data[0], int):
        # Do int specific code
        ...
    else:
        # Do str-specific code
        ...


# What is the type of 'output'? float or str?
output = summarize([])


dynamic_var: Any
output2 = summarize(dynamic_var)
reveal_type(output2)  # output2 is of type 'Any'

some_list: Union[List[int], List[str]]
output3 = summarize(some_list)
reveal_type(output3)  # output3 is of type 'Union[float, str]'
```

```console
$ mypy --pretty --strict ch15/type_checking_calls.py
ch15/type_checking_calls.py:33: note: Revealed type is 'Any'
ch15/type_checking_calls.py:37: note: Revealed type is 'Union[builtins.float, builtins.str]'
```

#### Type checking the variants

- See [`type_checking_variants.py`](ch15/type_checking_variants.py)
- Mypy will perform several checks on your overload variant definitions to ensure they behave as expected
- Mypy will check and make sure that no overload variant is _shadowing_ a subsequent one

```python
class Expression:
    # ...snip...
    ...


class Literal(Expression):
    # ...snip...
    ...


# Warning -- the first overload variant shadows the second!


@overload
def add(left: Expression, right: Expression) -> Expression:
    ...


@overload
def add(left: Literal, right: Literal) -> Literal:
    ...


def add(left: Expression, right: Expression) -> Expression:
    # ...snip...
    ...
```

```console
$ mypy --pretty --strict ch15/type_checking_variants.py
ch15/type_checking_variants.py:25: error: Overloaded function signature 2 will
never be matched: signature 1's parameter type(s) are the same or broader
    def add(left: Literal, right: Literal) -> Literal:
    ^
```

- Mypy will also type check the different variants and flag any overloads that have inherently unsafely overlapping variants
  - mypy will detect and prohibit inherently unsafely overlapping overloads on a _best-effort_ basis
  - 2 variants are considered unsafely overlapping when both of the following are true:
    - all of the arguments of the first variant are compatible with the second
    - the return type of the first variant is not compatible with (e.g. is not a subtype of) the second

```python
@overload
def unsafe_func(x: int) -> int:
    ...


@overload
def unsafe_func(x: object) -> str:
    ...


def unsafe_func(x: object) -> Union[int, str]:
    if isinstance(x, int):
        return 42
    else:
        return "some string"


some_obj: object = 42
x = unsafe_func(some_obj) + " danger danger"  # Type checks, yet crashes at runtime!
reveal_type(x)
```

```console
$ mypy --pretty --strict ch15/type_checking_variants.py
ch15/type_checking_variants.py:35: error: Overloaded function signatures 1 and
2 overlap with incompatible return types
    def unsafe_func(x: int) -> int:
    ^
ch15/type_checking_variants.py:53: note: Revealed type is 'builtins.str'
```

#### Type checking the implementation

- The body of an implementation is type-checked against the type hints provided on the implementation
- If there are no annotations on the implementation, then the body is not type checked
  - if you want to force mypy to check the body anyways, use the `--check-untyped-defs` flag
- The variants must also also be compatible with the implementation type hints

### Advanced uses of self-types

- Normally, mypy doesn't require annotations for the first arguments of instance and class methods
  - they may be needed to have more precise static typing for certain programming patterns

#### Restricted methods in generic classes

- See [`restricted_methods_generic.py`](ch15/restricted_methods_generic.py)
- In generic classes some methods may be allowed to be called only for certain values of type arguments

```python
T = TypeVar("T")


class Tag(Generic[T]):
    item: T

    def uppercase_item(self: Tag[str]) -> str:
        return self.item.upper()


def label(ti: Tag[int], ts: Tag[str]) -> None:
    ti.uppercase_item()  # Error
    ts.uppercase_item()  # This is OK
```

```console
$ mypy --pretty --strict ch15/restricted_methods_generic.py
ch15/restricted_methods_generic.py:16: error: Invalid self argument "Tag[int]"
to attribute function "uppercase_item" with type "Callable[[Tag[str]], str]"
        ti.uppercase_item()  # Error
        ^
```

- This pattern also allows matching on nested types in situations where the type argument is itself generic

```python
T = TypeVar("T")
S = TypeVar("S")


class Storage(Generic[T]):
    def __init__(self, content: T) -> None:
        self.content = content

    def first_chunk(self: Storage[Sequence[S]]) -> S:
        return self.content[0]


page: Storage[List[str]]
page.first_chunk()  # OK, type is "str"
Storage(0).first_chunk()  # Error
```

```console
$ mypy --pretty --strict ch15/restricted_methods_generic.py
ch15/restricted_methods_generic.py:33: error: Invalid self argument
"Storage[int]" to attribute function "first_chunk" with type
"Callable[[Storage[Sequence[S]]], S]"
    Storage(0).first_chunk()  # Error
    ^
```

- Note: mypy 0.770 also reports the following error although it is fine at runtime:

```console
$ mypy --pretty --strict ch15/restricted_methods_generic.py
ch15/restricted_methods_generic.py:32: error: Invalid self argument
"Storage[List[str]]" to attribute function "first_chunk" with type
"Callable[[Storage[Sequence[S]]], S]"
    page.first_chunk()  # OK, type is "str"
    ^
```

- Finally, one can use overloads on self-type to express precise types of some tricky methods

```python
T = TypeVar("T")


class Tag(Generic[T]):

    @overload
    def export(self: Tag[str]) -> str:
        ...

    @overload
    def export(self, converter: Callable[[T], str]) -> str:
        ...

    def export(self, converter=None):
        if isinstance(self.item, str):
            return self.item
        return converter(self.item)
```

#### Mixin classes

- See [`mixin_classes.py`](ch15/mixin_classes.py)
- Using host class protocol as a self-type in mixin methods allows more code re-usability for static typing of mixin classes
- E.g., one can define a protocol that defines common functionality for host classes instead of adding required abstract methods to every mixin
- Note that the explicit self-type is _required_ to be a protocol whenever it is not a supertype of the current class
  - in this case mypy will check the validity of the self-type only at the call site

```python
class Lockable(Protocol):
    @property
    def lock(self) -> Lock:
        ...


class AtomicCloseMixin:
    def atomic_close(self: Lockable) -> int:
        with self.lock:
            # perform actions
            ...


class AtomicOpenMixin:
    def atomic_open(self: Lockable) -> int:
        with self.lock:
            # perform actions
            ...


class File(AtomicCloseMixin, AtomicOpenMixin):
    def __init__(self) -> None:
        self.lock = Lock()


class Bad(AtomicCloseMixin):
    pass


f = File()
b: Bad
f.atomic_close()  # OK
b.atomic_close()  # Error: Invalid self type for "atomic_close"
```

```console
$ mypy --pretty --strict ch15/mixin_classes.py
ch15/mixin_classes.py:38: error: Invalid self argument "Bad" to attribute
function "atomic_close" with type "Callable[[Lockable], int]"
    b.atomic_close()  # Error: Invalid self type for "atomic_close"
    ^
```

#### Precise typing of alternative constructors

- See [`alternative_constructors.py`](ch15/alternative_constructors.py)
- Some classes may define alternative constructors
- If these classes are generic, self-type allows giving them precise signatures

```python
T = TypeVar("T")


class Base(Generic[T]):
    Q = TypeVar("Q", bound="Base[T]")

    def __init__(self, item: T) -> None:
        self.item = item

    @classmethod
    def make_pair(cls: Type[Q], item: T) -> Tuple[Q, Q]:
        return cls(item), cls(item)


class Sub(Base[T]):
    ...


pair = Sub.make_pair("yes")  # Type is "Tuple[Sub[str], Sub[str]]"
reveal_type(pair)
bad = Sub[int].make_pair("no")  # Error
```

```console
$ mypy --pretty --strict ch15/alternative_constructors.py
ch15/alternative_constructors.py:24: note: Revealed type is 'Tuple[alternative_constructors.Sub[builtins.str*], alternative_constructors.Sub[builtins.str*]]'
ch15/alternative_constructors.py:25: error: Argument 1 to "make_pair" of "Base"
has incompatible type "str"; expected "int"
    bad = Sub[int].make_pair("no")  # Error
                             ^
```

### Typing `async`/`await`

- See [`async_await.py`](ch15/async_await.py)
- Mypy supports the ability to type coroutines that use the `async/await` syntax introduced in Python 3.5
- Functions defined using `async def` are typed just like normal functions
  - the return type annotation should be the same as the type of the value you expect to get back when `await`-ing the coroutine
- The result of calling an `async def` function without awaiting will be a value of type `Coroutine[Any, Any, T]`, which is a subtype of `Awaitable[T]`

```python
async def format_string(tag: str, count: int) -> str:
    return "T-minus {} ({})".format(count, tag)


async def countdown_1(tag: str, count: int) -> str:
    while count > 0:
        my_str = await format_string(tag, count)  # has type 'str'
        print(my_str)
        await asyncio.sleep(0.1)
        count -= 1
    return "Blastoff!"


loop = asyncio.get_event_loop()
loop.run_until_complete(countdown_1("Millennium Falcon", 5))
loop.close()

my_coroutine = countdown_1("Millennium Falcon", 5)
reveal_type(my_coroutine)  # has type 'Coroutine[Any, Any, str]'
```

- You may also choose to create a subclass of `Awaitable` instead

```python
class MyAwaitable(Awaitable[str]):
    def __init__(self, tag: str, count: int) -> None:
        self.tag = tag
        self.count = count

    def __await__(self) -> Generator[Any, None, str]:
        for i in range(self.count, 0, -1):
            print("T-minus {} ({})".format(i, self.tag))
            yield from asyncio.sleep(0.1)
        return "Blastoff!"


def countdown_3(tag: str, count: int) -> Awaitable[str]:
    return MyAwaitable(tag, count)


loop3 = asyncio.get_event_loop()
loop3.run_until_complete(countdown_3("Heart of Gold", 5))
loop3.close()
```

- To create an iterable coroutine, subclass `AsyncIterator`

```python
class arange(AsyncIterator[int]):
    def __init__(self, start: int, stop: int, step: int) -> None:
        self.start = start
        self.stop = stop
        self.step = step
        self.count = start - step

    def __aiter__(self) -> AsyncIterator[int]:
        return self

    async def __anext__(self) -> int:
        self.count += self.step
        if self.count == self.stop:
            raise StopAsyncIteration
        else:
            return self.count


async def countdown_4(tag: str, n: int) -> str:
    async for i in arange(n, 0, -1):
        print("T-minus {} ({})".format(i, tag))
        await asyncio.sleep(0.1)
    return "Blastoff!"


loop4 = asyncio.get_event_loop()
loop4.run_until_complete(countdown_4("Serenity", 5))
loop4.close()
```

### `TypedDict`

- See [`typeddict.py`](ch15/typeddict.py)
- You can use a `TypedDict` to give a precise type for objects, where the type of each dictionary value depends on the key

```python
Movie = TypedDict("Movie", {"name": str, "year": int})
movie: Movie = {"name": "Blade Runner", "year": 1982}
```

- Note that we used an explicit type annotation for the `movie` variable
  - without it, mypy will try to infer a regular, uniform `Dict` type for `movie`
- If you pass a `TypedDict` object as an argument to a function, no type annotation is usually necessary since mypy can infer the desired type based on the declared argument type
- If an assignment target has been previously defined, and it has a `TypedDict` type, mypy will treat the assigned value as a `TypedDict`, not `Dict`
- Mypy will detect an invalid key as an error
- Mypy will also reject a runtime-computed expression as a key, as it can't verify that it's a valid key
  - you can only use string literals as `TypedDict` keys

```python
movie_bad: Movie = {"name": "Blade Runner", "year": 1982, "director": "Scott"}
director = movie_bad["director"]
```

```console
$ mypy --pretty --strict ch15/typeddict.py
ch15/typeddict.py:8: error: Extra key 'director' for TypedDict "Movie"
    movie_bad: Movie = {"name": "Blade Runner", "year": 1982, "director": ...
                       ^
ch15/typeddict.py:9: error: TypedDict "Movie" has no key 'director'
    director = movie_bad["director"]
                         ^
```

- The `TypedDict` type object can also act as a constructor
  - returns a normal `dict` object at runtime
  - a `TypedDict` does not define a new runtime type
  - equivalent to just constructing a dictionary directly using `{ ... }` or `dict(key=value, ...)`
  - convenient, since it can be used without a type annotation, and makes the type of the object explicit

```python
toy_story = Movie(name="Toy Story", year=1995)
```

- Like all types, `TypedDict`s can be used as components to build arbitrarily complex types
  - you can define nested `TypedDict`s and containers with `TypedDict` items
  - unlike most other types, mypy uses structural compatibility checking (or structural subtyping) with `TypedDict`s
    - a `TypedDict` object with extra items is compatible with (a subtype of) a narrower `TypedDict`
      - assuming item types are compatible
      - _totality_ also affects subtyping (see below)
- A `TypedDict` object is not a subtype of the regular `Dict[...]` type (and vice versa)
  - `Dict` allows arbitrary keys to be added and removed, unlike `TypedDict`
- Any `TypedDict` object is a subtype of (i.e., compatible with) `Mapping[str, object]`
  - `Mapping` only provides read-only access to the dictionary items

#### Totality

- By default mypy ensures that a `TypedDict` object has all the specified keys

```python
toy_story_2: Movie = {"name": "Toy Story 2"}
```

```console
$ mypy --pretty --strict ch15/typeddict.py
ch15/typeddict.py:13: error: Key 'year' missing for TypedDict "Movie"
    toy_story_2: Movie = {"name": "Toy Story 2"}
                         ^
```

- Sometimes you want to allow keys to be left out when creating a `TypedDict` object
  - provide the `total=False` argument to `TypedDict(...)`

```python
GuiOptions = TypedDict("GuiOptions", {"language": str, "color": str}, total=False)
options: GuiOptions = {}
options["language"] = "en"
```

- You may need to use `get()` to access items of a partial (non-total) `TypedDict`, since indexing using `[]` could fail at runtime

```python
print(options["color"])  # KeyError
print(options.get("color"))  # None
```

- Keys that aren't required are shown with a `?`

```python
reveal_type(options)
```

```console
$ mypy --pretty --strict ch15/typeddict.py
ch15/typeddict.py:22: note: Revealed type is 'TypedDict('typeddict.GuiOptions', {'language'?: builtins.str, 'color'?: builtins.str})'
```

- Totality also affects structural compatibility
  - you can't use a partial `TypedDict` when a total one is expected
  - a total `TypedDict` is not valid when a partial one is expected

#### Supported operations

- `TypedDict` objects support a _subset_ of dictionary operations and methods
  - anything included in `Mapping`:
    - `d[key]`
    - `key in d`
    - `len(d)`
    - `for key in d` (iteration)
    - `d.get(key[, default])`
    - `d.keys()`
    - `d.values()`
    - `d.items()`
  - `d.copy()`
  - `d.setdefault(key, default)`
  - `d1.update(d2)`
  - `d.pop(key[, default])` (partial `TypedDicts` only)
  - `del d[key]` (partial `TypedDicts` only)
- `clear()` and `popitem()` are not supported since they are unsafe
  - they could delete required `TypedDict` items that are not visible to mypy because of structural subtyping

#### Class-based syntax

- An alternative, class-based syntax to define a `TypedDict` is supported in Python 3.6 and later

```python
class MovieClassBased(TypedDict):
    name: str
    year: int
```

- Equivalent to the original `Movie` definition
- Doesn't actually define a real class
- Also supports a form of inheritance
  - subclasses can define additional items
  - primarily a notational shortcut
    - since mypy uses structural compatibility with `TypedDicts`, inheritance is not required for compatibility

```python
class BookBasedMovie(MovieClassBased):
    based_on: str


book_based_movie = BookBasedMovie(
    name="The Social Network", year=2010, based_on="The Accidental Billionaires"
)
print(book_based_movie["name"])
print(book_based_movie.based_on)  # Error
```

#### Mixing required and non-required items

- Inheritance also allows you to mix required and non-required (using `total=False`) items in a single `TypedDict`

```python
class MovieBase(TypedDict):
    name: str
    year: int

class Movie(MovieBase, total=False):
    based_on: str
```

- `based_on` can be left out when constructing an object
- A `TypedDict` with a mix of required and non-required keys will only be compatible with another `TypedDict` if the keys' "required"ness match between the `TypedDict`s

#### Unions of `TypedDict`s

- It is not possible to use `isinstance` checks to distinguish between different variants of a `Union` of `TypedDict` in the same way you can with regular objects
  - `TypedDict`s are really just regular `dict`s at runtime
  - you can use the [tagged union pattern](#tagged-unions) instead

## 16. Literal types

- See [`literal_types.py`](ch16/literal_types.py)
- Literal types let you indicate that an expression is equal to some _specific primitive value_
- Useful when annotating functions that behave differently based on the exact value the caller provides

```python
# The first two overloads use Literal[...] so we can have precise return types.


@overload
def fetch_data(raw: Literal[True]) -> bytes:
    ...


@overload
def fetch_data(raw: Literal[False]) -> str:
    ...


# The last overload is a fallback in case the caller provides a regular bool.


@overload
def fetch_data(raw: bool) -> Union[bytes, str]:
    ...


def fetch_data(raw: bool) -> Union[bytes, str]:
    # Implementation is omitted
    ...


reveal_type(fetch_data(True))  # Revealed type is 'bytes'
reveal_type(fetch_data(False))  # Revealed type is 'str'

# Variables declared without annotations will continue to have an inferred type of
# 'bool'.

variable = True
reveal_type(fetch_data(variable))  # Revealed type is 'Union[bytes, str]'
```

```console
$ mypy --pretty --strict ch16/literal_types.py
ch16/literal_types.py:31: note: Revealed type is 'builtins.bytes'
ch16/literal_types.py:32: note: Revealed type is 'builtins.str'
ch16/literal_types.py:38: note: Revealed type is 'Union[builtins.bytes, builtins.str]'
```

### Parameterizing Literals

- See [`parameterizing_literals.py`](ch16/parameterizing_literals.py)
- May contain one or more literal `bool`s, `int`s, `str`s, `bytes`, and `enum` values
- Cannot contain arbitrary expressions
  - types like `Literal[my_string.trim()]`, `Literal[x > 3]`, or `Literal[3j + 4]` are all illegal
- Literals containing two or more values are equivalent to the union of those values
  - `Literal[-3, b"foo", MyEnum.A]` is equivalent to `Union[Literal[-3], Literal[b"foo"], Literal[MyEnum.A]]`
- May contain `None`
  - equivalent to just `None`
  - `Literal[4, None]`, `Union[Literal[4], None]`, and `Optional[Literal[4]]` are all equivalent
- May also contain aliases to other literal types
- May not contain any other kind of type or expression
  - `Literal[my_instance]`, `Literal[Any]`, `Literal[3.14]`, or `Literal[{"foo": 2, "bar": 5}]` are all illegal

```python
PrimaryColors = Literal["red", "blue", "yellow"]
SecondaryColors = Literal["purple", "green", "orange"]
AllowedColors = Literal[PrimaryColors, SecondaryColors]


def paint(color: AllowedColors) -> None:
    ...


paint("red")  # Type checks!
paint("turquoise")  # Does not type check
```

```console
$ mypy --pretty --strict ch16/parameterizing_literals.py
ch16/parameterizing_literals.py:15: error: Argument 1 to "paint" has
incompatible type "Literal['turquoise']"; expected
"Union[Literal['red'], Literal['blue'], Literal['yellow'], Literal['purple'], Literal['green'], Literal['orange']]"
    paint("turquoise")  # Does not type check
          ^
```

### Declaring literal variables

- See [`literal_vars.py`](ch16/literal_vars.py)
- You must explicitly add an annotation to a variable to declare that it has a literal type

```python
a: Literal[19] = 19
reveal_type(a)  # Revealed type is 'Literal[19]'
```

- You can instead change the variable to be `Final`
  - see [Final names, methods and classes](#17-final-names-methods-and-classes)

```python
def expects_literal(x: Literal[19]) -> None:
    pass


c: Final = 19

reveal_type(c)  # Revealed type is 'Literal[19]?'
expects_literal(c)  # ...and this type checks!
```

```console
$ mypy --pretty --strict ch16/literal_vars.py
ch16/literal_vars.py:12: note: Revealed type is 'Literal[19]?'
```

- If you do not provide an explicit type in the `Final`, the type of `c` becomes context-sensitive
  - mypy will basically try "substituting" the original assigned value whenever it's used before performing type checking
  - `Literal[19]?`: the question mark at the end reflects this context-sensitive nature
- The main cases where the behavior of context-sensitive vs true literal types differ are when you try using those types in places that are not explicitly expecting a `Literal[...]`

```python
a: Final = 19

# Mypy will infer List[int] here.
list_of_ints = []
list_of_ints.append(a)
reveal_type(list_of_ints)  # Revealed type is 'List[int]'

b: Literal[19] = 19

# mypy # will infer List[Literal[19]].
list_of_lits = []
list_of_lits.append(b)
reveal_type(list_of_lits)  # Revealed type is 'List[Literal[19]]'
```

```console
$ mypy --pretty --strict ch16/literal_vars.py
ch16/literal_vars.py:21: note: Revealed type is 'builtins.list[builtins.int]'
ch16/literal_vars.py:28: note: Revealed type is 'builtins.list[Literal[19]]'
```

### Intelligent indexing

- See [`intelligent_indexing.py`](ch16/intelligent_indexing.py)
- We can use `Literal` types to more precisely index into structured heterogeneous types such as tuples, `NamedTuple`s, and `TypedDict`s
  - intelligent indexing
  - e.g., when we index into a tuple using some `int`, the inferred type is normally the union of the tuple item types
    - if we want just the type corresponding to some particular index, we can use `Literal` types

```python
tup = ("foo", 3.4)

# Indexing with an int literal gives us the exact type for that index
reveal_type(tup[0])  # Revealed type is 'str'

# If the index to be a variable, normally mypy won't # know exactly what the index is
# and so will return a less precise type:
int_index = 1
reveal_type(tup[int_index])  # Revealed type is 'Union[str, float]'

# But if we use either Literal types or a Final int, we can gain back # the precision
# we originally had:
lit_index: Literal[1] = 1
fin_index: Final = 1
reveal_type(tup[lit_index])  # Revealed type is 'float'
reveal_type(tup[fin_index])  # Revealed type is 'float'

# We can do the same thing with with TypedDict and str keys:
class MyDict(TypedDict):
    name: str
    main_id: int
    backup_id: int


d: MyDict = {"name": "Saanvi", "main_id": 111, "backup_id": 222}

name_var = "name"
reveal_type(d[name_var])  # Error
reveal_type(d.get(name_var))  # Revealed type is 'object*'

name_key: Final = "name"
reveal_type(d[name_key])  # Revealed type is 'str'
reveal_type(d.get(name_key))  # Revealed type is 'Union[str, None]'

# You can also index using unions of literals
id_key: Literal["main_id", "backup_id"]
reveal_type(d[id_key])  # Revealed type is 'int'
```

```console
$ mypy --pretty --strict ch16/intelligent_indexing.py
ch16/intelligent_indexing.py:8: note: Revealed type is 'builtins.str'
ch16/intelligent_indexing.py:13: note: Revealed type is 'Union[builtins.str, builtins.float]'
ch16/intelligent_indexing.py:19: note: Revealed type is 'builtins.float'
ch16/intelligent_indexing.py:20: note: Revealed type is 'builtins.float'
ch16/intelligent_indexing.py:32: note: Revealed type is 'Any'
ch16/intelligent_indexing.py:32: error: TypedDict key must be a string literal;
expected one of ('name', 'main_id', 'backup_id')
    reveal_type(d[name_var])  # Error
                  ^
ch16/intelligent_indexing.py:33: note: Revealed type is 'builtins.object*'
ch16/intelligent_indexing.py:36: note: Revealed type is 'builtins.str'
ch16/intelligent_indexing.py:37: note: Revealed type is 'Union[builtins.str, None]'
ch16/intelligent_indexing.py:41: note: Revealed type is 'builtins.int'
```

### Tagged unions

- See [`tagged_unions.py`](ch16/tagged_unions.py)
- When you have a union of types, you can normally discriminate between each type in the union by using `isinstance` checks
  - e.g., if you had a variable `x` of type `Union[int, str]`, you could write some code that runs only if `x` is an `int` by doing `if isinstance(x, int): ....`
- It is not always possible or convenient to do this
  - e.g., it is not possible to use `isinstance` to distinguish between two different `TypedDict`s since at runtime, your variable will simply be just a `dict`
  - you can _label_ or _tag_ your `TypedDict`s with a distinct `Literal` type
    - you can then discriminate between each kind of `TypedDict` by checking the label
  - you can also use the same technique wih regular objects, tuples, or namedtuples

```python
class NewJobEvent(TypedDict):
    tag: Literal["new-job"]
    job_name: str
    config_file_path: str


class CancelJobEvent(TypedDict):
    tag: Literal["cancel-job"]
    job_id: int


Event = Union[NewJobEvent, CancelJobEvent]


def process_event(event: Event) -> None:
    # Since we made sure both TypedDicts have a key named 'tag', it's safe to do
    # 'event["tag"]'. This expression normally has the type Literal["new-job",
    # "cancel-job"], but the check below will narrow the type to either
    # Literal["new-job"] or Literal["cancel-job"].
    #
    # This in turns narrows the type of 'event' to either NewJobEvent or CancelJobEvent.
    if event["tag"] == "new-job":
        print(event["job_name"])
    else:
        print(event["job_id"])
```

- Tags do not need to be specifically `str` `Literal`s
  - they can be any type you can normally narrow within `if` statements and the like
  - e.g., you could have your tags be `int` or `Enum` `Literal`s or even regular classes you narrow using `isinstance()`
  - this feature is sometimes called "sum types" or "discriminated union types" in other programming languages

```python
T = TypeVar("T")


class Wrapper(Generic[T]):
    def __init__(self, inner: T) -> None:
        self.inner = inner


def process(w: Union[Wrapper[int], Wrapper[str]]) -> None:
    # Doing `if isinstance(w, Wrapper[int])` does not work: isinstance requires that
    # the second argument always be an *erased* type, with no generics. This is because
    # generics are a typing-only concept and do not exist at runtime in a way
    # `isinstance` can always check.
    #
    # However, we can side-step this by checking the type of `w.inner` to narrow `w`
    # itself:
    if isinstance(w.inner, int):
        reveal_type(w)  # Revealed type is 'Wrapper[int]'
    else:
        reveal_type(w)  # Revealed type is 'Wrapper[str]'
```

```console
$ mypy --pretty --strict ch16/tagged_unions.py
ch16/tagged_unions.py:50: note: Revealed type is 'tagged_unions.Wrapper[builtins.int]'
ch16/tagged_unions.py:52: note: Revealed type is 'tagged_unions.Wrapper[builtins.str]'
```

### Limitations

- Mypy will not understand expressions that use variables of type `Literal[..]` on a deep level
  - e.g., if you have a variable `a` of type `Literal[3]` and another variable `b` of type `Literal[5]`, mypy will infer that `a + b` has type `int`, not type `Literal[8]`
- The basic rule is that literal types are treated as just regular subtypes of whatever type the parameter has
  - e.g., `Literal[3]` is treated as a subtype of `int` and so will inherit all of `int`'s methods directly
    - this means that `Literal[3].__add__` accepts the same arguments and has the same return type as `int.__add__`

## Sources

- "Welcome to Mypy Documentation!" _Mypy Documentation_, [mypy.readthedocs.io/en/stable/index.html](https://mypy.readthedocs.io/en/stable/index.html).
- van Rossum, Guido, and Ivan Levkivskyi. "PEP 483 -- The Theory of Type Hints." _Python.org_, 19 Dec. 2014, [www.python.org/dev/peps/pep-0483/](https://www.python.org/dev/peps/pep-0483/).
