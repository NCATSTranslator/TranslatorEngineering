# Performance Refactor Proposal

This document describes (at a high level) the proposed refactoring of Translator at the start of the Performance phase. This does not describe all details of the refactoring, which will be jointly developed over time through discussions and decisions in the relevant working groups.
The goal of this document is to establish a broad agreed-upon framework into which those details will fit, and codify the discussions at the February 2025 Relay.

The plan to to complete the refactoring by Feb 28, 2026.

There are several advantages to the proposed refactoring:
* Increased query speed achieved by careful and centralized implementation of the query interface.
* Increased software maintenance achieved by the collection of common tasks into single units of code.
* Increased evolution of the Translator system, similarly achieved by the collection of common tasks into single units of code.
* Decreased testing and deployment costs acheived through simplificiation of the system and reduction in number of components.
* Increased data quality acheived through common ingests.

## ARAs to Shepherd

* We will create a shared platform for ARA implementation
* The name of this platform is Shepherd
* The workflow core of Shepherd will be implemented in python
* Individual Shepherd operations may vary in their implementation language or technology, though python is preferred
* Shepherd will be implemented as a workflow engine with shared operation components
* Technical decisions related to the implementation of workflows are explicitly outside the scope of this document
* ARAs will maintain individual TRAPI endpoints addressable at individual URLs, even if the underlying implementation is shared.
* Best effort will be made to reimplement ARAGORN, BTE, and ARAX to Shepherd.
* ARS will continue to exist and does not require modifications based on the outlined plan for Shepherd.
* It is possible to host non-Shepherd ARAs if desired and this PR does not exclude the possibility.
* Shepherd will access Translator knowledge providers via the Retriever interface.
* ARAs can access ARA-specific data sources such as databases directly.
* Shepherd will pass the query to each ARA without modification.

## KPS to Retriever / DogPark

* Translator will implement a common data platform called DogPark.
* The details of DogPark implementation including data architecture, database implementation, tiers, or interfaces are outside the scope of this document.
* DogPark will host all Translator Knowledge Providers (KPs).
* Translator will implement a query interface to DogPark called Retriever.
* Retriever will implement at least an async TRAPI interface, and may develop further interfaces in the future.
* The TRAPI Interface will respond to lookup queries, and will implement all Phase 2 requirements of TRAPI KPs such as subclass inference, canonical edge directions, and others as described in the TranslatorArchitecture document.
* Retriever will also provide API access to external resources.
* The detailed implementation of Retriever is outside the scope of this document.
* Translator will coordinate knowledge ingests to reduce redundancy and modeling variation.
* Translator will move towards a common declarative ingest pipeline.
* Some ingests will require non-declarative ingests or generate new knowledge via analysis, which will require special handling outside of the common ingest pipeline.
* Data hosted in DogPark will be pre-normalized to the extent possible, but this document does not specify the details of normalization, which will be agreed upon at a later date.

## Node Components

* Several components do not contain edges, but only nodes. At present, these components include (but are not necessarily limited to) SRI Node Normalizer, KG2 Node Synonymizer, Node Annotator, and Name Resolver.
* These components will agree on a common set of identifier equivalences to be used across all tools, and in the normalization of DogPark knowledge.
* Node Normalizer will implement refactorings to reduce its cost and may reduce performance to acheive this goal
* Node Normalizer will however still be used at query time to provide canonical identifiers for external API sources.
* Translator will investigate the merger of any or all of these tools based upon their use in the proposed architecture, but this document does not specify any decision.
