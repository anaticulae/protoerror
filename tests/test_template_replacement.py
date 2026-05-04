# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protoerror.solution

TEMPLATE = """\
{%if MSWORD %}
Erstellen Sie das Inhaltsverzeichnis indem Sie die Reiter
Start->Programme->Generator klicken. Danach klicken sie doppelt auf Los.
{% endif %}
{%if LATEX %}
Include \\toc to generate a beautyfull table of content
{% endif %}
{%if BASE %}
Hier spricht Helm
{% endif %}
"""


def test_render_template():
    latex = protoerror.solution.render_template(
        TEMPLATE,
        LATEX=True,
    )
    expected = 'Include \\toc to generate a beautyfull table of content'
    assert expected == latex
