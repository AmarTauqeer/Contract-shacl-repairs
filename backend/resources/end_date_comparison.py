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
@prefix base: <http://ontologies.atb-bremen.de/smashHitCore#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <http://schema.org/> .
@prefix fibo-fbc-fe-fse: <https://spec.edmcouncil.org/fibo/ontology/FBC/FunctionalEntities/FinancialServicesEntities/> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix dpv-gdpr: <http://www.w3.org/ns/dpv-gdpr#> .
@prefix fibo-fnd-agr-ctr: <https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix gconsent: <https://w3id.org/GConsent#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix rdf4j: <http://rdf4j.org/schema/rdf4j#> .
@prefix fibo-der-dc-dma: <https://spec.edmcouncil.org/fibo/ontology/DER/DerivativesContracts/DerivativesMasterAgreements/> .
@prefix fibo-fnd-trext-reatr: <https://spec.edmcouncil.org/fibo/ontology/FND/TransactionsExt/REATransactions/> .
@prefix gn: <http://www.geonames.org/ontology#> .
@prefix dpv: <http://www.w3.org/ns/dpv#> .
@prefix consent: <http://purl.org/adaptcentre/openscience/ontologies/consent#> .
@prefix fibo-loan-loant-mloan: <https://spec.edmcouncil.org/fibo/ontology/LOAN/LoanTypes/MortgageLoans/> .
@prefix LCC: <https://www.omg.org/spec/LCC/Countries/CountryRepresentation/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix fibo-fnd-plc-loc: <https://spec.edmcouncil.org/fibo/ontology/FND/Places/Locations/> .
@prefix time: <http://www.w3.org/2006/time#> .
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix fibo-fbc-dae-dbt: <https://spec.edmcouncil.org/fibo/ontology/FBC/DebtAndEquities/Debt/> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.com/ns#> .

<http://datashapes.org/shasf/tests/expression/advanced.test.shacl>
  rdf:type owl:Ontology ;
  rdfs:label "Test of advanced features" ;
.
ex:lessThan
    a sh:SPARQLFunction ;
    rdfs:comment "Returns True if current date > end date" ;
    sh:parameter [
        sh:path ex:op1 ;
        sh:datatype xsd:dateTime ;
        sh:description "end date" ;
    ] ;
    sh:parameter [
        sh:path ex:op2 ;
        sh:datatype xsd:dateTime ;
        sh:description "current date time" ;
    ] ;
    sh:returnType xsd:boolean ;
    sh:select """
        SELECT ?result
        WHERE {
          BIND(IF(?op2 < ?op1, False, True) AS ?result) .
        }
        """ .
        
ex:ContractExpressionShape
    a sh:NodeShape ;
    sh:targetClass fibo-fnd-agr-ctr:Contract ;
    sh:expression [
        sh:message "The current date must be less than end date." ;
        ex:lessThan ([sh:path base:hasEndDate] [sh:path ex:currentDateTime]);
    ] .

'''

data_graph = '''
    @prefix base: <http://ontologies.atb-bremen.de/smashHitCore#> .
    @prefix fibo-fnd-agr-ctr: <https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix ex: <http://datashapes.org/shasf/tests/expression/advanced.test.shacl#> .

    base:contb2b_bfcff2dc-2ed3-11ed-be7d-3f8589292a29 a fibo-fnd-agr-ctr:Contract;
    base:contractType base:Written;
    base:forPurpose "data sharing between Tim and Alice";
    base:hasContractCategory base:categoryBusinessToBusiness;
    base:hasContractStatus base:statusExpired;
    base:hasEndDate "2023-09-07 17:14:32.687000+00:00"^^xsd:dateTime;
    fibo-fnd-agr-ctr:hasEffectiveDate "2022-09-07 17:14:32.687000+00:00"^^xsd:dateTime;
    ex:currentDateTime "2023-09-07 17:14:32.687000+00:00"^^xsd:dateTime;
    fibo-fnd-agr-ctr:hasExecutionDate "2022-09-07 17:14:32.687000+00:00"^^xsd:dateTime .

    base:ob_9e2bb1ce-2ed4-11ed-be7d-3f8589292a29 a base:Obligation;
    base:contractorID "base:c_729c70aa-2ed1-11ed-be7d-3f8589292a29";
    base:fulfillmentDate "2022-09-07"^^xsd:dateTime;
    base:hasEndDate "2023-09-07"^^xsd:dateTime;
    base:hasStates base:stateInvalid;
    dct:description "HaYRkfbFhvn5eerbqV6lnDckfnBQIRnACZDsYloyjteATU1bsOxH0MaJuI9K+fid/yoMOmCjBvdgQDQ2t2P5wg==";
    fibo-fnd-agr-ctr:hasExecutionDate "2022-09-07"^^xsd:dateTime .  
'''

if __name__ == "__main__":
    d = Graph().parse(data=data_graph, format="turtle")
    s = Graph().parse(data=shacl_file, format="turtle")
    conforms, report, message = validate(d, shacl_graph=s, advanced=True, debug=False)
    print(message)