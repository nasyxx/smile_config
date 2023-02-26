# config.py
from typing import Annotated
from dataclasses import dataclass, asdict, field
from smile_config import from_dataclass

@dataclass
class Train:
    """Train config."""

    batch_size: int = 64


@dataclass
class ML:
    lr: Annotated[float, dict(help="learning rate", type=float)] = 0.001
    train: Train = Train()
    cc: list[int] = field(default_factory=lambda: [10])


@dataclass
class Example:
    """Example config."""

    ml: ML = ML()
    x: bool = True
    a: int | None = None

config = from_dataclass(Example()).config

print(config)

# If autocomplete is not working, try to add the following line to your config file:
from typing import cast
config = cast(Example, config)
