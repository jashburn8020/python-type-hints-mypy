"""Tagged unions."""

from typing import Literal, TypedDict, Union, TypeVar, Generic


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
