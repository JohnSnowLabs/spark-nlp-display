import os
from sparknlp_display.ner import NerVisualizer
from sparknlp_display.dependency_parser import DependencyParserVisualizer
from sparknlp_display.relation_extraction import RelationExtractionVisualizer
from sparknlp_display.entity_resolution import EntityResolverVisualizer
from sparknlp_display.assertion import AssertionVisualizer

here = os.path.abspath(os.path.dirname(__file__))

def get_version():
    version_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, "VERSION"), "r") as fh:
        app_version = fh.read().strip()
        return app_version

__version__ = get_version()

def version():
    return get_version()