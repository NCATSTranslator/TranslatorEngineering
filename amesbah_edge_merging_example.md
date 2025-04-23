# Edge Merging Example

The example will show an entire merged knowledge graph, as well as each step in the process. This shows an edge that was returned by three knowledge providers (KP_1, KP_2, KP_3) to two ARA's (ARA_1 and ARA_2), and then from the ARA's to the Workflow Runner (WR). In this, ARA_1 receives the edge from KP_1 and KP_2, and ARA_2 receives it from KP_1 and KP_3. Also, say ARA_1 actually contains KP_2 within it.

## KP output

This section shows the outputs of the three KP's.

### KP_1

```json
{
  "edges": {
    "e719492": {
      "subject": "RXCUI:1544384",
      "predicate": "biolink:correlated_with",
      "object": "MONDO:0008383",
      "provenance": {
          "p0": {
              "original_knowledge_source": "infores:DB"
          },
          "p1": {
              "aggregator_knowledge_source": "infores:KP_1",
              "adjacency_list": [
                  {
                      "parent": "p0",
                      "method": "consumed"
                  }
              ]
          }
      },
      "attributes": [
          {
              "attribute_type_id": "biolink:p_value",
              "value": 0,
              "value_type_id": "EDAM:data_1669",
              "attribute_source": "infores:DB"
          },
          {
              "attribute_type_id": "biolink:p_value",
              "value": 0,
              "value_type_id": "EDAM:data_0006",
              "attribute_source": "infores:DB"
          },
      ],
    }
  }
}
```

### KP_2

```json
{
  "edges": {
    "e719492": {
      "subject": "RXCUI:1544384",
      "predicate": "biolink:correlated_with",
      "object": "MONDO:0008383",
      "provenance": {
          "p0": {
              "original_knowledge_source": "infores:DB"
          },
          "p2": {
              "aggregator_knowledge_source": "infores:KP_2",
              "adjacency_list": [
                  {
                      "parent": "p0",
                      "method": "consumed"
                  }
              ]
          }
      },
      "attributes": [
          {
              "attribute_type_id": "biolink:p_value",
              "value": 0,
              "value_type_id": "EDAM:data_1669",
              "attribute_source": "infores:DB"
          },
          {
              "attribute_type_id": "biolink:p_value",
              "value": 0,
              "value_type_id": "EDAM:data_6109",
              "attribute_source": "infores:DB"
          },
      ],
    }
  }
}
```

### KP_3

```json
{
  "edges": {
    "e719492": {
      "subject": "RXCUI:1544384",
      "predicate": "biolink:correlated_with",
      "object": "MONDO:0008383",
      "provenance": {
          "p0": {
              "original_knowledge_source": "infores:DB"
          },
          "p3": {
              "aggregator_knowledge_source": "infores:KP_3",
              "adjacency_list": [
                  {
                      "parent": "p0",
                      "method": "consumed"
                  }
              ]
          }
      },
      "attributes": [
          {
              "attribute_type_id": "biolink:p_value",
              "value": 0,
              "value_type_id": "EDAM:data_6109",
              "attribute_source": "infores:DB"
          },
          {
              "attribute_type_id": "biolink:p_value",
              "value": 0,
              "value_type_id": "EDAM:data_1669",
              "attribute_source": "infores:DB"
          }
      ],
    }
  }
}
```

## ARA output

This section shows the outputs of the two ARA's.

### ARA_1

```json
{
  "edges": {
    "e719492": {
      "subject": "RXCUI:1544384",
      "predicate": "biolink:correlated_with",
      "object": "MONDO:0008383",
      "provenance": {
          "p0": {
              "original_knowledge_source": "infores:DB"
          },
          "p1": {
              "aggregator_knowledge_source": "infores:KP_1",
              "adjacency_list": [
                  {
                      "parent": "p0",
                      "method": "consumed"
                  }
              ]
          },
          "p2": {
              "aggregator_knowledge_source": "infores:KP_2",
              "adjacency_list": [
                  {
                      "parent": "p0",
                      "method": "consumed"
                  }
              ]
          },
          "p4": {
              "aggregator_knowledge_source": "infores:ARA_1",
              "adjacency_list": [
                  {
                      "parent": "p1",
                      "method": "query"
                  },
                  {
                      "parent": "p2",
                      "method": "contains"
                  }
              ]
          }
      },
      "attributes": [
          {
              "attribute_type_id": "biolink:p_value",
              "value": 0,
              "value_type_id": "EDAM:data_1669",
              "attribute_source": "infores:DB"
          },
          {
              "attribute_type_id": "biolink:p_value",
              "value": 0,
              "value_type_id": "EDAM:data_0006",
              "attribute_source": "infores:DB"
          },
          {
              "attribute_type_id": "biolink:p_value",
              "value": 0,
              "value_type_id": "EDAM:data_6109",
              "attribute_source": "infores:DB"
          },
      ],
    }
  }
}
```

