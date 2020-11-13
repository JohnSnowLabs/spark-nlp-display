# spark-nlp-display
A library for the simple visualization of different types of Spark NLP annotations. 

## Supported Visualizations:
- Dependency Parser
- Named Entity Recognition
- Entity Resolution
- Relation Extraction
- Assertion Status

### How to use

#### Dependency Parser
```python
from sparknlp_display import DependencyParserVisualizer

dependency_vis = DependencyParserVisualizer()

dependency_vis.display(pipeline_result, #should be the results of a single example, not the complete dataframe.
                       pos_col = 'pos', #specify the pos column
                       dependency_col = 'dependency', #specify the dependency column
                       dependency_type_col = 'dependency_type' #specify the dependency type column
                       )
```

#### Named Entity Recognition

```python
from sparknlp_display import NerVisualizer

ner_vis = NerVisualizer()

ner_vis.set_label_colors({'LOC':'#800080', 'PER':'#77b5fe'}) #set label colors by specifying hex codes

ner_vis.display(pipeline_result, #should be the results of a single example, not the complete dataframe
                    label_col='entities', #specify the entity column
                    document_col='document' #specify the document column (default: 'document')
                    labels=['PER'] #only allow these labels to be displayed. (default: [] - all labels will be displayed)
                    )

```

#### Entity Resolution

```python
from sparknlp_display import EntityResolverVisualizer

er_vis = EntityResolverVisualizer()

er_vis.set_label_colors({'TREATMENT':'#800080', 'PROBLEM':'#77b5fe'}) #set label colors by specifying hex codes

er_vis.display(pipeline_result, #should be the results of a single example, not the complete dataframe
               label_col='entities', #specify the ner result column
               resolution_col = 'resolution'
               document_col='document' #specify the document column (default: 'document')
               )

```


#### Relation Extraction
```python
from sparknlp_display import RelationExtractionVisualizer

re_vis = RelationExtractionVisualizer()

re_vis.display(pipeline_result, #should be the results of a single example, not the complete dataframe
               relation_col = 'relations', #specify relations column
               document_col = 'document', #specify document column
               show_relations=True #display relation names on arrows (default: True)
               )

```

#### Assertion Status
```python
from sparknlp_display import AssertionVisualizer

assertion_vis = AssertionVisualizer()

assertion_vis.set_label_colors({'TREATMENT':'#008080', 'problem':'#800080'}) #set label colors by specifying hex codes

assertion_vis.display(assertion_res[0], 
                      label_col = 'entities', #specify the ner result column
                      assertion_col = 'assertion' #specify assertion column
                      document_col = 'document' #specify the document column (default: 'document')
                      )

```

