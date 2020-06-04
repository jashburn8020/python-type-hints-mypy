"""Type checking calls to overloads."""

from typing import Any, List, Union, overload


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
