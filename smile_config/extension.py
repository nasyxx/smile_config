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
date     : Dec 17, 2022
email    : Nasy <nasyxx+python@gmail.com>
filename : extension.py
project  : smile_config
license  : GPL-3.0+

Extension
"""

# Types
from typing import Any, Mapping

# Others
from tomlkit import TOMLDocument, dump, parse

# Local
from .utils import UP


def load_config(path: UP) -> TOMLDocument:
    """Load config file."""
    with open(path) as f:
        return parse(f.read())


def save_config(config: Mapping[str, Any], path: UP) -> Mapping[str, Any]:
    """Save config file."""
    with open(path, "w") as f:
        dump(config, f)
    return config
