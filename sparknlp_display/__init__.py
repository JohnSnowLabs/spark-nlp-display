import os
from sparknlp_display.ner_output import NerOutput
from sparknlp_display.dependency_parser import DependencyParserOutput

here = os.path.abspath(os.path.dirname(__file__))

def get_version():
    version_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, "VERSION"), "r") as fh:
        app_version = fh.read().strip()
        return app_version

__version__ = get_version()