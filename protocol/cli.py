# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import sys

import serializeraw
import utila

import protocol


@utila.saveme
def main():
    inpath, outpath, pages, action = evaluate()
    for path in inpath:
        if not utila.exists(path):
            utila.error(f'input does not exists: {path}')
            return utila.FAILURE
    if not utila.exists(outpath):
        utila.error(f'output does not exists: {outpath}')
        return utila.FAILURE
    if action == 'optimize':
        optimize(srcs=inpath, dest=outpath, pages=pages)
        return utila.SUCCESS
    return utila.INVALID_COMMAND


def optimize(srcs: str, dest: str, pages: tuple = None, msgid: set = None):
    findings = []
    for src in srcs:
        utila.log(f'load findings from: {src}', preserve_newlines=False)
    findings = serializeraw.findings_from_path(
        path=srcs,
        msgid=msgid,
        pages=pages,
    )
    findings = utila.flatten_content(findings)
    dest = os.path.join(dest, '__optimized__')
    os.makedirs(dest, exist_ok=True)
    utila.log(
        f'write optimized findings to: {dest}',
        preserve_newlines=False,
    )
    serializeraw.write_grouped(findings, dest=dest)


def evaluate() -> tuple:
    parser = utila.cli.create_parser(
        todo=[
            utila.cli.Flag(
                longcut='optimize',
                message='read findings and write to page dependent structure',
            ),
        ],
        config=utila.ParserConfiguration(
            inputparameter=True,
            outputparameter=True,
            multiprocessed=False,
            pages=True,
            prefix=False,
            verboseflag=True,
            waitingflag=False,
            cacheflag=False,
        ),
        version=protocol.__version__,
        prog='findings',
    )
    args = utila.parse(parser)
    action = ''
    if args['optimize']:
        action = 'optimize'
    if not action:
        utila.error('nothing todo')
        sys.exit(utila.INVALID_COMMAND)
    choice = (
        args['input'],
        args['output'],
        utila.parse_pages(','.join(args['pages'])),  # DIRTY
        action,
    )
    return choice
