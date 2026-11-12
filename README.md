# TranslatorEngineering

WORK IN PROGRESS, UPDATING FROM ARCHITECTURE TO ENGINEERING GROUP
## Process

This repository tracks the decision making for the Translator architecture.

This README documents the current strawman architecture.  Changes must be made via pull requests.   Questions or discussion around a topic that is not easily related to a specific pull request occurs in github issues.

## Definitions

  * Message: A Message object as defined in the Translator Reasoner API [here](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L161)
  * KP (Knowledge Provider): a Translator software component, not a project team
  * ARA (Automated Relay Agent): a Translator software component, not a project team
  * KS (Knowledge Source): a non-Translator source of information that can be ingested to produce a KP.

## Architecture Principles

1. The goal is to create a single integrated product from federated services and data
1. Which components communicate with one another?
    1. ARS broadcasts query (Message) to one or more ARAs
    1. ARAs respond to ARS with Message
    1. ARA sends query messages to KPs
    1. KPs respond to ARAs with Message
1. Interfaces:
   1. All communication between the ARS and ARAs conforms to the ReasonerAPI Message spec
   1. KP can expose their information using these methods:
      1. ReasonerAPI Message
      1. Any SmartAPI-annotated interface
      1. A file dump conforming to KGX standards
   1. The Translator consortium will develop tools to automatically 
      1. proxy ReasonerAPI calls to smartAPI calls and 
      1. deploy ReasonerAPIs of KGX file dumps 
   1. Subsequent requirements on KPs in this document will specify their application to ReasonerAPI, SmartAPI, and/or KGX interfaces.
1. Entities in any ReasonerAPI message (ARS/ARA or ARA/KP) or KGX file-based communication are represented using compact URIs (CURIES), which must be expandable to full IRIs using a biolink-model provided json-ld context file.  Entities returned from a non-ReasonerAPI smartAPI-registered KP must provide sufficient information in the registry to allow an automated conversion of the entity identifier to a biolink-model CURIE.
1. Node Identifiers
   1. KPs must expose machine readable information about the types of node identifiers that they consume and produce.
   1. ARAs or other integration tools such as KGX will perform node identifier equivalence translations.
   1. The consortium will produce or adopt equivalent id sets, which will be shared across Translator tools.  Multiple Translator teams will contribute expertise to these sets, but that expertise will produce centralized results.
   1. SRI will provide tools for disseminating these equivalent identifiers, drawing on the prior work of multiple Translator teams.
   1. The ARS will use these tools to normalize identifiers coming from ARAs before merging results.  Normalization will be performed with conflation.  Unconflated normalization may be implemented in the future, but it will require a query-time specification of conflation status, which will be passed to the ARAs.
1. Node Properties
   1. The consortium will produce or adopt a set of node properties.  The semantics of these properties will be defined in the biolink model.  Multiple Translator teams will contribute expertise to these properties, but that expertise will produce centralized results.
   1. The consortium will provide a central tool for disseminating these node properties.
   1. The ARS will call these tools to provide a consistent set of node properties to the UI and other clients.
1. Edge Predicates
   1. Relationships between entities (edges) have a predicate indicating the specific type of relationship between the entities.
   1. The biolink model will contain a set of predicates (_biolink predicates_) used to bridge across pre-existing predicate vocabularies
   1. The biolink model will designate a set of such vocabularies that can be mapped to biolink predicates. These vocabularies are called _biolink-mapped_.
   1. Predicates in ReasonerAPI messages and KGX files must be biolink predicates.
   1. Responses from non-ReasonerAPI smartAPI-registered KP must provide sufficient information via the registry that clients can determine the predicate as an identifier from a biolink-mapped vocabulary.
   1. As a best practice, KPs should map ingested predicates to a biolink-mapped vocabulary as precisely as possible, and rely on tools to convert these predicates into biolink predicates.
   1. The SRI will provide mapping tools to perform this conversion.