### ARA_2

```json
{
  "edges": {
    "e719492": {
      "subject": "RXCUI:1544384",
      "predicate": "biolink:correlated_with",
      "object": "MONDO:0008383",
      "provenance": {
          "p0": {
              "original_knowledge_source": "infores:DB"
          },
          "p1": {
              "aggregator_knowledge_source": "infores:KP_1",
              "adjacency_list": [
                  {
                      "parent": "p0",
                      "method": "consumed"
                  }
              ]
          },
          "p3": {
              "aggregator_knowledge_source": "infores:KP_3",
              "adjacency_list": [
                  {
                      "parent": "p0",
                      "method": "consumed"
                  }
              ]
          },
          "p5": {
              "aggregator_knowledge_source": "infores:ARA_2",
              "adjacency_list": [
                  {
                      "parent": "p1",
                      "method": "query"
                  },
                  {
                      "parent": "p3",
                      "method": "query"
                  }
              ]
          }
      },
      "attributes": [
          {
              "attribute_type_id": "biolink:p_value",
              "value": 0,
              "value_type_id": "EDAM:data_1669",
              "attribute_source": "infores:DB"
          },
          {
              "attribute_type_id": "biolink:p_value",
              "value": 0,
              "value_type_id": "EDAM:data_0006",
              "attribute_source": "infores:DB"
          },
          {
              "attribute_type_id": "biolink:p_value",
              "value": 0,
              "value_type_id": "EDAM:data_6109",
              "attribute_source": "infores:DB"
          },
      ],
    }
  }
}
```

## WR

Finally, this would be the final merged output from the WR.

```json
{
  "edges": {
    "e719492": {
      "subject": "RXCUI:1544384",
      "predicate": "biolink:correlated_with",
      "object": "MONDO:0008383",
      "provenance": {
          "p0": {
              "original_knowledge_source": "infores:DB"
          },
          "p1": {
              "aggregator_knowledge_source": "infores:KP_1",
              "adjacency_list": [
                  {
                      "parent": "p0",
                      "method": "consumed"
                  }
              ]
          },
          "p2": {
              "aggregator_knowledge_source": "infores:KP_2",
              "adjacency_list": [
                  {
                      "parent": "p0",
                      "method": "consumed"
                  }
              ]
          },
          "p3": {
              "aggregator_knowledge_source": "infores:KP_3",
              "adjacency_list": [
                  {
                      "parent": "p0",
                      "method": "consumed"
                  }
              ]
          },
          "p4": {
              "aggregator_knowledge_source": "infores:ARA_1",
              "adjacency_list": [
                  {
                      "parent": "p1",
                      "method": "query"
                  },
                  {
                      "parent": "p2",
                      "method": "contains"
                  }
              ]
          },
          "p5": {
              "aggregator_knowledge_source": "infores:ARA_2",
              "adjacency_list": [
                  {
                      "parent": "p1",
                      "method": "query"
                  },
                  {
                      "parent": "p3",
                      "method": "query"
                  }
              ]
          },
          "p6": {
              "aggregator_knowledge_source": "infores:WR",
              "adjacency_list": [
                  {
                      "parent": "p4",
                      "method": "query"
                  },
                  {
                      "parent": "p5",
                      "method": "query"
                  }
              ]
          }
      },
      "attributes": [
          {
              "attribute_type_id": "biolink:p_value",
              "value": 0,
              "value_type_id": "EDAM:data_1669",
              "attribute_source": "infores:DB"
          },
          {
              "attribute_type_id": "biolink:p_value",
              "value": 0,
              "value_type_id": "EDAM:data_0006",
              "attribute_source": "infores:DB"
          },
          {
              "attribute_type_id": "biolink:p_value",
              "value": 0,
              "value_type_id": "EDAM:data_6109",
              "attribute_source": "infores:DB"
          },
      ],
    }
  }
}
```