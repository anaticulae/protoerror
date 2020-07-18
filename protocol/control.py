# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import enum
import re


class Generator(enum.Enum):
    BASE = enum.auto()
    LATEX = enum.auto()
    MSWORD = enum.auto()


def render_template(content: str, generator: Generator) -> str:

    def start(name: str):
        return r'\{\%' + name + r'\%\}(\n){0,1}'

    def end(name: str):
        return r'\{\%' + name + r'_END\%\}(\n){0,1}'

    def remove(content, selected: str):
        pattern = start(selected)
        pattern += r'.+'
        pattern += end(selected)
        replaced = re.sub(pattern, '', content, flags=re.DOTALL)
        return replaced

    content = re.sub(start(generator.name), r'', content)
    content = re.sub(end(generator.name), '', content)

    for item in Generator:
        if item == generator:
            continue
        content = remove(content, item.name)
    return content
