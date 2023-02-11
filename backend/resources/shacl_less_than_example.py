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

schema:CCVFirstScenarioShape
  a sh:NodeShape ;
  sh:targetClass fibo-fnd-agr-ctr:Contract;
  sh:property [
    sh:path base:hasEndDate ;
    sh:lessThan fibo-fnd-agr-ctr:hasEffectiveDate ;
  ] .	
'''

data_graph = '''
@prefix base: <http://ontologies.atb-bremen.de/smashHitCore#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix fibo-fnd-agr-ctr: <https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

base:contb2b_bfcff2dc-2ed3-11ed-be7d-3f8589292a29 a fibo-fnd-agr-ctr:Contract;
  base:contractID "base:contb2b_bfcff2dc-2ed3-11ed-be7d-3f8589292a29";
  base:contractType base:Written;
  base:forPurpose "data sharing between Tim and Alice";
  base:hasContractCategory base:categoryBusinessToBusiness;
  base:hasContractStatus base:statusExpired;
  base:hasEndDate "2023-09-07 17:14:32.687000+00:00"^^xsd:dateTime;
  rdf:value "2000";
  fibo-fnd-agr-ctr:hasEffectiveDate "2022-09-07 17:14:32.687000+00:00"^^xsd:dateTime;
  fibo-fnd-agr-ctr:hasExecutionDate "2022-09-07 17:14:32.687000+00:00"^^xsd:dateTime .
'''

if __name__ == "__main__":
    d = Graph().parse(data=data_graph, format="turtle")
    s = Graph().parse(data=shacl_file, format="turtle")
    conforms, report, message = validate(d, shacl_graph=s, advanced=True, debug=False)
    print(message)