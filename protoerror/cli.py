# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import sys

import serializeraw
import utilo

import protoerror


@utilo.saveme
def main():
    inpath, outpath, pages, action = evaluate()
    for path in inpath:
        if not utilo.exists(path):
            utilo.error(f'input does not exists: {path}')
            return utilo.FAILURE
    if not utilo.exists(outpath):
        utilo.error(f'output does not exists: {outpath}')
        return utilo.FAILURE
    if action == 'optimize':
        optimize(srcs=inpath, dest=outpath, pages=pages)
        return utilo.SUCCESS
    return utilo.INVALID_COMMAND


def optimize(srcs: str, dest: str, pages: tuple = None, msgid: set = None):
    findings = []
    for src in srcs:
        utilo.log(f'load findings from: {src}', preserve_newlines=False)
    findings = serializeraw.findings_from_path(
        path=srcs,
        msgid=msgid,
        pages=pages,
    )
    findings = utilo.flatten_content(findings)
    dest = os.path.join(dest, '__optimized__')
    os.makedirs(dest, exist_ok=True)
    utilo.log(
        f'write optimized findings to: {dest}',
        preserve_newlines=False,
    )
    serializeraw.write_grouped(findings, dest=dest)


def evaluate() -> tuple:
    parser = utilo.cli.create_parser(
        todo=[
            utilo.cli.Flag(
                longcut='optimize',
                message='read findings and write to page dependent structure',
            ),
        ],
        config=utilo.ParserConfiguration(
            inputparameter=True,
            outputparameter=True,
            multiprocessed=False,
            pages=True,
            prefix=False,
            verboseflag=True,
            waitingflag=False,
            cacheflag=False,
        ),
        version=protoerror.__version__,
        prog='findings',
    )
    args = utilo.parse(parser)
    action = ''
    if args['optimize']:
        action = 'optimize'
    if not action:
        utilo.error('nothing todo')
        sys.exit(utilo.INVALID_COMMAND)
    choice = (
        args['input'],
        args['output'],
        utilo.parse_pages(','.join(args['pages'])),  # DIRTY
        action,
    )
    return choice
