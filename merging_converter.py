## Use like this: "python merging_converter.py example1.json example2.json".
## At least one TRAPI compliant json file must be passed in.
## Merged knowledge graph will be output to file "example_merged_kg.json", if "example.json" is input file.
import sys
import json

def edge_conversion(kedge):
    kedge = dict(kedge)
    ksubject = kedge.get("subject")
    kpredicate = kedge.get("predicate")
    kobject = kedge.get("object")
    kqualifiers = []
    hashing_qualifiers =[]
    ksource = None
    provenance_tree = []
    knegated = kedge.get("negated", False)
    kattributes = []
    for attribute in kedge.get("attributes"):
        if "biolink:original_knowledge_source" == attribute.get("attribute_type_id"):
            ksource = attribute["value"]
            attribute["attribute_type_id"] = "biolink:primary_knowledge_source"
            if provenance_tree:
                last = provenance_tree[len(provenance_tree) - 1]
                for i in range(len(provenance_tree) - 1, 1, -1):
                    if provenance_tree[i]["resource"] == attribute.get("attribute_source"):
                        provenance_tree[1], provenance_tree[i] = provenance_tree[i], provenance_tree[1]
                    provenance_tree[i] = provenance_tree[i - 1]
                provenance_tree[0] = {
                    "resource": attribute["value"],
                    "resource_role": attribute["attribute_type_id"]
                }
                provenance_tree[1]["retrievals"] = provenance_tree[0]["resource"]
                provenance_tree.append(last)
            else:
                provenance_tree.append({
                    "resource": attribute["value"],
                    "resource_role": attribute["attribute_type_id"]
                })
        elif "biolink:primary_knowledge_source" == attribute["attribute_type_id"]:
            ksource = attribute["value"]
            if provenance_tree:
                last = provenance_tree[len(provenance_tree) - 1]
                for i in range(len(provenance_tree) - 1, 1, -1):
                    if provenance_tree[i]["resource"] == attribute.get("attribute_source"):
                        provenance_tree[1], provenance_tree[i] = provenance_tree[i], provenance_tree[1]
                    provenance_tree[i] = provenance_tree[i - 1]
                provenance_tree[0] = {
                    "resource": attribute["value"],
                    "resource_role": attribute["attribute_type_id"]
                }
                provenance_tree[1]["retrievals"] = provenance_tree[0]["resource"]
                provenance_tree.append(last)
            else:
                provenance_tree.append({
                    "resource": attribute["value"],
                    "resource_role": attribute["attribute_type_id"]
                })
        elif attribute["attribute_type_id"] == "biolink:qualifiers":
            hashing_qualifiers.append(attribute["value"])
            kqualifiers.append(attribute)
        elif attribute["attribute_type_id"] == "biolink:aggregator_knowledge_source":
            if provenance_tree:
                check = True
                for source in provenance_tree:
                    if source["resource"] == attribute.get("attribute_source"):
                        provenance_tree.append(provenance_tree[len(provenance_tree) - 1])
                        source["retrievals"] = attribute["value"]
                        source_index = provenance_tree.index(source)
                        for i in range(len(provenance_tree) - 1, source_index + 1, -1):
                            provenance_tree[i] = provenance_tree[i - 1]
                        provenance_tree[source_index] = {
                            "resource": attribute["value"],
                            "resource_role": attribute["attribute_type_id"],
                        }
                        check = False
                        break
                if check:
                    provenance_tree.append(
                        {
                            "resource": attribute["value"],
                            "resource_role": attribute["attribute_type_id"],
                            "retrievals": [provenance_tree[len(provenance_tree) - 1]["resource"]]
                        }
                    )
            else:
                provenance_tree.append(
                    {
                        "resource": attribute["value"],
                        "resource_role": attribute["attribute_type_id"],
                    }
                )
        else:
            kattributes.append(attribute)
    edge_key = hash((ksubject, kobject, kpredicate, knegated, tuple(hashing_qualifiers), ksource))
    converted_edge = {
        "subject": ksubject,
        "predicate": kpredicate,
        "object": kpredicate,
        "negated": knegated,
        "qualifiers": kqualifiers,
        "sources": provenance_tree,
        "attributes": kattributes
    }
    return edge_key, converted_edge

def merge_edges(edge, candidate):
    for attribute in candidate["attributes"]:
        if attribute not in edge["attributes"]:
            edge["attributes"].append(attribute)
    for source in candidate["sources"]:
        if source not in edge["sources"]:
            edge["sources"].append(source)

def main(argv):
    for f in argv:
        with open(f) as file:
            message = json.load(file)
            kg = message["message"]["knowledge_graph"]
            merged_kg = {}
            for edge in kg["edges"].values():
                edge_key, converted_edge = edge_conversion(edge)
                if edge_key in merged_kg.keys():
                    merge_edges(merged_kg[edge_key], converted_edge)
                else:
                    merged_kg[edge_key] = converted_edge
        output = f.replace('.json', '_merged_kg.json')
        with open(output, "w") as output_file:
            json.dump(merged_kg, output_file)


if __name__ == "__main__":
    main(sys.argv[1:])
