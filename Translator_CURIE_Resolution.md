# Translator CURIE Resolution

This document is a discussion to review needs and requirements for a strategy and/or service to support
the resolution of [**C**ompact **U**niform **R**esource **I**dentifiers ("CURIES")](https://www.w3.org/TR/2010/NOTE-curie-20101216/)
within the NCATS Biomedical Translator knowledge management platform ("Platform") currently under development.

## Background

CURIE identifiers are a fundamental standard tool for concept identification within the Platform.
The core semantic standard of the Platform is the [Biolink Model](https://biolink.github.io/biolink-model/), 
within which mappings are made to namespaces for such CURIES which refer to external third party concepts
or ontology terms (other than the default namespace (prefix) `biolink` which is, by definition, 
defined by the contents of the Biolink Model itself, in the canonical biolink-model.yaml file).

Instances of CURIE identifiers have two component parts: their global namespace, stipulated to be
globally unique, and their object identifier, only guaranteed to be uniquely resolvable within the
given namespace.  

To ensure the global uniqueness of namespaces, they need to be defined in terms
of their full [**U**niform **R**esource **I**dentifier ("URI")](https://www.w3.org/Addressing/URL/uri-spec.html),
in accordance with global (W3C) internet standards. CURIE provide a means of concise expression
of full URI's by allowing substitution of the invariant "global" ("base URI") part of a URI with a
"compact" XML namespace prefix and colon, in front of the locally unique object identifier.

The Biolink Model (using the LinkML defined model tags and parsing software) directly supports the 
external resolution or local definition of the base URI associated with every CURIE namespace prefix,
thus enabling, in principle, the proper resolution and semantic mapping of distinct CURIE instances within the model.

## Motivation for SRI Guidelines and Service Support

Ideally, in principle, it is desirable that all instances of CURIE be simply resolvable in a web browser
or web service client by **RE**presentational **S**tate **T**ransfer (REST) access to the expanded URI
used as **U**niform **R**esource **L**ocator (URL).

In practice, simply expanding a CURIE based on the prefix URI definitions in the Biolink Model does not 
yet suffice to always resolve it, for various reasons:

### 1. Concepts that are visible on the Web but not REST URI resolvable

Although the Authority of a given concept namespace may have published some internet accessible document
describing its distinct concepts, such a document may may be structured for REST URI access to each 
distinct CURIE identified definition. An example of this within the Biolink Model are UMLS concept
definitions and concept types associated with the Semantic Medline Database.

### 2. Concepts may NOT be directly visible on the Web, but may well defined in some digital form

Although the Authority of a given collection of concepts may have a digital project document somewhere
describing those concepts, such a document is not visible for REST URI access to each distinct
concept definition. A relevant example of this scenerio within Translator project, are the "feature variable"
definitions of ICEES and COHD clinical exposure cohort data sets, which have a page of definitions
(in digital form) but no formal (CURIE) namespace, let alone, internet endpoint, where such definitions
could be automatically resolved and retrieved by web browser or web service clients.

### 3. Concepts may have been discovered by Translator curation but have no public definition

The Biolink Model currently maps CURIE namespaces introduced by various Translator teams
during the early process of knowledge curation, but such CURIE may not have a formal definition
other than their names. An example of this within the Biolink Model the GAMMA concepts from the
NCATS Translator Feasibility phase work of the ROBOKOP team.

It appears generally recognized that, given the proposed level of functionality and automation
of the Platform, that the current limitations of Platform resolution of CURIE represents an
important cross-cutting limitation of the system requiring SRI leadership to supply suitable 
strategy and, likely, service support to "solve the problem".

A secondary, but related issue, is the alignment of "equivalent concepts" between namespaces. 
CURIE resolution per say seems complementary but slightly orthogonal to the use case of the
SRI Node Normalization Service (NNS) in that once all CURIE instances may be web browser or
programmatically resolved, then they may be curated as fresh class/slot `*_mappings` slots
as concepts matching Biolink slots and classes as roughly "equivalent" concepts", and/or 
their namespaces referenced as instances of `id_prefixes`, to make them fully accessible
for NNS processing.

# Possible Strategy

T.B.A.

# Possible Service Support

(initial brainstorm...)

- don't 'reinvent the wheel' but use off-the-shelf tools:
    - **prefixcommons** or **OBO** project libraries (@cmungall to comment here...) to develop a facility for Translator local namespace prefix management.
    - use a Translator GitHub repository to host Translator namespace prefix mappings and dictionary of terms imported or curated concept definitions into such local "Translator" namespaces
    - host (at least, internally to the Platform) a CURIE resolution service which retrieves locally curated/ETL'd definitions of concepts mapped onto the Translator minted CURIE namespaces

T.B.A. _if and as needed_.

