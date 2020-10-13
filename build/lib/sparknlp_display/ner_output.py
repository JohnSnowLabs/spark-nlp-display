import random
import os
import json
from . import style_utils as style_config
from IPython.display import display, HTML

here = os.path.abspath(os.path.dirname(__file__))

class NerOutput:
    def __init__(self):
        with open(os.path.join(here, 'label_colors.json'), 'r', encoding='utf-8') as f_:
            self.label_colors = json.load(f_)

    #public function to get color for a label
    def getLabelColor(self, label):
        """Returns color of a particular label
        
        Input: entity label <string>
        Output: Color <string> or <None> if not found
        """

        if str(label).lower() in self.label_colors:
            return self.label_colors[label.lower()]
        else:
            return None

    # private function for colors for display
    def __getLabel(self, label):
        """Set label colors.
        
        Input: dictionary of entity labels and corresponding colors
        Output: self object - to allow chaining
        Note: Previous values of colors will be overwritten
        """
        if str(label).lower() in self.label_colors:
            return self.label_colors[label.lower()]
        else:
            #update it to fetch from git new labels 
            r = lambda: random.randint(100,255)
            return '#%02X%02X%02X' % (r(), r(), r())

    def setLabelColors(self, color_dict):
        """Sets label colors.

        input: dictionary of entity labels and corresponding colors
        output: self object - to allow chaining
        note: Previous values of colors will be overwritten
        """

        for key, value in color_dict.items():
          self.label_colors[key.lower()] = value
        return self
    
    def __verfiyInput(self, input_result, original_text):
        basic_msg = """
        In sparknlp please use 'LightPipeline.fullAnnotate' for LightPipeline or 'Pipeline.transform' for PipelineModel.
        Or 
        Make sure the result is a list of objects having the following structure: 
            Annotation(type='annotation', begin=0, end=0, result='Adam', metadata={'entity': 'PERSON'})"""
        if not isinstance(original_text, str):
            raise ValueError("Invalid text input. Text should be of type str.")
        if not isinstance(input_result, list):
            raise ValueError("Invalid annotation result. Result should a list of objects."+basic_msg)
        

        for entity in input_result:
            if not hasattr(entity, 'begin'):
                raise AttributeError("Incorrect annotation structure. 'begin' attribute not found in the annotation."+basic_msg)
            if not hasattr(entity, 'end'):
                raise AttributeError("Incorrect annotation structure. 'end' attribute not found in the annotation."+basic_msg)
            if not hasattr(entity, 'result'):
                raise AttributeError("Incorrect annotation structure. 'result' attribute not found in the annotation."+basic_msg)
            if not hasattr(entity, 'metadata'):
                raise AttributeError("Incorrect annotation structure. 'metadata' attribute not found in the annotation."+basic_msg)
            if 'entity' not in entity.metadata:
                raise AttributeError("Incorrect annotation structure. KeyError 'entity' not found in metadata."+basic_msg)

    # main display function
    def __displayNer(self, fully_annotated_text, original_text, labels_list = None):
        self.__verfiyInput(fully_annotated_text, original_text)

        if labels_list is not None:
            labels_list = [v.lower() for v in labels_list]
        label_color = {}
        html_output = ""
        pos = 0
        for entity in fully_annotated_text:
            entity_type = entity.metadata['entity'].lower()
            if (entity_type not in label_color) and ((labels_list is None) or (entity_type in labels_list)) :
                label_color[entity_type] = self.__getLabel(entity_type)

            begin = int(entity.begin)
            end = int(entity.end)
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

    def display(self, result, original_text, labels_list=None):
        """Displays NER visualization. 

        Inputs:
        result -- A list of objects containig annotations.
        original_text -- Original Text
        labels_list -- A list of labels that should be highlighted in the output. Default: Display all labels.

        Output: Visualization
        """
        html_content = self.__displayNer(result, original_text, labels_list)
        html_content = html_content.replace("\n", "<br>")
        
        return display(HTML(style_config.STYLE_CONFIG+ " "+html_content))
