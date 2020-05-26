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
  - [Sources](#sources)

## 1. Introduction

- Mypy is a static type checker for Python 3 and Python 2.7
- Type annotations are just hints for mypy and don't interfere when running your program
- You can annotate your code using the Python 3 function annotation syntax (using the [PEP 484](https://www.python.org/dev/peps/pep-0484) notation) or a comment-based annotation syntax for Python 2 code

## 2. Getting started

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
  - note that even though they are similar to abstract base classes defined in [`collections.abc`](https://docs.python.org/3/library/collections.abc.html#module-collections.abc) (Python 3.8), they are not identical
    - the built-in collection type objects do not support indexing

## 5. Type inference and type annotations

- See [`type_inference_type_annotations.py`](ch05/type_inference_type_annotations.py)

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

- You can override the inferred type of a variable by using a **variable type annotation**
- Mypy checks that the type of the initializer is compatible with the declared type

```python
invalid_initializer: Union[int, str] = 1.1  # Error!
```

```console
$ mypy --pretty --strict ch05/type_inference_type_annotations.py
ch05/type_inference_type_annotations.py:4: error: Incompatible types in
assignment (expression has type "float", variable has type "Union[int, str]")
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

- The type checker cannot always infer the type of a list or a dictionary
  - often arises when creating an empty list or dictionary
  - give the type explicitly using a type annotation

```python
empty_list: List[int] = []
empty_dict: Dict[str, int] = {}
empty_set: Set[int] = set()
```

### Compatibility of container types

- The following program generates a mypy error since `List[int]` is not compatible with `List[object]`:
  - allowing the assignment could result in non-`int` values stored in a list of `int`

```python
def incompatible_lists(object_list: List[object], int_list: List[int]) -> None:
    """Incompatible container types."""
    object_list = int_list
```

```console
$ mypy --pretty --strict ch05/type_inference_type_annotations.py
ch05/type_inference_type_annotations.py:20: error: Incompatible types in
assignment (expression has type "List[int]", variable has type "List[object]")
        object_list = int_list
                      ^
ch05/type_inference_type_annotations.py:20: note: "List" is invariant -- see http://mypy.readthedocs.io/en/latest/common_issues.html#variance
ch05/type_inference_type_annotations.py:20: note: Consider using "Sequence" instead, which is covariant
```

- Other container types like `Dict` and `Set` behave similarly

### Context in type inference

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

- You can declare more than a single variable at a time, but only with a type comment

```python
multiple_vars_int, multiple_vars_bool = 0, False  # type: int, bool
```

### Starred expressions

- Mypy can infer the type of starred expressions from the right-hand side of an assignment, but not always:

```python
int_1, *ints_a = 1, 2, 3  # OK
int_2, int_3, *ints_b = 1, 2  # Error: Type of ints_b cannot be inferred
```

```console
$ mypy --pretty --strict ch05/type_inference_type_annotations.py
ch05/type_inference_type_annotations.py:40: error: Need type annotation for
'ints_b' (hint: "ints_b: List[<type>] = ...")
    int_2, int_3, *ints_b = 1, 2  # Error: Type of ints_b cannot be inferr...
                   ^
```

- Mypy cannot infer the type of `ints_b`, because there is no right-hand side value for `ints_b` to infer the type from

## 6. Kinds of types

- See [`kinds_of_types.py`](ch06/kinds_of_types.py)

### Class types

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
$ mypy --pretty --strict ch06/kinds_of_types.py
ch06/kinds_of_types.py:16: error: "SuperClass" has no attribute "method_b";
maybe "method_a"?
        clazz.method_b()  # Error: "SuperClass" has no attribute "method_b"
        ^
```

### The `Any` type

- A value with the `Any` type is dynamically typed
- `Any` is compatible with every other type, and vice versa
- If you do not define a function return value or argument types, these default to `Any`

### `Tuple` types

```python
def tuple_type(some_tuple: Tuple[int, str]) -> None:
    """Fixed-length tuple."""
    some_tuple = 1, "foo"  # OK
    some_tuple = "foo", 1  # Type check error
```

```console
$ mypy --pretty --strict ch06/kinds_of_types.py
ch06/kinds_of_types.py:28: error: Incompatible types in assignment (expression
has type "Tuple[str, int]", variable has type "Tuple[int, str]")
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
$ mypy --pretty --strict ch06/kinds_of_types.py
ch06/kinds_of_types.py:39: error: Argument 1 to "var_length_tuple" has
incompatible type "List[int]"; expected "Tuple[int, ...]"
    var_length_tuple([1, 2])  # Error: only a tuple is valid
                     ^
```

- Note: Usually it's a better idea to use `Sequence[T]` instead of `Tuple[T, ...]`, as `Sequence` is also compatible with lists and other non-tuple sequences

### `Callable` types (and lambdas)

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
$ mypy --pretty --strict ch06/kinds_of_types.py
ch06/kinds_of_types.py:60: error: Argument 1 to "arbitrary_call" has
incompatible type
"Callable[[Union[str, bytes, int, _PathLike[Any]], str, int, Optional[str], Optional[str], Optional[str], bool, Optional[Callable[[str, int], int]]], IO[Any]]";
expected "Callable[..., int]"
    arbitrary_call(open)  # Error: does not return an int
                   ^
ch06/kinds_of_types.py:61: error: Argument 1 to "arbitrary_call" has
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
$ mypy --pretty --strict ch06/kinds_of_types.py
ch06/kinds_of_types.py:69: error: Unsupported operand types for + ("str" and
"int")
        print(arg + 1)  # Error: str + int is not valid
                    ^
ch06/kinds_of_types.py:69: note: Left operand is of type "Union[int, str]"
ch06/kinds_of_types.py:78: error: Argument 1 to "union_type" has incompatible
type "float"; expected "Union[int, str]"
    union_type(1.1)  # Error
               ^
```

### `Optional` types and the `None` type

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
$ mypy --pretty --strict ch06/kinds_of_types.py
ch06/kinds_of_types.py:100: error: Argument 1 to "open" has incompatible type
"Optional[str]"; expected "Union[str, bytes, int, _PathLike[Any]]"
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

- Python does not allow references to a class object before the class is defined
  - you can enter the type as a string literal - this is a _forward reference_
  - string literal types must be defined (or imported) later in the _same module_

```python
def no_forward_reference(clazz: SomeClass) -> None:
    """Python does not allow references to a class object before the class is defined.
    """
    pass


def forward_reference(clazz: "SomeClass") -> None:
    """Enter the type as a string literal - forward reference."""
    pass


class SomeClass:
    """Class defined after references."""

    pass
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
$ mypy --pretty --strict ch06/kinds_of_types.py
ch06/kinds_of_types.py:146: error: Argument "y" to "TypedPoint" has
incompatible type "str"; expected "int"
    typed_point = TypedPoint(x=1, y="two")
                                    ^
ch06/kinds_of_types.py:157: error: Argument "y" to "ClassBasedPoint" has
incompatible type "str"; expected "int"
    class_based_point = ClassBasedPoint(x=1, y="two")
                                               ^
```

### The type of class objects

- Note: **`Type`** is introduced in Python 3.8
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

### `Text` and `AnyStr`

- Note: **`Text`** and **`AnyStr`** are introduced in Python 3.8
- You may want to write a function which will accept only unicode strings
  - challenging to do in a codebase intended to run in both Python 2 and Python 3
    - `str` means something different in both versions
    - `unicode` is not a keyword in Python 3
- Use `Text`, which is aliased to
  - `unicode` in Python 2
  - `str` in Python 3
- Use **`AnyStr`**
  - to write a function that will work with any kind of string but will not let you mix two different string types

### Generators

- Note: Type hints for generators are mostly introduced in Python 3.8
  - see <https://mypy.readthedocs.io/en/stable/kinds_of_types.html#generators>

## Sources

- "Welcome to Mypy Documentation!" _Mypy Documentation_, mypy.readthedocs.io/en/stable/index.html.
