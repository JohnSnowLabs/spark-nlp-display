import os

HTML_WRAPPER = """<div class="spark-nlp-display-scroll-entities" style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem; white-space:pre-wrap">{}</div>"""
HTML_INDEX_WRAPPER = """<div ">{}</div>"""

STYLE_CONFIG_ENTITIES = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Vistol Regular:wght@300;400;500;600;700&display=swap');
    
    .spark-nlp-display-scroll-entities {{
        border: 1px solid #E7EDF0;
        border-radius: 3px;
        text-align: justify;
        
    }}
    .spark-nlp-display-scroll-entities span {{  
        font-size: 14px;
        line-height: 24px;
        color: #536B76;
        font-family: 'Montserrat', sans-serif !important;
    }}
    
    .spark-nlp-display-entity-wrapper{{
    
        display: inline-grid;
        text-align: center;
        border-radius: 4px;
        margin: 0 2px 5px 2px;
        padding: 1px
    }}
    .spark-nlp-display-entity-name{{
        font-size: 14px;
        line-height: 24px;
        font-family: 'Montserrat', sans-serif !important;
        
        background: #f1f2f3;
        border-width: medium;
        text-align: center;
        
        font-weight: 400;
        
        border-radius: 5px;
        padding: 2px 5px;
        display: block;
        margin: 3px 2px;
    
    }}
    .spark-nlp-display-entity-type{{
        font-size: 14px;
        line-height: 24px;
        color: #ffffff;
        font-family: 'Montserrat', sans-serif !important;
        
        text-transform: uppercase;
        
        font-weight: 500;

        display: block;
        padding: 3px 5px;
    }}
    
    .spark-nlp-display-entity-resolution{{
        font-size: 14px;
        line-height: 24px;
        color: #ffffff;
        font-family: 'Vistol Regular', sans-serif !important;
        
        text-transform: uppercase;
        
        font-weight: 500;

        display: block;
        padding: 3px 5px;
    }}
    
    .spark-nlp-display-others{{
        font-size: 14px;
        line-height: 24px;
        font-family: 'Montserrat', sans-serif !important;
        
        font-weight: 400;
    }}

</style>
"""
