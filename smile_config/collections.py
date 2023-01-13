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
filename : collections.py
project  : smile_config
license  : GPL-3.0+

Smile config collections.
"""
from __future__ import annotations

# Standard Library
from dataclasses import dataclass, field

# Types
from typing import Annotated

# Local
from .build import from_dataclass
from .config import Config, Option, SConfig


def ml_basic(*extra_options: Option | SConfig) -> Config:
    """Machine learning basic options."""
    return Config(
        "Smile machine learning basic options.",
        Option(
            "--lr",
            "-lr",
            "--learning_rate",
            type=float,
            default=1e-3,
            help="Learning rate.",
        ),
        SConfig(
            "train",
            None,
            SConfig("path", None, Option("--p1", type=str, default="train1.csv")),
        ),
        *extra_options,
    )


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
class A:
    a: int = 1


@dataclass
class B:
    a: A = A()


@dataclass
class C:
    a: A = A()
    b: B = B()
    c: int = 0
    _d: int = 1


@dataclass
class Example:
    """Example config."""

    ml: ML = ML()
    x: bool = True
    a: int | None = None
    c: C = C()


if __name__ == "__main__":
    eg = from_dataclass(Example(), ns=globals())
    print(eg.config)
