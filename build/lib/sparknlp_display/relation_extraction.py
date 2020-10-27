import random
import os
import json
import pandas as pd
import numpy as np
import svgwrite
from IPython.display import display, HTML

here = os.path.abspath(os.path.dirname(__file__))

class RelationExtractionOutput:

    def __init__(self):
        with open(os.path.join(here, 'label_colors/relations.json'), 'r', encoding='utf-8') as f_:
            self.color_dict = json.load(f_)
            
    def __get_color(self, l):
        r = lambda: random.randint(100,255)
        return '#%02X%02X%02X' % (r(), r(), r())

    def __size(self, text):
        return ((len(text)+1)*9.7)-5

    def __draw_line(self, dwg, s_x , s_y, e_x, e_y, d_type, color, show_relations):
        if s_x > e_x:
            #s_x -= 5
            e_x += 10
        else:
            #s_x += 5
            e_x -= 10
        if s_y == e_y:
            s_y -= 20
            e_y = s_y-4#55
            text_place_y = s_y-45
            line = dwg.add(dwg.polyline(
                [(s_x, s_y), (s_x, s_y-10), ((s_x+e_x)/2, s_y-40), (e_x, s_y-10),
                (e_x, e_y),    
                (e_x+2, e_y),
                (e_x, e_y+4),
                (e_x-2, e_y),
                (e_x, e_y)
                ],
                stroke=color, stroke_width = "2", fill='none',))
        elif s_y >= e_y:
            e_y +=30
            s_y-=20
            text_place_y = s_y-(abs(s_y-e_y)/2)
            line = dwg.add(dwg.polyline(
                    [(s_x, s_y),(s_x, s_y-10), (e_x, e_y+10),
                    (e_x, e_y),    
                    (e_x+2, e_y),
                    (e_x, e_y-4),
                    (e_x-2, e_y),
                    (e_x, e_y)
                    ],
                    stroke=color, stroke_width = "2", fill='none',))
        else:
            s_y-=5
            e_y -= 40
            text_place_y = s_y+(abs(s_y-e_y)/2)
            line = dwg.add(dwg.polyline(
                    [(s_x, s_y),
                    (e_x, e_y-40),    
                    (e_x+2, e_y),
                    (e_x, e_y+4),
                    (e_x-2, e_y),
                    (e_x, e_y)
                    ],
                    stroke=color, stroke_width = "2", fill='none',))
        if show_relations:
            dwg.add(dwg.text(d_type, insert=(((s_x+e_x)/2)-(self.__size(d_type)/2.75), text_place_y), 
            fill=color, font_size='12', font_family='courier'))

    def __gen_graph(self, rdf, selected_text, show_relations):
        
        done_ent1 = {}
        done_ent2 = {}
        all_done = {}
        
        start_y = 75
        x_limit = 920
        y_offset = 100
        dwg = svgwrite.Drawing("temp.svg",profile='tiny', size = (x_limit, len(selected_text) * 1.1 + len(rdf)*20))
        
        begin_index = 0
        start_x = 10
        this_line = 0

        all_entities_index = set()
        all_entities_1_index = []
        basic_dict = {}
        relation_dict = {}
        for t in rdf:
            if t.result.lower().strip() != 'o':
                all_entities_index.add(int(t.metadata['entity1_begin']))
                all_entities_index.add(int(t.metadata['entity2_begin']))
                basic_dict[int(t.metadata['entity1_begin'])] = [t.metadata['entity1_begin'],
                                                    t.metadata['entity1_end'],
                                                    t.metadata['chunk1'], 
                                                    t.metadata['entity1']]

                basic_dict[int(t.metadata['entity2_begin'])] = [t.metadata['entity2_begin'],
                                                    t.metadata['entity2_end'],
                                                    t.metadata['chunk2'], 
                                                    t.metadata['entity2']]
            
            #all_entities_1_index.append(t[4]['entity1_begin'])
        all_entities_index = np.asarray(list(all_entities_index))
        all_entities_index = all_entities_index[np.argsort(all_entities_index)]
        for ent_start_ind in all_entities_index:
            e_start_now, e_end_now, e_chunk_now, e_entity_now = basic_dict[ent_start_ind]
            prev_text = selected_text[begin_index:int(e_start_now)]
            begin_index = int(e_end_now)+1
            for word_ in prev_text.split(' '):
                this_size = self.__size(word_)
                if (start_x + this_size + 10) >= x_limit:
                    start_y += y_offset
                    start_x = 10
                    this_line = 0
                dwg.add(dwg.text(word_, insert=(start_x, start_y ), fill='gray', font_size='16', font_family='courier'))
                start_x += this_size + 5
                
            this_size = self.__size(e_chunk_now)
            if (start_x + this_size + 10)>= x_limit:# or this_line >= 2:
                    start_y += y_offset
                    start_x = 10
                    this_line = 0
            #chunk1
            dwg.add(dwg.text(e_chunk_now, insert=(start_x, start_y ), fill='gray', font_size='16', font_family='courier'))
            #rectange chunk 1
            dwg.add(dwg.rect(insert=(start_x-3, start_y-18), size=(this_size,25), stroke='orange', 
            stroke_width='2', fill='none'))
            #entity 1
            central_point_x = start_x+(this_size/2)
            
            dwg.add(dwg.text(e_entity_now, 
                            insert=(central_point_x-(self.__size(e_entity_now)/2.75), start_y+20), 
                            fill='mediumseagreen', font_size='12', font_family='courier'))
            
            all_done[int(e_start_now)] = [central_point_x, start_y]
            start_x += this_size + 10
            this_line += 1 
              
            #all_done[ent_start_ind] = 
        
        prev_text = selected_text[begin_index:]        
        for word_ in prev_text.split(' '):
            this_size = self.__size(word_)
            if (start_x + this_size)>= x_limit:
                start_y += y_offset
                start_x = 10
            dwg.add(dwg.text(word_, insert=(start_x, start_y ), fill='gray', font_size='16', font_family='courier'))
            start_x += this_size

        for row in rdf:
            if row.result.lower().strip() != 'o':
                if row.result.lower().strip() not in self.color_dict:
                    self.color_dict[row.result.lower().strip()] = self.__get_color(row.result.lower().strip())
                d_key2 = all_done[int(row.metadata['entity2_begin'])]
                d_key1 = all_done[int(row.metadata['entity1_begin'])]
                self.__draw_line(dwg, d_key2[0] , d_key2[1], d_key1[0], d_key1[1], 
                          row.result,self.color_dict[row.result.lower().strip()], show_relations)
            
        return dwg.tostring()

    def display(self, result, relation_col, document_col='document', show_relations=True):

        original_text = result[document_col][0].result
        res = result[relation_col]
        return display(HTML(self.__gen_graph(res, original_text, show_relations)))
