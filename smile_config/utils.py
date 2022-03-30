#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""
Python ♡ Nasy.

    |             *         *
    |                  .                .
    |           .                              登
    |     *                      ,
    |                   .                      至
    |
    |                               *          恖
    |          |\___/|
    |          )    -(             .           聖 ·
    |         =\ -   /=
    |           )===(       *
    |          /   - \
    |          |-    |
    |         /   -   \     0.|.0
    |  NASY___\__( (__/_____(\=/)__+1s____________
    |  ______|____) )______|______|______|______|_
    |  ___|______( (____|______|______|______|____
    |  ______|____\_|______|______|______|______|_
    |  ___|______|______|______|______|______|____
    |  ______|______|______|______|______|______|_
    |  ___|______|______|______|______|______|____

author   : Nasy https://nasy.moe
date     : Feb  1, 2022
email    : Nasy <nasyxx+python@gmail.com>
filename : utils.py
project  : smile_config
license  : GPL-3.0+

smile config utils
"""
# Standard Library
import inspect
from collections import defaultdict
from itertools import chain
from os import PathLike

# Types
from typing import Any, Callable, Generator, Iterable, Mapping, Type, TypeVar, Union
from typing_extensions import Protocol

# Others
from tomlkit import TOMLDocument, dump, dumps, parse

A = TypeVar("A")
B = TypeVar("B")
DD = defaultdict[str, Any]


class DC(Protocol):
    """Dataclass typing."""

    __dataclass_fields__: dict


def load_config(path: Union[str, PathLike[str]]) -> TOMLDocument:
    """Load config file."""
    with open(path) as f:
        return parse(f.read())


def save_config(config: Mapping, path: Union[str, PathLike[str]]) -> Mapping:
    """Save config file."""
    with open(path, "w") as f:
        dump(config, f)
    return config


def add_prefix(x: str, p: str) -> str:
    """Add prefix P to X."""
    xs = x.split("-")
    return p and "-".join(chain(xs[:-1], (f"{p}.{xs[-1]}",))) or x


def _config_dict_init() -> DD:
    return defaultdict(_config_dict_init)


def _config_insert(d: DD, key: str, value: Any, nested: bool = True) -> DD:
    if nested:
        d[key] = value
    keys = key.split(".")
    for subkey in keys[:-1]:
        d = d[subkey]
    d[keys[-1]] = value
    return d


def config_dict(d: dict, nested: bool = True) -> DD:
    """Get config dictional from config D."""
    r = _config_dict_init()
    for k, v in d.items():
        _config_insert(r, k, v, nested)
    return r


def scanl(
    func: Callable[[B, A], B], xs: Iterable[A], init: B
) -> Generator[B, None, None]:
    """Simular to foldl but keep result."""
    for x in xs:
        init = func(init, x)
        yield init


def from_dict(cls: Type[A], data: dict[str, Any]) -> A:
    """From dict to dataclass."""
    d: dict[str, Any] = {}
    for key, value in data.items():
        dt = d
        levels = key.split(".")
        for level in levels[:-1]:
            dt = dt.setdefault(level, {})
        dt[levels[-1]] = value

    return cls(
        **dict(
            map(
                lambda kv: (
                    lambda k, v: (k in d)
                    and (
                        isinstance(d[k], dict)
                        and (k, from_dict(v.default.__class__, d[k]))
                    )
                    or (k, d.get(k, v.default))
                )(kv[0], kv[1]),
                inspect.signature(cls).parameters.items(),
            )
        )
    )
