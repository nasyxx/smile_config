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
from argparse import ArgumentDefaultsHelpFormatter
from dataclasses import is_dataclass

# Types
from typing import Any, Generator, Optional, TypeVar, Union, get_type_hints
from typing_extensions import _AnnotatedAlias  # noqa: WPS450

# Local
from .config import Config, Option, SConfig
from .utils import DC

A = TypeVar("A")
B = TypeVar("B")


def from_dataclass(config: DC, ns: Optional[dict[str, Any]] = None) -> Config:
    """Build config from dataclass."""
    if not is_dataclass(config):
        raise TypeError("config must be a dataclass.")
    return Config(
        Option(
            description=config.__doc__ or type(config).__name__,
            formatter_class=ArgumentDefaultsHelpFormatter,
        ),
        *_build_options(config, ns),
        dcls=config.__class__,
    )


def _build_option(x: str, dc: DC, ns: Optional[dict[str, Any]] = None) -> Option:
    typ = get_type_hints(dc, globalns=ns, include_extras=True)[x]
    helps = "-"
    if isinstance(typ, _AnnotatedAlias):
        helps = typ.__metadata__[0]
        typ = get_type_hints(dc, globalns=ns, include_extras=True)[x]
    return Option(f"--{x}", default=getattr(dc, x), type=typ, help=helps)


def _build_sconfig(x: str, dc: DC, ns: Optional[dict[str, Any]] = None) -> SConfig:
    if not is_dataclass(dc):
        raise TypeError("dc must be a dataclass.")
    return SConfig(x, None, *_build_options(getattr(dc, x), ns))


def _build_options(
    dc: DC, ns: Optional[dict[str, Any]] = None
) -> Generator[Union[SConfig, Option], None, None]:
    for x in dc.__dataclass_fields__:
        if is_dataclass(getattr(dc, x)):
            yield _build_sconfig(x, dc, ns)
        else:
            yield _build_option(x, dc, ns)
