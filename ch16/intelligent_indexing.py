"""Intelligent indexing."""

from typing import Final, Literal, TypedDict

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
