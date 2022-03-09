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
date     : Mar  8, 2022
email    : Nasy <nasyxx+python@gmail.com>
filename : command.py
project  : smile_config
license  : GPL-3.0+

build
"""
from __future__ import annotations

# Standard Library
from dataclasses import _MISSING_TYPE, Field, asdict, dataclass, is_dataclass

# Types
from typing import Any, Generator, Optional, Type, TypeVar, Union, get_type_hints

# Others
from typing_extensions import Protocol

# Local
from .config import Config, Option, SConfig

A = TypeVar("A")
B = TypeVar("B")


class DC(Protocol):
    """Dataclass protocol."""

    __dataclass_fields__: dict


def from_dataclass(config: DC, ns: Optional[dict[str, Any]] = None) -> Config:
    """Build config from dataclass."""
    if not is_dataclass(config):
        raise TypeError("config must be a dataclass.")
    return Config(
        config.__doc__ or type(config).__name__,
        *_build_options(config, ns),
    )


def _build_option(x: str, dc: DC, ns: Optional[dict[str, Any]] = None) -> Option:
    return Option(
        f"--{x}", default=getattr(dc, x), type=get_type_hints(dc, globalns=ns)[x]
    )


def _build_sconfig(x: str, dc: DC, ns: Optional[dict[str, Any]] = None) -> SConfig:
    if not is_dataclass(dc):
        raise TypeError("dc must be a dataclass.")
    return SConfig(x, None, *_build_options(getattr(dc, x), ns))


def _build_options(
    dc: DC, ns: Optional[dict[str, Any]] = None
) -> Generator[Union[SConfig, Option], None, None]:
    for x in dc.__dataclass_fields__:
        if is_dataclass(x):
            yield _build_sconfig(x, dc, ns)
        else:
            yield _build_option(x, dc, ns)
