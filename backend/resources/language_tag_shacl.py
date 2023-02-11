"""\
A cool test that combines a bunch of SHACL-AF features, including:
SHACL Functions (implemented as SPARQL functions)
SHACL Rules
Node Expressions
Expression Constraint
"""

from pyshacl import validate
from rdflib import Graph

shacl_file = '''\
# prefix: ex
@prefix ex: <http://datashapes.org/shasf/tests/expression/advanced.test.shacl#> .
@prefix exOnt: <http://datashapes.org/shasf/tests/expression/advanced.test.ont#> .
@prefix exData: <http://datashapes.org/shasf/tests/expression/advanced.test.data#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix schema: <http://schema.org/> .
@prefix fibo-fnd-agr-ctr: <https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/> .
@prefix base: <http://ontologies.atb-bremen.de/smashHitCore#> .
<http://datashapes.org/shasf/tests/expression/advanced.test.shacl>
  rdf:type owl:Ontology ;
  rdfs:label "Test of advanced features" ;
.
schema:CCV1stScenarioShape a sh:NodeShape ;
 sh:targetClass base:CCV;
 sh:sparql [
 a sh:SPARQLConstraint ;
 sh:message "Violation occure the end date already passed." ;
 sh:select """
    SELECT $this
    WHERE {
     $this base:hasEndDate ?endDate .
     $this base:hasContractStatus ?contractStatus .
     $this base:hasStates ?state .
     BIND(xsd:dateTime(now())as ?currentDate) .
     FILTER (?state=base:stateInvalid)
    }
    """ ;
 ] .
'''

data_graph = '''

@prefix ex: <http://datashapes.org/shasf/tests/expression/advanced.test.data#> .
@prefix exOnt: <http://datashapes.org/shasf/tests/expression/advanced.test.ont#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix schema: <http://schema.org/> .
@prefix base: <http://ontologies.atb-bremen.de/smashHitCore#> .
@prefix fibo-fnd-agr-ctr: <https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix ex: <http://datashapes.org/shasf/tests/expression/advanced.test.shacl#> .
 

base:contb2b_bfcff2dc-2ed3-11ed-be7d-3f8589292a29 a base:CCV;
    base:contractType base:Written;
    base:forPurpose "data sharing between Tim and Alice";
    base:hasContractCategory base:categoryBusinessToBusiness;
    base:hasContractStatus base:statusExpired;
    base:hasEndDate "2022-09-07 17:14:32.687000+00:00"^^xsd:dateTime;
    fibo-fnd-agr-ctr:hasEffectiveDate "2022-09-07 17:14:32.687000+00:00"^^xsd:dateTime;
    fibo-fnd-agr-ctr:hasExecutionDate "2022-09-07 17:14:32.687000+00:00"^^xsd:dateTime;
    base:hasStates base:stateInvalid .
'''

if __name__ == "__main__":
    d = Graph().parse(data=data_graph, format="turtle")
    s = Graph().parse(data=shacl_file, format="turtle")
    conforms, report, message = validate(d, shacl_graph=s, advanced=True, debug=False)
    print(message)
