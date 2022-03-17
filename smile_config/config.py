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

Conifg.py
"""
from __future__ import annotations

# Standard Library
from argparse import ArgumentParser, _ArgumentGroup  # noqa: WPS450
from dataclasses import asdict

# Types
from typing import Any, Generator, MutableMapping, Optional, Type, Union

# Local
from .utils import DC, add_prefix, from_dict


def _iter_config(
    d: dict[str, Any], prefix: str = ""
) -> Generator[tuple[str, Any], None, None]:
    for k, v in d.items():
        if isinstance(v, dict):
            yield from _iter_config(v, prefix=f"{prefix}{k}.")
        else:
            yield f"{prefix}{k}", v


class ConfigDict(MutableMapping):
    """Config dictionary."""

    def __init__(self, d: MutableMapping[str, Any]) -> None:
        """Initialize."""
        self.__data = {}  # type: dict[str, Any]
        for k, v in d.items():
            self[k] = v

    def get(self, key: str, default: Any = None) -> Any:
        """Get VALUE from KEY."""
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def __setitem__(self, key: str, value: Any) -> None:
        """Set VALUE to data with KEY."""
        keys = key.split(".")
        d = self.__data
        for subkey in keys[:-1]:
            d = d.setdefault(subkey, {})
        d[keys[-1]] = value

    def __getitem__(self, key: str) -> Any:
        """Get VALUE from KEY."""
        keys = key.split(".")
        r = self.__data
        for subkey in keys:
            r = r[subkey]
        return r

    def __getattr__(self, name: str) -> Any:
        """Get attr VALUE from NAME."""
        try:
            res = self[name]
        except KeyError:
            res = object.__getattribute__(self, name)
        if isinstance(res, dict):
            return ConfigDict(res)
        return res

    def __setstate__(self, state: dict):
        """Restore state."""
        data = state.pop("_ConfigDict__data")
        self.__dict__.update(state)
        self.__data = data

    def __iter__(self) -> Generator[tuple[str, Any], None, None]:
        """Generate config items."""
        yield from self.__data.items()

    def deep_iter(self) -> Generator[tuple[str, Any], None, None]:
        """Deep iter config."""
        yield from _iter_config(self.__data)

    def __len__(self) -> int:
        """Get length of config items."""
        return len(self.__data)

    def __delitem__(self, __v: Any) -> None:
        """Del config item."""
        return self.__data.__delitem__(__v)

    def __repr__(self) -> str:
        """Repr config item."""
        return repr(self.__data)

    def __dir__(self) -> list[str]:
        """Dir self."""
        return list(map(lambda x: x[0], self.deep_iter()))


class Option:
    """Smile Config Arguments."""

    def __init__(self, *args, **kwds) -> None:
        """Initialize."""
        self.args = args
        self.kwds = kwds

    def __repr__(self) -> str:
        """Repr options."""
        args = ", ".join(self.args)
        kwds = ", ".join(
            map(
                lambda x: "=".join(
                    map(lambda s: "'" in str(s) and str(s) or repr(s), x)
                ),
                self.kwds.items(),
            )
        )
        return f"Option({args and f'{args}, *, ' or ''}{kwds}"


class Config:
    """Smile config."""

    def __init__(
        self,
        help_: Union[Option, str] = "Smile Config help info.",
        *options: Union[Option, SConfig],
        dcls: Optional[Type[DC]] = None,
    ) -> None:
        """Initialize."""
        if isinstance(help_, str):
            self.help = Option(description=help_)
        else:
            self.help = help_
        self.options = options
        config = vars(self.build().parse_args())
        if dcls is not None:
            self.config = from_dict(dcls, config)
        else:
            self.config = ConfigDict(config)

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
        if name == "config":
            return super().__getattribute__(name)  # noqa: WPS613
        if name in asdict(self.config).keys():
            return getattr(self.config, name)
        return super().__getattribute__(name)  # noqa: WPS613

    def __repr__(self) -> str:
        """Repr str."""
        if "config" in self.__dict__:
            return str(self.config)
        return str(vars(self))

    def __dir__(self) -> list[str]:
        """Dir self."""
        return dir(self.config)


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