1. ARAs and KPs may both score answers (provide scores in the message); ARAs are required to score answers.
1. KPs should not call other KPs.
1. KPs that implement the Translator Reasoner API must perform the following kinds of reasoning in answering queries:
   1. Making identifiers more specific, e.g. responding to a query involving an entity with information related to a subclass of that entity. In the `knowledge_graph` portion of the response, the more-specific identifier must be present and linked to the less-specific identifier.  In the `results` portion of the response, the more-specific response node will be bound to the less-specific query node.
   1. Making categories in a query more specific. e.g. responding to a query for a biolink:NamedThing with a particular biolink:ChemicalSubstance.
   1. Making predicates more specific, e.g. responding to a query for “affects expression of” with an edge with predicate “increases expression of”.  In the response, the more specific edge must occur in the knowledge_graph portion of the response, and in individual results, that more specific edge will be bound to the less specific query edge.  Query Graph and Knowledge Graph edges need not match in either predicate or direction to be bound in an answer.
   1. Inverting symmetric predicates, e.g. if the KP contains information that A and B are correlated, then it should respond with that information whether the query is asked in the form A-[correlated_with]->B or B-[correlated_with]->A.
1. Query Modes:
   1. As described in the TRAPI specification, edges may be queried in either "lookup" or "inferred" mode.
   1. KPs and ARAs must respond to lookup queries by treating the query as an exact database match
   1. ARAs may respond to inferred mode one-hops with relevant results beyond an exact database match; KPs may also provide this capability
   1. When answering an inferred-mode query, a component must also include lookup results.
   1. inferred-mode queries must be one-hops with a single predicate.
1. ReasonerAPI best practices:
   1. When an ARA obtains multiple edges with the same subject, predicate, qualifiers, object, and original/primary source from KPs, it should represent these as a single edge in the knowledge_graph component of a ReasonerAPI message.
   1. An ARA or a KP must not combine edges unless they contain the same subject, predicate, qualifiers, object, and original/primary source.
   1. An ARA result is defined by the bindings of knowledge graph nodes to input query graph nodes.  For a given set of node bindings, there can be only a single result. Two separate results MUST NOT differ only in their edge bindings, with the same set of node bindings.
1. ARAs obtain biomedical data only via KPs (or other ARAs), not from locally-cached aggregated graphs or non-Translator data sources.
1. Aggregated graphs must be created at the consortium level and exposed as a KP.
1. Components that do not fulfill the responsibilities of KPs and ARAs can still be stand-alone elements of the architecture to provide particular functionality; such tools will use the Translator ReasonerAPI whenever possible.
1. Answer persistence will be the responsibility of the ARS.
1. A system-wide UI will (eventually) exist, and will allow users to interpret answers, and reformulate questions.
1. The SmartAPI registry will serve as a Translator Registry, and will expose programmatically accessible metadata about KPs and ARAs.
    1. All REST-Style SmartAPI KPs must be registered in the Translator Registry.
    1. All Translator Reasoner API KPs must be registered in the Translator Registry. All metadata for Translator Reasoner APIs must be available via endpoints at the service, from which it will be extracted by the SmartAPI Registry.
    1. All KGX files intended for graph transfer must be registered in the Translator Registry. All metadata for KGX files must be contained in associated metadata files and exposed via an API, which will be consumed by the SmartAPI Registry.
    1. All ARA must be registered in the Translator Registry.  The ARS will not require a separate registration.
    1. Each type of component must provide the metadata described [here](RegistryMetadata.md)
    1. Non-KP, Non-ARA components, such as normalizers, must also be registered and provide metadata appropriate to their API type.
    1. The SmartAPI Registry will provide a unified query system, returning information about all three API methods.  This query system will allow ARAs to locate the appropriate KPs.
    1. SRI will guarantee that metadata standards across the components allow such a unified query system.
    1. The SmartAPI registry will allow components to find all KPs by querying for biolink predicates. The SmartAPI registry will allow components to query by predicate from biolink-understood vocabularies, and return KPs that provide such metadata.
1. A continuous integration framework will consume metadata from the registry, and provide automated testing and reports.
1. Both KPs and ARAs should acquire and transmit provenance information to the fullest possible extent.
1. When querying and returning results with predicates, KPs and ARAs must be queried using the 'canonical' predicate (as opposed to its inverse), and must return the 'canonical' predicate.  There will be two ways to identify the 'canonical' predicate in the biolink-model: canonical translator predicates will not be tagged with the 'inverse:' attribute, and canonical predicates will be tagged with an "annotations" flag with the tag: "biolink:canonical_predicate" and value: "True".  This principle also applies to KGX files and TRAPI messages.
## Diagram

![image](https://user-images.githubusercontent.com/306971/117194943-b3f69e00-adb2-11eb-81f5-8f959d67a9b2.png)


![image](https://user-images.githubusercontent.com/306971/117195654-8827e800-adb3-11eb-88b6-68d38cd2bdeb.png)

