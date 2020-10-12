import os

ENTITIES_FOR_ICD10 = ['problem', 'diagnosis', 'procedure name', 'lab name', 'symptom_name', 'procedure_name', 'procedure', 'lab_name', 'pathological_formation', 'cancer']


#APP STYLE
MAX_WIDTH = 1600
PADDING_TOP = 1
PADDING_BOTTOM = 1
PADDING_RIGHT = 4
PADDING_LEFT = 4
COLOR = 'black'
BACKGROUND_COLOR = 'white'

HTML_WRAPPER = """<div class="scroll entities" style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem; white-space:pre-wrap">{}</div>"""
HTML_INDEX_WRAPPER = """<div ">{}</div>"""

STYLE_CONFIG_OLD = f"""
<style>
    *:not(text){{
      font-family: Montserrat !important;
    }}
    .reportview-container .main .block-container{{
        max-width: {MAX_WIDTH}px;
        padding-top: {PADDING_TOP}rem;
        padding-right: {PADDING_RIGHT}rem;
        padding-left: {PADDING_LEFT}rem;
        padding-bottom: {PADDING_BOTTOM}rem;
    }}
    .reportview-container .main {{
        color: {COLOR};
        background-color: {BACKGROUND_COLOR};
    }}
    div.scroll {{ 
                margin:4px, 4px; 
                padding:4px; 
                width: 100%; 
                height: 500px; 
                overflow-x: hidden; 
                overflow-x: auto;  
    }}
    .entity-wrapper{{
        padding: 5px;
        display: inline-grid;
        text-align:center;
        margin-bottom:5px;
        border-radius: 5px 5px
    }}
    .entity-name{{
        background: #f1f2f3;
        color: #3c3e44;
        padding: 2px;
        border-color: #484b51;
        border-width: medium;
        border-radius: 5px 5px;
    }}
    .entity-type{{
        color: #272727;
        text-transform: uppercase;
        font-family: roboto;
        font-size: 13px;
    }}
    .reportview-container .markdown-text-container{{
        font-family: roboto !important;
        color: dimgray !important;
        line-height: normal !important;
    }}
    .reportview-container h2
    {{
        font-weight: 400 !important;
        font-size: 1.5rem !important;
        line-height: 1.6!important;
    }}
    .reportview-container h2
    {{
        font-weight: 300 !important;
        font-size: 1.3rem !important;
        line-height: 1.4!important;
    }}
    .Widget>label
    {{
        font-size: 1.3rem !important;
        color: dimgray !important;
        margin-bottom: .4rem !important;
    }}
    
</style>
"""

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'style.css'), 'r', encoding='utf-8') as f:
    STYLE_CONFIG_NEW = f.read()
STYLE_CONFIG = STYLE_CONFIG_OLD + '<style>{}</style>'.format(STYLE_CONFIG_NEW)

LABEL_COLORS = {'problem':'#cceeff',
               'test':'#e6ccff',
               'treatment':'#ffffcc',
                'multi':'#ccfff5',
                'multi-tissue_structure':'#8dd8b4',
                'cell':'#ffe6cc',
                'organism':'#ffddcc',
                'gene_or_gene_product':'#fff0b3',
                'organ':'#e6e600',
                'simple_chemical':'#ffd699',
                'drug':'#8B668B',
                'diagnosis':'#b5a1c9',
                'maybe':'#FFB5C5',
                'lab_result':'#3abd80',
                'negated':'#CD3700',
                'name':'#C0FF3E',
                'lab_name':'#698B22',
                'modifier':'#8B475D',
                'symptom_name':'#CDB7B5',
                'section_name':'#8B7D7B',
                'drug_name':'#BDFCC9',
                'procedure_name':'#48D1CC',
                'grading':"#8c61e8",
                'size':"#746b87",
                'organism_substance':'#ffaa80',
                'gender':'#ffacb7',
                'age':'#ffe0ac',
                'date': '#a6b1e1'
                }