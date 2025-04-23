# Knowledge Graph Edge Merging


Based on discussions, it has been decided that some level of merging is necessary with the Translator. This is a proposal for the conditions underwhich knowledge graph edges can be merged. Subsequent discussions and proposals will be required to determine the necessary TRAPI schema changes so that no information is lost during merging.

## Proposal

Edges in the knowledge graph may be merged if they share the following properties:
* “subject”: The two edges must share the same subject. To facilitate this, node normalization may be required, in case two KP’s utilize different CURIE’s to refer to the same entity.
* “object”: The two edges must share the same object. To facilitate this, node normalization may be required, in case two KP’s utilize different CURIE’s to refer to the same entity.
* “predicate”: The two edges must use the same biolink predicate. Descendent predicates should not be merged with ancestral predicates.
* “qualifiers”: Any qualifiers in the candidate edges must be identical.

Additionally, certain attributes must also be the same:
* "biolink: original_knowledge_source"
OR
* "biolink: primary_knowledge_source"

All edges must have one (and only one) of these attributes listed, and to merge two edges, they must share the same value for the attribute.

If these five properties of the edges are the same, then these edges can be merged. 

We propose a hash function be used to calculate hashes using the aforementioned five properties as inputs. We could then use the calculated hash values as edge identifiers (keys) in the knowledge graph. This would require Knoweldge Providers to calculate the hash values themselves and pass them onto the ARA, and then require the ARA to not change the keys of the edges in the knowledge graph.

Say we have some hash function H and an edge e. H(e) = H(e["subject"], e["predicate"], e["object"], e["qualifiers"], e["knowledge_source"]). In the knowledge graph, we then have knowledge_graph[H(e)] = e. 

## Other Considerations

The above is the basics of how this might be done, but there are a few other aspects of this to consider. Most of these would be passed onto the relevant working groups to make the final decisions.

### Qualifiers

Qualifiers may be elevated out of edge attributes to be a new top level predicate for edges, based on recent discussiong from the TRAPI group. However, with qualifiers, a decision must be made on what qualifiers can be merged with one another, if any. The simplest solution would be to not merge any edges with different qualifiers, but that might not necessarily be the best idea. This would require investigation by the Data Modelling Working Group before a final decision can be made.

### Provenance

One major concern is how to adjust provenance to represent merged edges. Currently, the provenance is just reported as an ordered list, but this is unlikely to work with what would be much more complicated provenance for merged edges. A single edge would need to report what ARA's it came from, and what KP's the ARA had retrieved the knowledge from. As an example, say we have a query processed by the Workflow Runner. WR has a single edge retrieved from ARA_1 and ARA_2 that fulfills all of the stated requirements and can be merged. ARA_2 retrieved the edge from KP_1 and KP_2, while ARA_1 retrieved it from KP_1 and KP_3. Now, an ordered list would make it unclear which ARA retrieved the edge from which KP.

We propose that the provenance schema be changed to represent multiple provenance paths. As an initial potential solution, consider provenance represented as a directed graph. Each service could use nodes to represent knowledge source and edges for methods of use (query, consumed/contains). This would allow for the provenance information attached to a merged edge to retain multiple paths that were used to identify the edge.

Using the earlier example, we can constuct a message as such.

Both ARA_1 and ARA_2 receives this edge from KP_1:

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
      }
    }
  }
}
```

ARA_1 receives this edge from KP_2:

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
      }
    }
  }
}
```

ARA_2 receives this edge from KP_3:

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
      }
    }
  }
}
```

ARA_1 would send this edge, after adding it's own provenance information:

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
                      "method": "query"
                  }
              ]
          }
      }
    }
  }
}
```

ARA_2 would do the same:

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
      }
    }
  }
}
```

Finally, the two edges from the ARA's can be merged togather:

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
                      "method": "query"
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
      }
    }
  }
}
```

This way, the entire tree of paths taken to retrieve an edge is preserved. It should be noted that, in the example above, the keys in the provenance (p0, p1, p2, etc.) do not neccessarily have to be listed in that way, just that they must be unique. This could be a hash of the contents, or the infores id for the service. Either would be sufficient for this.

The EPC working group will have to make a final decision on how to modify proveance to accommodate this, while the TRAPI working group will need to finalize any neccessary TRAPI changes to facilitate it.

### Attributes

Although the same underyling information is represented by two equivalent mergable edges, additional information is also encoded that must be considered, because ARA's and KP's may add different attributes to an edge. This is accomplished by requiring edge attributes be merged by concatanating the lists of attributes, and removing any duplicates. Since edge attributes are encoded as sets in the trapi model, deduplication is straightforward. In this case, we say that two attributes are identical for deduplicaiton if and only if all fields of the attribute are identical.

For instance, if an ARA receives this edge from KP_1:

```json
{
  "edges": {
    "e719492": {
      "subject": "RXCUI:1544384",
      "predicate": "biolink:correlated_with",
      "object": "MONDO:0008383",
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
              "attribute_source": "infores:DP"
          },
      ],
    },
  }
}
```

And this edge from KP_2:

```json
{
  "edges": {
    "e719492": {
      "subject": "RXCUI:1544384",
      "predicate": "biolink:correlated_with",
      "object": "MONDO:0008383",
      "attributes": [
          {
              "attribute_type_id": "biolink:p_value",
              "value": 0,
              "value_type_id": "EDAM:data_1669",
              "attribute_source": "infores:DB"
          },
      ],
    },
  }
}
```

(Note that the edge identifiers are the same here, indicating that these edges are equivalent. Additionally, the attribute identifiers are also equivalent for one and not the other, indicating that the edges share an attribute.)

Then the ARA can merge these edges this way:

```json
{
  "edges": {
    "e719492": {
      "subject": "RXCUI:1544384",
      "predicate": "biolink:correlated_with",
      "object": "MONDO:0008383",
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
    },
  }
}
```

 It may make even more sense to take certain properties out of the attributes and add them as top level properties. We propose that we move provenance, knowledge_source, and qualifiers out of the attributes. 


## Justifications

### Determining Edge Equivalence

Having to look through the entire knowledge graph to determine edge equivalence would be inefficient, so instead, which is why we propose setting the edge identifier to be the hash value of the required propertoes. This would allow the ARA to check if the key is in the knowledge graph. If it isn't, then the edge is simply added to the knowledge graph. If it is, then the incoming edge can be merged with the existing edge. This would make the process far more efficient.

Another proposed option is adding an attribute that stores the hash value, but this would still require the receiving service to look through the knowledge graph and check each edge for equivalence, which still results in inefficiency. 

### Decendent Predicates

Above, we stated that decendent predicates should not be merged, but merging decendent predicates may be desirable in some cases but come at the cost of complexity. For instance, we may want to merge two edges where one has the predicate `interacts_with` and the other has `related_to`. Since `interacts_with` is a descendant of `related_to`, and based on the earlier requirements, this necessarily comes from the same underlying knowledge, these edges could be said to be equivalent. 

This does post some concerns. Edges should only be able to be merged with the direct ancestors, but this may result in collisions with other predicates. For instance, using the example above, an edge with predicate `interacts_with` could be merged with `related_to_at_instance_level` and `related_to`, but not `diagnoses` and `related_to_at_concept_level`. However, what happens when you have three edges, `interacts_with`, `diagnoses`, and `related_to`? It would me possible to merge the `related_to` edge with both of its descendants, but the descendants would not be able to be merged with one another.

Additionally, this could also prevent us from using the hash value keys as discussed above, since the hash values would be different with different predicates. Overall, we believe that it would not be advisable to merge descendant predicates, however this may warrant additional investigation by the Data Modelling Working Group.