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
from .config import Option, Config, SConfig
from typing import Union


def ml_basic(*extra_options: Union[Option, SConfig]) -> Config:
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


if __name__ == "__main__":
    print(ml_basic())
