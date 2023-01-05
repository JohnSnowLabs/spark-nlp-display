
import random
import os
import json
import pandas as pd
import numpy as np
import svgwrite
import math
import re
from IPython.display import display, HTML

here = os.path.abspath(os.path.dirname(__file__))
#overlap_hist = []
#y_hist_dict = {}
x_i_diff_dict = {}
x_o_diff_dict = {}
class RelationExtractionVisualizer:
    
    def __init__(self):
        with open(os.path.join(here, 'label_colors/relations.json'), 'r', encoding='utf-8') as f_:
            self.color_dict = json.load(f_)
        with open(os.path.join(here, 'label_colors/ner.json'), 'r', encoding='utf-8') as f_:
            self.entity_color_dict = json.load(f_)
            self.entity_color_dict = dict((k.lower(), v) for k, v in self.entity_color_dict.items())
            self.font_path = os.path.join(here, 'fonts/Lucida_Console.ttf')
            self.main_font = 'Lucida'
    def __get_color(self, l):
        r = lambda: random.randint(0,200)
        return '#%02X%02X%02X' % (r(), r(), r())

    def __size(self, text):
        return ((len(text)+1)*9.7)-5

    def __draw_line(self, dwg, s_x , s_y, e_x, e_y, d_type, color, show_relations, size_of_entity_label):
        eps = 0.0000001
        def get_bezier_coef(points):
            # since the formulas work given that we have n+1 points
            # then n must be this:
            n = len(points) - 1

            # build coefficents matrix
            C = 4 * np.identity(n)
            np.fill_diagonal(C[1:], 1)
            np.fill_diagonal(C[:, 1:], 1)
            C[0, 0] = 2
            C[n - 1, n - 1] = 7
            C[n - 1, n - 2] = 2

            # build points vector
            P = [2 * (2 * points[i] + points[i + 1]) for i in range(n)]
            P[0] = points[0] + 2 * points[1]
            P[n - 1] = 8 * points[n - 1] + points[n]

            # solve system, find a & b
            A = np.linalg.solve(C, P)
            B = [0] * n
            for i in range(n - 1):
                B[i] = 2 * points[i + 1] - A[i + 1]
            B[n - 1] = (A[n - 1] + points[n]) / 2

            return A, B

        # returns the general Bezier cubic formula given 4 control points
        def get_cubic(a, b, c, d):
            return lambda t: np.power(1 - t, 3) * a + 3 * np.power(1 - t, 2) * t * b + 3 * (1 - t) * np.power(t, 2) * c + np.power(t, 3) * d

        # return one cubic curve for each consecutive points
        def get_bezier_cubic(points):
            A, B = get_bezier_coef(points)
            return [
                get_cubic(points[i], A[i], B[i], points[i + 1])
                for i in range(len(points) - 1)
            ]

        # evalute each cubic curve on the range [0, 1] sliced in n points
        def evaluate_bezier(points, n):
            curves = get_bezier_cubic(points)
            return np.array([fun(t) for fun in curves for t in np.linspace(0, 1, n)])


        def draw_pointer(dwg, s_x, s_y, e_x, e_y):
            size = 5
            ratio = 1
            fullness1 = 2
            fullness2 = 3
            bx = e_x
            ax = s_x
            by = e_y
            ay = s_y
            abx = bx - ax
            aby = by - ay
            ab = np.sqrt(abx * abx + aby * aby) + eps

            cx = bx - size * abx / ab
            cy = by - size * aby / ab
            dx = cx + (by - cy) / ratio
            dy = cy + (cx - bx) / ratio
            ex = cx - (by - cy) / ratio
            ey = cy - (cx - bx) / ratio
            fx = (fullness1 * cx + bx) / fullness2
            fy = (fullness1 * cy + by) / fullness2

            text_place_y = s_y-(abs(s_y-e_y)/2)
            '''
            line = dwg.add(dwg.polyline(
                      [
                      (bx, by),    
                      (dx, dy),
                      (fx, fy),
                      (ex, ey),
                      (bx, by)
                      ],
                      stroke=color, stroke_width = "1", fill='none',))
            '''
            line = dwg.add(dwg.polyline(
                      [
                      (dx, dy),
                      (bx, by),    
                      (ex, ey),
                      (bx, by)
                      ],
                      stroke=color, stroke_width = "1", fill='none',))
            return text_place_y
        unique_o_index = str(s_x)+str(s_y)
        unique_i_index = str(e_x)+str(e_y)
        if s_x > e_x:
            if unique_o_index in x_o_diff_dict:
                s_x -= 5
            else:
                s_x -= 10
                x_o_diff_dict[unique_o_index] = 5
            if s_y > e_y:
                e_x += size_of_entity_label
            elif s_y < e_y:
                s_x -= size_of_entity_label
                
            if unique_i_index in x_i_diff_dict:
                e_x += 5
            else:
                e_x += 10
                x_i_diff_dict[unique_i_index] = 5
        else:
            if unique_o_index in x_o_diff_dict:
                s_x += 5
            else:
                s_x += 10
                x_o_diff_dict[unique_o_index] = 5
            if s_y > e_y:
                e_x -= size_of_entity_label
            elif s_y < e_y:
                s_x += size_of_entity_label
                
            if unique_i_index in x_i_diff_dict:
                e_x -= 5
            else:
                e_x -= 10
                x_i_diff_dict[unique_i_index] = 5
        #this_y_vals = list(range(min(s_x,e_x), max(s_x,e_x)+1))
        #this_y_vals = [ str(s_y)+'|'+str(i) for i in this_y_vals]
        #common = set(this_y_vals) & set(overlap_hist)
        #overlap_hist.extend(this_y_vals)
        #if s_y not in y_hist_dict:
        #    y_hist_dict[s_y] = 20
        #if common:
        #    y_hist_dict[s_y] += 20
        #y_increase = y_hist_dict[s_y]
        angle = -1
        if s_y == e_y:
            angle = 0
            s_y -= 20
            e_y = s_y-4#55
            
            text_place_y = s_y-35

            pth = evaluate_bezier(np.array([[s_x, s_y], 
                                [(s_x+e_x)/2.0, s_y-40],
                                [e_x,e_y]]), 50)
            dwg.add(dwg.polyline(pth,
                stroke=color, stroke_width = "1", fill='none',))
            draw_pointer(dwg, (s_x+e_x)/2.0, s_y-50, e_x, e_y)
        elif s_y >= e_y:
            
            e_y +=15
            s_y-=20
            text_place_y = s_y-(abs(s_y-e_y)/2)
            
            pth = evaluate_bezier(np.array([[s_x, s_y],
                                #[((3*s_x)+e_x)/4.0, (s_y+e_y)/2.0],
                                [(s_x+e_x)/2.0, (s_y+e_y)/2.0],
                                #[(s_x+(3*e_x))/4.0,(s_y+e_y)/2.0],
                                [e_x,e_y]]), 50)
            dwg.add(dwg.polyline(pth,
                stroke=color, stroke_width = "1", fill='none',))
            draw_pointer(dwg, s_x, s_y, e_x, e_y)

            '''
            line = dwg.add(dwg.polyline(
                    [(s_x, s_y),(s_x, s_y-y_increase), (e_x, s_y-y_increase),
                    (e_x, e_y),    
                    (e_x+2, e_y),
                    (e_x, e_y-4),
                    (e_x-2, e_y),
                    (e_x, e_y)
                    ],
                    stroke=color, stroke_width = "2", fill='none',))
            '''
        else:
            
            s_y+=15
            e_y -= 20
            text_place_y = s_y+(abs(s_y-e_y)/2)
            
            pth = evaluate_bezier(np.array([[s_x, s_y],
                                #[((3*s_x)+e_x)/4.0, (s_y+e_y)/2.0],
                                [(s_x+e_x)/2.0, (s_y+e_y)/2.0],
                                #[(s_x+(3*e_x))/4.0,(s_y+e_y)/2.0],
                                [e_x,e_y]]), 50)
            dwg.add(dwg.polyline(pth,
                stroke=color, stroke_width = "1", fill='none',))
            draw_pointer(dwg, s_x, s_y, e_x, e_y)
            
        if show_relations:
            if angle == -1: angle = math.degrees(math.atan((s_y-e_y)/((s_x-e_x)+eps)))
            rel_temp_size = self.__size(d_type)/1.35
            rect_x, rect_y = (((s_x+e_x)/2.0)-(rel_temp_size/2.0)-3, text_place_y-10)
            rect_w, rect_h = (rel_temp_size+3,13)
            dwg.add(dwg.rect(insert=(rect_x, rect_y), rx=2,ry=2, 
            size=(rect_w, rect_h), 
            fill='white', stroke=color , stroke_width='1', 
            transform = f"rotate({angle} {rect_x+rect_w/2} {rect_y+rect_h/2})"))

            dwg.add(dwg.text(d_type, insert=(((s_x+e_x)/2)-(rel_temp_size/2.0), text_place_y), 
            fill=color, font_size='12', font_family='courier',
            transform = f"rotate({angle} {rect_x+rect_w/2} {rect_y+rect_h/2})"))

    def __gen_graph(self, rdf, selected_text, exclude_relations, show_relations):
        exclude_relations = [ i.lower().strip() for i in exclude_relations]
        rdf = [ i for i in rdf if i.result.lower().strip() not in exclude_relations]

        done_ent1 = {}
        done_ent2 = {}
        all_done = {}
        
        start_y = 75
        x_limit = 1000
        y_offset = 100
        #dwg = svgwrite.Drawing("temp.svg",profile='full', size = (x_limit, len(selected_text) * 1.1 + len(rdf)*20))
        
        begin_index = 0
        start_x = 10
        this_line = 0

        all_entities_index = set()
        all_entities_1_index = []
        basic_dict = {}
        relation_dict = {}
        for t in rdf:
        
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
            if t.metadata['entity1'].lower().strip() not in self.entity_color_dict:
                self.entity_color_dict[t.metadata['entity1'].lower().strip()] = self.__get_color(t.metadata['entity1'].lower().strip())
            if t.metadata['entity2'].lower().strip() not in self.entity_color_dict:
                self.entity_color_dict[t.metadata['entity2'].lower().strip()] = self.__get_color(t.metadata['entity2'].lower().strip())  
             
        
            #all_entities_1_index.append(t[4]['entity1_begin'])
        all_entities_index = np.asarray(list(all_entities_index))
        all_entities_index = all_entities_index[np.argsort(all_entities_index)]
        dwg_rects, dwg_texts = [], []
        for ent_start_ind in all_entities_index:
            e_start_now, e_end_now, e_chunk_now, e_entity_now = basic_dict[ent_start_ind]
            prev_text = selected_text[begin_index:int(e_start_now)]
            prev_text = re.sub(r'\s*(\n)+', r'\1', prev_text.strip(), re.MULTILINE)
            begin_index = int(e_end_now)+1
            for line_num, line in enumerate(prev_text.split('\n')):
                if line_num != 0:
                    start_y += y_offset
                    start_x = 10
                    this_line = 0
                for word_ in line.split(' '):
                    this_size = self.__size(word_)
                    if (start_x + this_size + 10) >= x_limit:
                        start_y += y_offset
                        start_x = 10
                        this_line = 0
                    dwg_texts.append([word_, (start_x, start_y ), '#546c74', '16', self.main_font, 'font-weight:100'])
                    #dwg.add(dwg.text(word_, insert=(start_x, start_y ), fill='#546c77', font_size='16', 
                    #                 font_family='Monaco', style='font-weight:lighter'))
                    start_x += this_size + 10
                
            this_size = self.__size(e_chunk_now)
            if (start_x + this_size + 10)>= x_limit:# or this_line >= 2:
                    start_y += y_offset
                    start_x = 10
                    this_line = 0
                    
            #rectange chunk 1
            dwg_rects.append([(start_x-3, start_y-18), (this_size,25), self.entity_color_dict[e_entity_now.lower().strip()]])
            #dwg.add(dwg.rect(insert=(start_x-3, start_y-18),rx=2,ry=2, size=(this_size,25), stroke=self.entity_color_dict[e_entity_now.lower()], 
            #stroke_width='1', fill=self.entity_color_dict[e_entity_now.lower()], fill_opacity='0.2'))
            #chunk1
            dwg_texts.append([e_chunk_now, (start_x, start_y ), '#546c74', '16', self.main_font, 'font-weight:100'])
            #dwg.add(dwg.text(e_chunk_now, insert=(start_x, start_y ), fill='#546c77', font_size='16', 
            #                 font_family='Monaco', style='font-weight:lighter'))
            #entity 1
            central_point_x = start_x+(this_size/2)
            temp_size = self.__size(e_entity_now)/2.75
            dwg_texts.append([e_entity_now.upper(), (central_point_x-temp_size, start_y+20), '#1f77b7', '12', self.main_font, 'font-weight:lighter'])
            #dwg.add(dwg.text(e_entity_now.upper(), 
            #                insert=(central_point_x-temp_size, start_y+20), 
            #                fill='#1f77b7', font_size='12', font_family='Monaco',
            #                style='font-weight:lighter'))
            
            all_done[int(e_start_now)] = [central_point_x, start_y, temp_size]
            start_x += this_size + 20
            this_line += 1 
        

        prev_text = selected_text[begin_index:]
        prev_text = re.sub(r'\s*(\n)+', r'\1', prev_text.strip(), re.MULTILINE)
        for line_num, line in enumerate(prev_text.split('\n')):
            if line_num != 0:
                start_y += y_offset
                start_x = 10
            for word_ in line.split(' '):
                this_size = self.__size(word_)
                if (start_x + this_size)>= x_limit:
                    start_y += y_offset
                    start_x = 10
                dwg_texts.append([word_, (start_x, start_y ), '#546c77', '16', self.main_font, 'font-weight:100'])
                #dwg.add(dwg.text(word_, insert=(start_x, start_y ), fill='#546c77', font_size='16', 
                #                 font_family='Monaco', style='font-weight:lighter'))
                start_x += this_size + 10
            
        
        dwg = svgwrite.Drawing("temp.svg",profile='full', size = (x_limit, start_y+y_offset))
        dwg.embed_font(self.main_font, self.font_path)
        
        for crect_ in dwg_rects:
            dwg.add(dwg.rect(insert=crect_[0],rx=2,ry=2, size=crect_[1], stroke=crect_[2], 
            stroke_width='1', fill=crect_[2], fill_opacity='0.2'))
            
        for ctext_ in dwg_texts:
            dwg.add(dwg.text(ctext_[0], insert=ctext_[1], fill=ctext_[2], font_size=ctext_[3], 
                             font_family=ctext_[4], style=ctext_[5]))
        
        
        relation_distances = []
        relation_coordinates = []
        for row in rdf:
            if row.result.lower().strip() not in self.color_dict:
                self.color_dict[row.result.lower().strip()] = self.__get_color(row.result.lower().strip())
            
            d_key2 = all_done[int(row.metadata['entity1_begin'])]
            d_key1 = all_done[int(row.metadata['entity2_begin'])]
            this_dist = abs(d_key2[0] - d_key1[0]) + abs (d_key2[1]-d_key1[1])
            relation_distances.append(this_dist)
            relation_coordinates.append((d_key2, d_key1, row.result))
        
        relation_distances = np.array(relation_distances)
        relation_coordinates = np.array(relation_coordinates)
        temp_ind = np.argsort(relation_distances)
        relation_distances = relation_distances[temp_ind]
        relation_coordinates = relation_coordinates[temp_ind]
        for row in relation_coordinates:
            #if int(row[0][1]) == int(row[1][1]):
            size_of_entity_label = int(row[1][2])
            self.__draw_line(dwg, int(row[0][0]) , int(row[0][1]), int(row[1][0]), int(row[1][1]), 
                            row[2],self.color_dict[row[2].lower().strip()], show_relations, size_of_entity_label)
        
        return dwg.tostring()

    def display(self, result, relation_col, document_col='document', exclude_relations=['O'], show_relations=True, return_html=False, save_path=None):
        """Displays Relation Extraction visualization. 
        Inputs:
        result -- A Dataframe or dictionary.
        relation_col -- Name of the column/key containing relationships.
        document_col -- Name of the column/key containing text document.
        exclude_relations -- list of relations that don't need to be displayed. Default: ["O"]
        show_relations -- Display relation types on arrows. Default: True
        return_html -- If true, returns raw html code instead of displaying. Default: False
        Output: Visualization
        """

        original_text = result[document_col][0].result
        res = result[relation_col]
        
        html_content = self.__gen_graph(res, original_text, exclude_relations, show_relations)
        
        if save_path != None:
            with open(save_path, 'w') as f_:
                f_.write(html_content)
        
        if return_html:
            return html_content
        else:
            return display(HTML(html_content))
