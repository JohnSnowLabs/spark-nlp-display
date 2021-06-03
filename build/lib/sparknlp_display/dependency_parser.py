import random
import os
import json
import pandas as pd
import numpy as np
import svgwrite
from . import style_utils as style_config
from IPython.display import display, HTML

here = os.path.abspath(os.path.dirname(__file__))

class DependencyParserVisualizer:
    
    def __init__(self):
        self.font_path = os.path.join(here, 'fonts/Lucida_Console.ttf')
        self.main_font = 'Lucida'

    def __get_color(self, l):
        r = lambda: random.randint(0,200)
        return '#%02X%02X%02X' % (r(), r(), r())

    def __size(self, text):
        return ((len(text)+1)*12)

    def __draw_line(self, dwg, s_x , s_y, e_x, e_y, d_type, color):
        line = dwg.add(dwg.polyline(
          [
              (e_x, s_y),
          (e_x+2, s_y),
          (e_x, s_y+4),
          (e_x-2, s_y),
          (e_x, s_y)
          ],
          stroke='black', stroke_width = "2", fill='none',))
        
        #if e_x > s_x:
        rad=10
        height=abs(e_y-s_y-4)-rad
        sx = s_x
        sy=300
        distance=abs(e_x-s_x)-rad*2
        if e_x > s_x:
            dwg.add(dwg.path(d=f"M{s_x},{s_y+4} v-{height} a{rad},{rad} 0 0 1 {rad},-{rad} h{distance} a{rad},{rad} 0 0 1 {rad},{rad} v{height-4}",
                 fill="none", 
                 stroke="black", stroke_width=1
                ))
        else:
            dwg.add(dwg.path(d=f"M{s_x},{s_y+4} v-{height} a{rad},{rad} 0 0 0 -{rad},-{rad} h-{distance} a{rad},{rad} 0 0 0 -{rad} {rad} v{height-4}",
                 fill="none", 
                 stroke="black", stroke_width=1
                ))
            
        
        
        dwg.add(dwg.text(d_type, insert=(((s_x+e_x)/2)-(self.__size(d_type.strip())/3.0), e_y-4), 
        fill=color, font_size='14', font_family=self.main_font))

    def __generate_graph(self, result_df):
        # returns an svg graph

        colors_dict = {}
        max_x = 50
        max_y = 100
        
        for i in result_df['dependency_type'].unique():
            colors_dict[i] = self.__get_color(i)
        
        for i in result_df['pos'].unique():
            colors_dict[i] = self.__get_color(i)

        for i, row in result_df.iterrows():
            txt = row['chunk'].strip()
            max_x += (self.__size(txt) + 50)
            max_y += 30
        
        max_x += 50
        start_x = 50
        starty_y = max_y
        dp_dict={}
        tk_dict = {}
        dist_dict = {}
        main_text = []
        main_pos = []

        for i, row in result_df.iterrows():
            txt = row['chunk'].strip()
            dt = row['dependency'].lower().strip()
            is_root = False
            if dt == 'root':
                is_root = True
            main_text.append((txt, start_x, starty_y, is_root))
            main_pos.append(
                (row['pos'].strip(), 
                 (start_x + int((self.__size(txt)/2) - int(self.__size(row['pos'])/2.25))), 
                 starty_y+30))
            
            tk_dict[str(row['begin'])+str(row['end'])] = (start_x+int(self.__size(txt)/2), starty_y)
            start_x += (self.__size(txt) + 50)
        
        y_offset = starty_y-100
        dist_dict = {}
        e_dist_dict = {}
        direct_dict = {}
        left_side_dict = {}
        right_side_dict = {}
        y_hist = {}
        root_list = []
        main_lines = []
        lines_dist = []

        dist = []
        for i, row in result_df.iterrows():
            if row['dependency'].lower().strip() != 'root':
                lines_dist.append(abs(int(row['begin']) - int(row['dependency_start']['head.begin'])))
            else:
                lines_dist.append(0)
            
        result_df = result_df.iloc[np.argsort(lines_dist)]

        count_left = {}
        count_right = {}
        t_x_offset = {}
        for i, row in result_df.iterrows():
            if row['dependency'].lower().strip() != 'root':
                sp = str(row['dependency_start']['head.begin'])+str(row['dependency_start']['head.end'])
                x_e, y_e = tk_dict[str(row['begin'])+str(row['end'])]
                x, y = tk_dict[sp]
                if int(row['begin']) < int(row['dependency_start']['head.begin']):
                    if x in count_left:
                        count_left[x] += 1
                        t_x_offset[x] += 7
                    else:
                        count_left[x] = 1
                        t_x_offset[x] = 7
                    if x_e in count_right:
                        count_right[x_e] += 1
                        t_x_offset[x_e] -= 7
                    else:
                        count_right[x_e] = 0
                        t_x_offset[x_e] = 0
                else:
                    if x in count_right:
                        count_right[x] += 1
                        t_x_offset[x] -= 7
                    else:
                        count_right[x] = 0
                        t_x_offset[x] = 0
                    if x_e in count_left:
                        count_left[x_e] += 1
                        t_x_offset[x_e] += 7
                    else:
                        count_left[x_e] = 1
                        t_x_offset[x_e] = 7
        
        for i, row in result_df.iterrows():
          
            sp = str(row['dependency_start']['head.begin'])+str(row['dependency_start']['head.end'])
            ep = tk_dict[str(row['begin'])+str(row['end'])]

            if sp != '-1-1':
                x, y = tk_dict[sp]

                if int(row['begin']) > int(row['dependency_start']['head.begin']):
                    dist_dict[x] = count_right[x] * 7
                    count_right[x] -= 1
                    e_dist_dict[ep[0]] = count_left[ep[0]] * -7
                    count_left[ep[0]] -= 1
                else:
                    dist_dict[x] = count_left[x] * -7
                    count_left[x] -= 1
                    e_dist_dict[ep[0]] = count_right[ep[0]] * 7
                    count_right[ep[0]] -= 1
                #row['dependency'], x, t_x_offset[x], x+dist_dict[x], x+dist_dict[x]+t_x_offset[x]
                final_x_s = int(x+dist_dict[x]+(t_x_offset[x]/2))
                final_x_e = int(ep[0]+ e_dist_dict[ep[0]]+(t_x_offset[ep[0]]/2))

                x_inds = range(min(final_x_s, final_x_e), max(final_x_s, final_x_e)+1)
                common = set(y_hist.keys()).intersection(set(x_inds))

                if common:
                    y_fset = min([y_hist[c] for c in common])
                    y_fset -= 50
                    y_hist.update(dict(zip(x_inds, [y_fset]*len(x_inds))))

                else:
                    y_hist.update(dict(zip(x_inds, [y_offset]*len(x_inds))))

                main_lines.append((None, final_x_s, y-30, final_x_e, y_hist[final_x_s], row['dependency_type']))

            else:
                x_x , y_y = tk_dict[str(row['begin'])+str(row['end'])]
                
                root_list.append((row['dependency_type'].upper(), x_x, y_y))


        current_y = min(y_hist.values())

        y_ff = (max_y - current_y) + 50
        y_f = (current_y - 50)
        current_y = 50

        dwg = svgwrite.Drawing("temp.svg",
                              profile='full', size = (max_x, y_ff+100))
        dwg.embed_font(self.main_font, self.font_path)

        for mt, mp in zip(main_text, main_pos):
            dwg.add(dwg.text(mt[0], insert=(mt[1], mt[2]-y_f), fill='gray', 
            font_size='20', font_family=self.main_font))

            if mt[3]:
                dwg.add(dwg.rect(insert=(mt[1]-5, mt[2]-y_f-25), rx=5,ry=5, size=(self.__size(mt[0]),35), stroke='#800080', 
                stroke_width='1', fill='none'))

            dwg.add(dwg.text(mp[0], insert=(mp[1], mp[2]-y_f), font_size='14', fill=colors_dict[mp[0]]))

        for ml in main_lines:
            self.__draw_line(dwg, ml[1], ml[2]-y_f, ml[3], ml[4]-y_f, ml[5], colors_dict[ml[5]])
        
        return dwg.tostring()


    def display(self, res, pos_col, dependency_col, dependency_type_col=None, return_html=False):
        """Displays NER visualization. 

        Inputs:
        result -- A Dataframe or dictionary.
        label_col -- Name of the column/key containing NER annotations.
        document_col -- Name of the column/key containing text document.
        original_text -- Original text of type 'str'. If specified, it will take precedence over 'document_col' and will be used as the reference text for display.
        labels_list -- A list of labels that should be highlighted in the output. Default: Display all labels.

        Output: Visualization
        """

        pos_res = []
        for i in res[pos_col]:
            t_ = {'chunk': i.metadata['word'],
            'begin': i.begin,
            'end' : i.end,
            'pos' : i.result}
            pos_res.append(t_)
        dep_res = []
        dep_res_meta = []
        for i in res[dependency_col]:
            dep_res.append(i.result)
            dep_res_meta.append(i.metadata)
        df = pd.DataFrame(pos_res)
        df['dependency'] = dep_res
        df['dependency_start'] = dep_res_meta

        if dependency_type_col != None:
            df['dependency_type'] = [ i.result for i in res[dependency_type_col] ]
        else:
            df['dependency_type'] = ''
        
        html_content = self.__generate_graph(df)
        if return_html:
            return html_content
        else:
            return display(HTML(html_content))
        