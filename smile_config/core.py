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
filename : config.py
project  : smile_config
license  : GPL-3.0+

Config.py
"""

from __future__ import annotations

# Standard Library
import json
from argparse import ArgumentParser, _ArgumentGroup  # noqa: WPS450

# Types
from typing import Any, Optional, Union

# Local
from .utils import add_prefix, config_dict


class Option:
    """Smile Config Arguments."""

    def __init__(self, *args, **kwds) -> None:
        """Initialize."""
        self.args = args
        self.kwds = kwds


class Config:
    """Smile config."""

    def __init__(
        self,
        help_: Union[Option, str] = "Smile Config help info.",
        *options: Union[Option, SConfig],
    ) -> None:
        """Initialize."""
        if isinstance(help_, str):
            self.help = Option(description=help_)
        else:
            self.help = help_
        self.options = options
        self.config = vars(self.build().parse_args())

    def build(self):
        """Post initialize."""
        return build_commands(
            ArgumentParser(*self.help.args, **self.help.kwds),
            None,
            "",
            *self.options,
        )

    def __getattr__(self, name: str) -> Any:
        """Get attr from config."""
        try:
            return config_dict(self.config)[name]
        except AttributeError:
            return object.__getattribute__(self, name)  # noqa: WPS609

    def __repr__(self) -> str:
        """Repr str."""
        return str(json.loads(json.dumps(config_dict(self.config, nested=False))))


class SConfig(Config):
    """Smile sub config."""

    def __init__(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        *options: Union[Option, SConfig],
    ):
        """Initialize."""
        self.title = title
        self.desc = description
        self.options = options

    def build(self):
        """Build config."""
        raise NotImplementedError()


def build_commands(
    parser: ArgumentParser,
    group: Optional[_ArgumentGroup] = None,
    prefix: str = "",
    *args: Union[Option, SConfig],
) -> ArgumentParser:
    """Build commands."""
    for arg in args:
        if isinstance(arg, Option):
            if group is None:
                parser.add_argument(*arg.args, **arg.kwds)
            else:
                if len(arg.args) == 1 and "dest" in arg.kwds:
                    raise ValueError("dest supplied twice for positional argument")
                group.add_argument(
                    *map(lambda x: add_prefix(x, prefix), arg.args),
                    **arg.kwds,
                )
        elif isinstance(arg, SConfig):
            title = arg.title
            if title is not None:
                title = prefix and ".".join((prefix, title)) or title
            desc = arg.desc
            ngroup = parser.add_argument_group(title, desc)
            build_commands(parser, ngroup, title or prefix, *arg.options)
        else:
            raise TypeError(f"Unknown type of {type(arg)}")

    return parser
