import textwrap
from datetime import datetime

from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper(
    "	http://localhost:8080/rdf4j-server/repositories/shacl-shaps/statements"
)
sparql.setReturnFormat(JSON)

# gets the first 3 geological ages
# from a Geological Timescale database,
# via a SPARQL endpoint

create_date = datetime.now()
print(create_date)
insquery = textwrap.dedent("""
prefix ex: <http://example.org/ns#>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix schema: <http://schema.org/>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>
INSERT DATA {{
        ex:person rdf:type ex:Bob;
                schema:givenName "Robert";
                schema:familyName "Junior" ;
                schema:birthDate "1971-07-07"^^xsd:date ;
                schema:deathDate "1968-09-10"^^xsd:date.
                   }}       

  """)
print(insquery)
sparql.setQuery(insquery)
sparql.method = "POST"
sparql.queryType = "INSERT"
sparql.setReturnFormat('json')
result = sparql.query()
# print(result)
# sparql.setQuery("""
# PREFIX : <http://ontologies.atb-bremen.de/smashHitCore#>
# PREFIX prov: <http://www.w3.org/ns/prov#>
# PREFIX dcat: <http://www.w3.org/ns/dcat#>
# PREFIX fibo-fnd-agr-ctr: <https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/>
# PREFIX dc: <http://purl.org/dc/elements/1.1/>
# PREFIX dct: <http://purl.org/dc/terms/>
# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#
# select *
# where{
#
#    ?Contract rdf:type fibo-fnd-agr-ctr:Contract;
#                 :contractID ?contractId;
#                 :hasContractStatus ?contractStatus;
#                 :hasContractCategory ?contractCategory;
#                 dct:identifier ?consentId;
#                 :forPurpose ?purpose;
#                 :contractType ?contractType;
#                 fibo-fnd-agr-ctr:hasEffectiveDate ?effectiveDate;
#                 fibo-fnd-agr-ctr:hasExecutionDate ?executionDate;
#                 :hasEndDate ?endDate;
#                 :inMedium ?medium;
#                 dct:description ?consideration;
#                 rdf:value ?value .
#
#     #filter(?contractId="contract id") for sepecific contract
#
# }
#     """
#)

# try:
#     ret = sparql.queryAndConvert()
#     if len(ret["results"]["bindings"])>0:
#         for r in ret["results"]["bindings"]:
#             print(r)
# except Exception as e:
#     print(e)

if __name__=='__main__':
    print(result)
    # if len(ret["results"]["bindings"]) > 0:
    #     print(r['contractId'])