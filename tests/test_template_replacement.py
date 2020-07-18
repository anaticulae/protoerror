# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol.control

TEMPLATE = """\
{%MSWORD%}
Erstellen Sie das Inhaltsverzeichnis indem Sie die Reiter
Start->Programme->Generator klicken. Danach klicken sie doppelt auf Los.
{%MSWORD_END%}
{%LATEX%}
Include \\toc to generate a beautyfull table of content
{%LATEX_END%}
{%BASE%}
Hier spricht Helm
{%BASE_END%}
"""


def test_render_template():
    latex = protocol.control.render_template(
        TEMPLATE,
        protocol.control.Generator.LATEX,
    )
    expected = 'Include \\toc to generate a beautyfull table of content\n'
    assert expected == latex
