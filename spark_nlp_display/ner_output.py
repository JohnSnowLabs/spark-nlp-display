import random
import base64
import pandas as pd
import numpy as np
import os
import json
from . import style_utils as style_config
from IPython.display import display, HTML

this_path = os.path.abspath(os.path.dirname(__file__))

class NerOutput:
    def __init__(self):
        with open(os.path.join(this_path, 'label_colors.json'), 'r', encoding='utf-8') as f_:
            self.label_colors = json.load(f_)

    #public function to get color for a label
    def getLabelColor(self, label):
        if str(label).lower() in self.label_colors:
            return self.label_colors[label.lower()]
        else:
            return None

    # private function for colors for display
    def __getLabel(self, label):
        if str(label).lower() in self.label_colors:
            return self.label_colors[label.lower()]
        else:
            #update it to fetch from git new labels 
            r = lambda: random.randint(100,255)
            return '#%02X%02X%02X' % (r(), r(), r())

    # set label color manually
    def setLabelColor(self, label, color):
        self.label_colors[label.lower()] = color
        return self
  
    # main display function
    def __displayNer(self, original_text , fully_annotated_text, labels_list = None):
        if labels_list is not None:
            labels_list = [v.lower() for v in labels_list]
        label_color = {}
        html_output = ""
        pos = 0
        for entity in fully_annotated_text:
            entity_type = entity.metadata['entity'].lower()
            if (entity_type not in label_color) and ((labels_list is None) or (entity_type in labels_list)) :
                label_color[entity_type] = self.__getLabel(entity_type)

            begin = entity.begin
            end = entity.end
            if pos < begin and pos < len(original_text):
                white_text = original_text[pos:begin]
                html_output += '<span class="others" style="background-color: white">{}</span>'.format(white_text)
            pos = end+1

            if entity_type in label_color:
                html_output += '<span class="entity-wrapper" style="background-color: {}"><span class="entity-name">{} </span><span class="entity-type">{}</span></span>'.format(
                    label_color[entity_type],
                    entity.result,
                    entity.metadata['entity'])
            else:
                html_output += '<span class="others" style="background-color: white">{}</span>'.format(entity.result)

        if pos < len(original_text):
            html_output += '<span class="others" style="background-color: white">{}</span>'.format(original_text[pos:])

        html_output += """</div>"""
        return html_output

    def display(self, result, original_text, result_column, labels_list=None):

        annotated_column_values = result[result_column]
        html_content = self.__displayNer(original_text, annotated_column_values, labels_list)
        html_content = html_content.replace("\n", "<br>")
        
        return display(HTML(style_config.STYLE_CONFIG+ " "+html_content))
