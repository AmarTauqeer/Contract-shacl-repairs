import datetime

from core.Credentials import Credentials
from core.storage.Sparql import SPARQL
from helper.Helper import HelperContract
import textwrap
from datetime import date, datetime


class QueryEngine(Credentials, SPARQL, HelperContract):
    def __init__(self):
        super().__init__()

    def prefix(self):
        prefix = textwrap.dedent("""PREFIX : <http://ontologies.atb-bremen.de/smashHitCore#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            PREFIX dpv: <http://www.w3.org/ns/dpv#>
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX dcat: <http://www.w3.org/ns/dcat#>
            PREFIX fibo-fnd-agr-ctr: <https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/>
            PREFIX dct: <http://purl.org/dc/terms/>
            PREFIX consent: <http://purl.org/adaptcentre/openscience/ontologies/consent#>
        """)
        return prefix

    def get_all_contracts(self):
        query = textwrap.dedent("""{0}
            select * 
            where{{  
            ?Contract rdf:type fibo-fnd-agr-ctr:Contract;
                :contractID ?contractId;
                :hasContractStatus ?contractStatus;
                :hasContractCategory ?contractCategory;
                :consentID ?consentId;
                :forPurpose ?purpose;
                :contractType ?contractType;
                fibo-fnd-agr-ctr:hasEffectiveDate ?effectiveDate;
                fibo-fnd-agr-ctr:hasExecutionDate ?executionDate;
                :hasEndDate ?endDate;
                :inMedium ?medium;
                dct:description ?consideration;
                rdf:value ?value .
        }}
        """).format(self.prefix())
        return query

    def get_contract_by_contractor(self, name):
        query = textwrap.dedent("""{0}
                SELECT ?Contract   
                    WHERE {{ 
                     ?Contract rdf:type fibo-fnd-agr-ctr:Contract;
                        :contractID ?contractId;
                        :hasContractors ?contractor.
                ?contractor :hasName ?name .
                ?contractor :contractorID ?contractorId .
                ?contractor :hasPostalAddress ?address .
                ?contractor :hasEmail ?email .
                ?contractor :hasTelephone ?phone .
                ?contractor :hasCountry ?country .
                ?contractor :hasTerritory ?territory .
                ?contractor :hasCreationDate ?createDate .
                ?contractor :hasVATIN ?vat .
                    filter(?contractorId="{1}")
                }}""").format(self.prefix(), name)
        return query

    def get_contract_by_provider(self, name):
        query = textwrap.dedent("""{0}
            SELECT ?Contract   
                WHERE {{ 
                ?Contract a :contractID;
                        :ContractProvider :{1}.
            }}""").format(self.prefix(), name)
        return query

    def get_contract_by_id(self, id):
        query = textwrap.dedent("""{0}
            SELECT *   
                WHERE {{ 
                ?Contract rdf:type fibo-fnd-agr-ctr:Contract;
                :contractID ?contractId;
                :hasContractStatus ?contractStatus;
                :hasContractCategory ?contractCategory;
                :consentID ?consentId;
                :forPurpose ?purpose;
                :contractType ?contractType;
                fibo-fnd-agr-ctr:hasEffectiveDate ?effectiveDate;
                fibo-fnd-agr-ctr:hasExecutionDate ?executionDate;
                :hasEndDate ?endDate;
                :inMedium ?medium;
                dct:description ?consideration;
                rdf:value ?value .
                
                filter(?contractId="{1}") .
            }}""").format(self.prefix(), id)

        return query

    def get_contract_by_term_id(self, id):
        query = textwrap.dedent("""{0}
           SELECT *   
                WHERE {{ 
                ?Contract rdf:type fibo-fnd-agr-ctr:Contract;
                :contractID ?contractId;
                :hasTerms ?term;
                :hasContractStatus ?contractStatus;
                :hasContractCategory ?contractCategory;
                :consentID ?consentId;
                :forPurpose ?purpose;
                :contractType ?contractType;
                fibo-fnd-agr-ctr:hasEffectiveDate ?effectiveDate;
                fibo-fnd-agr-ctr:hasExecutionDate ?executionDate;
                :hasEndDate ?endDate;
                :inMedium ?medium;
                dct:description ?consideration;
                rdf:value ?value .
                
                filter(?term=:{1}) .
            }}""").format(self.prefix(), id)

        return query
    def get_contractor_by_id(self, id):
        query = textwrap.dedent("""{0}
            SELECT   ?contractorId ?name ?phone ?email ?country ?territory ?address ?vat ?companyId ?createDate ?role
                WHERE {{ 
                ?Contractor rdf:type prov:Agent;
                :contractorID ?contractorId;
                :hasName ?name;
                :hasTelephone ?phone;
                :hasEmail ?email;
                :hasCountry ?country;
                :hasTerritory ?territory;
                :hasPostalAddress ?address;
                :hasVATIN ?vat;
                :hasCompany ?companyId;
                :hasCreationDate ?createDate;
                :hasRole ?role .
                filter(?Contractor=:{1}) .
            }}""").format(self.prefix(), id)

        return query

    def get_company_by_id(self, id):
        query = textwrap.dedent("""{0}
            SELECT  ?companyId ?name ?phone ?email ?country ?territory ?address ?vat ?createDate   
                WHERE {{ 
                 ?Company a prov:Organization;
                :companyID ?companyId;
                :hasName ?name;
                :hasTelephone ?phone;
                :hasEmail ?email;
                :hasCountry ?country;
                :hasTerritory ?territory;
                :hasPostalAddress ?address ;
                :hasVATIN ?vat;
                :hasCreationDate ?createDate .
                filter(?companyId="{1}") .
            }}""").format(self.prefix(), id)

        return query

    def delete_contract_by_id(self, id):
        query = textwrap.dedent("""{0}
                delete{{?s ?p ?o}}   
                    WHERE {{ 
                    select ?s ?p ?o
                        where{{
                            ?s ?p ?o .
                            filter(?s=:{1})
                }}}}""").format(self.prefix(), id)
        # print(query)
        return query

    def delete_company_by_id(self, id):
        query = textwrap.dedent("""{0}
                delete{{?s ?p ?o}}   
                    WHERE {{ 
                    select ?s ?p ?o
                        where{{
                            ?s ?p ?o .
                            filter(?s=:{1})
                }}}}""").format(self.prefix(), id)
        # print(query)
        return query

    def delete_contractor_by_id(self, id):
        query = textwrap.dedent("""{0}
                delete{{?s ?p ?o}}   
                    WHERE {{ 
                    select ?s ?p ?o
                        where{{
                            ?s ?p ?o .
                            filter(?s=:{1})
                }}}}""").format(self.prefix(), id)
        # print(query)
        return query

    def get_all_contractors(self):
        query = textwrap.dedent("""{0}
            select ?contractorId ?companyId ?name ?phone ?email ?country ?territory ?address ?vat ?createDate ?role
            where{{  ?Contractor rdf:type prov:Agent;
                :contractorID ?contractorId;
                :hasName ?name;
                :hasTelephone ?phone;
                :hasEmail ?email;
                :hasCountry ?country;
                :hasTerritory ?territory;
                :hasPostalAddress ?address;
                :hasVATIN ?vat;
                :hasCompany ?companyId;
                :hasCreationDate ?createDate;
                :hasRole ?role .
        }}
        """).format(self.prefix())
        return query

    def get_all_companies(self):
        query = textwrap.dedent("""{0}
            select ?companyId ?name ?phone ?email ?country ?territory ?address ?vat ?createDate
            where{{  ?Company a prov:Organization;
                :companyID ?companyId;
                :hasName ?name;
                :hasTelephone ?phone;
                :hasEmail ?email;
                :hasCountry ?country;
                :hasTerritory ?territory;
                :hasPostalAddress ?address;
                :hasVATIN ?vat;
                :hasCreationDate ?createDate .
        }}
        """).format(self.prefix())
        return query

    def get_term_by_id(self, id):
        query = textwrap.dedent("""{0}
            SELECT ?termId ?termTypeId ?description ?createDate   
                WHERE {{ 
                ?Term rdf:type :TermsAndConditions;
                :termID ?termId;
                 :hasTermTypes ?termTypeId;
                dct:description ?description;
                :hasCreationDate ?createDate .
                filter(?termId="{1}") .
            }}""").format(self.prefix(), id)

        return query

    def get_term_by_obligation_id(self, id):
        query = textwrap.dedent("""{0}
                SELECT *
                WHERE {{
                ?Term rdf:type :TermsAndConditions;
                :termID ?termId;
                :hasObligations ?obligationId;
                 dct:description ?description;
                :hasCreationDate ?createDate .
                filter(?obligationId=:{1}) .
            }}""").format(self.prefix(), id)

        return query

    def get_signature_by_id(self, id):
        query = textwrap.dedent("""{0}
            SELECT ?signatureId ?signatureText ?createDate   
                WHERE {{ 
                ?Signature rdf:type :Signature;
                :signatureID ?signatureId;
                 :hasSignature ?signatureText;
                :hasCreationDate ?createDate .
                filter(?signatureId="{1}") .
            }}""").format(self.prefix(), id)

        return query

    def get_term_type_by_id(self, id):
        query = textwrap.dedent("""{0}
            SELECT ?termTypeId ?name ?description ?createDate   
                WHERE {{ 
                ?TermType rdf:type :TermTypes;
                :termTypeID ?termTypeId;
                :hasName ?name;
                dct:description ?description;
                :hasCreationDate ?createDate .
                filter(?termTypeId="{1}") .
            }}""").format(self.prefix(), id)

        return query

    def get_all_term_types(self):
        query = textwrap.dedent("""{0}
            select ?termTypeId ?name ?description ?createDate
            where{{  
                ?TermType rdf:type :TermTypes;
                :termTypeID ?termTypeId;
                :hasName ?name;
                dct:description ?description;
                :hasCreationDate ?createDate .
        }}
        """).format(self.prefix())
        return query

    def get_all_terms(self):
        query = textwrap.dedent("""{0}
            SELECT ?termId ?termTypeId ?description ?createDate   
                WHERE {{ 
                ?Term rdf:type :TermsAndConditions;
                :termID ?termId;
                 :hasTermTypes ?termTypeId;
                dct:description ?description;
                :hasCreationDate ?createDate .
        }}
        """).format(self.prefix())
        return query

    def get_all_signatures(self):
        query = textwrap.dedent("""{0}
            select ?signatureId ?signatureText ?createDate ?contractorId
            where{{   
                ?Signature rdf:type :Signature;
                :signatureID ?signatureId;
                 :hasSignature ?signatureText;
                :hasCreationDate ?createDate;
                :contractorID ?contractorId .
        }}
        """).format(self.prefix())
        return query

    def delete_term_by_id(self, id):
        query = textwrap.dedent("""{0}
                delete{{?s ?p ?o}}   
                    WHERE {{ 
                    select ?s ?p ?o
                        where{{
                            ?s ?p ?o .
                            filter(?s=:{1})
                }}}}""").format(self.prefix(), id)
        # print(query)
        return query

    def delete_contract_signature_by_id(self, id):
        query = textwrap.dedent("""{0}
                delete{{?s ?p ?o}}   
                    WHERE {{ 
                    select ?s ?p ?o
                        where{{
                            ?s ?p ?o .
                            filter(?s=:{1})
                }}}}""").format(self.prefix(), id)
        # print(query)
        return query

    def delete_term_type_by_id(self, id):
        query = textwrap.dedent("""{0}
                delete{{?s ?p ?o}}   
                    WHERE {{ 
                    select ?s ?p ?o
                        where{{
                            ?s ?p ?o .
                            filter(?s=:{1})
                }}}}""").format(self.prefix(), id)
        # print(query)
        return query

    def get_term_obligations(self, id):
        query = textwrap.dedent("""{0}
            SELECT *
                WHERE {{
                ?term rdf:type :TermsAndConditions;
                    :termID ?termId;
                    :hasCreationDate ?createDate;
                    :hasTermTypes ?termTypes;
                    dct:description ?description;
                    :hasObligations ?obl .
                ?obl :hasStates ?state .
                ?obl dct:description ?obligationDescription .
                ?obl fibo-fnd-agr-ctr:hasExecutionDate ?executionDate .
                ?obl :hasEndDate ?endDate .
                ?obl :fulfillmentDate ?fulfillmentDate .
                ?obl dct:identifier ?contractIdB2C .
                ?obl :obligationID ?obligationId .
                filter(?termId="{1}") .
            }}""").format(self.prefix(), id)

        return query

    def get_contract_terms(self, id):
        query = textwrap.dedent("""{0}
            SELECT ?contractId ?termId ?description ?createDate
                WHERE {{
                ?Contract rdf:type fibo-fnd-agr-ctr:Contract;
                    :contractID ?contractId;
                    :hasTerms ?term .
                    ?term dct:description ?description .
                    ?term :hasCreationDate ?createDate .
                    ?term :termID ?termId .
                filter(?contractId="{1}") .
            }}""").format(self.prefix(), id)
        return query

    def get_contract_signatures(self, id):
        query = textwrap.dedent("""{0}
            SELECT ?signatureId ?signatureText ?createDate ?contractorId
                WHERE {{
                 ?Contract rdf:type fibo-fnd-agr-ctr:Contract;
                    :contractID ?contractId;
                    :hasSignatures ?signature .
                    ?signature :hasSignature ?signatureText .
                    ?signature :hasCreationDate ?createDate .
                    ?signature :signatureID ?signatureId .
                    ?signature :contractorID ?contractorId .
                filter(?contractId="{1}") .
            }}""").format(self.prefix(), id)
        return query

    def get_contract_contractors(self, id):
        query = textwrap.dedent("""{0}
            SELECT *
                WHERE {{
                ?Contract rdf:type fibo-fnd-agr-ctr:Contract;
                    :contractID ?contractId;
                    :hasContractors ?contractor.
                ?contractor :hasName ?name .
                ?contractor :contractorID ?contractorId .
                ?contractor :hasPostalAddress ?address .
                ?contractor :hasEmail ?email .
                ?contractor :hasTelephone ?phone .
                ?contractor :hasCountry ?country .
                ?contractor :hasTerritory ?territory .
                ?contractor :hasCreationDate ?createDate .
                ?contractor :hasVATIN ?vat .
                filter(?contractId="{1}") .
            }}""").format(self.prefix(), id)
        return query

    def get_all_obligations(self):
        query = textwrap.dedent("""{0}
            select *
            where{{  
             ?Obligation rdf:type :Obligation;
                :obligationID ?obligationId;
                :contractorID ?contractorId;
                dct:identifier ?contractIdB2C;
                dct:description ?obligationDescription;
                fibo-fnd-agr-ctr:hasExecutionDate ?executionDate;
                :hasEndDate ?endDate;
                :fulfillmentDate ?fulfillmentDate;
                :hasStates ?state .
        }}
        """).format(self.prefix())
        return query

    def get_contract_compliance(self):
        query = textwrap.dedent("""{0}
            select *
            where{{  
            ?Obligation rdf:type :Obligation;
            :obligationID ?obligationId;
            :contractorID ?contractorId;
           :hasStates ?state;
    		dct:description ?obligationDescription;
    		fibo-fnd-agr-ctr:hasExecutionDate ?executionDate;
    		:hasEndDate ?endDate;
    		:fulfillmentDate ?fulfillmentDate .
      		
        }}
        """).format(self.prefix())
        return query

    def delete_obligation_by_id(self, id):
        query = textwrap.dedent("""{0}
                delete{{?s ?p ?o}}   
                    WHERE {{ 
                    select ?s ?p ?o
                        where{{
                            ?s ?p ?o .
                            filter(?s=:{1})
                }}}}""").format(self.prefix(), id)
        # print(query)
        return query

    def get_obligation_by_id(self, id):
        query = textwrap.dedent("""{0}
            SELECT *   
                WHERE {{ 
                ?Obligation rdf:type :Obligation;
                    :obligationID ?obligationId;
                    :contractorID ?contractorId;
                    dct:identifier ?contractIdB2C;
                    dct:description ?obligationDescription;
                    fibo-fnd-agr-ctr:hasExecutionDate ?executionDate;
                    :hasEndDate ?endDate;
                    :fulfillmentDate ?fulfillmentDate;
                    :hasStates ?state .
                filter(?obligationId="{1}") .
            }}""").format(self.prefix(), id)

        return query

    def get_obligation_identifier_by_id(self, id):
        query = textwrap.dedent("""{0}
            SELECT *   
                WHERE {{ 
                 ?Obligation rdf:type :Obligation;
                    :obligationID ?obligationId;
                    :contractorID ?contractorId;
                    :termID ?termId;
                    dct:identifier ?contractIdB2C;
                filter(?obligationId="{1}") .
            }}""").format(self.prefix(), id)

        return query

    def get_signature_by_id(self, id):
        query = textwrap.dedent("""{0}
        SELECT *   
        WHERE {{
            ?Signature rdf:type :Signature;
                       :hasCreationDate ?createDate;
                       :hasSignature ?signatureText;
                       :signatureID ?signatureId;
                       :contractorID ?contractorId .
            filter(?signatureId="{1}") .
        }}""").format(self.prefix(), id)

        return query

    def contract_update_status(self, id):
        violation_date = date.today()
        query = textwrap.dedent("""{0}
            DELETE {{?contractId :hasContractStatus :statusCreated.
                    ?contractId :hasContractStatus :statusPending.
                    ?contractId :hasContractStatus :statusRenewed.
                    ?contractId :hasContractStatus :statusUpdated.
                    ?contractId :hasContractStatus :statusSigned.}}
            INSERT {{?contractId :hasContractStatus :statusViolated.
            ?contractId :RevokedAtTime {1}.
            }}
             WHERE {{
                    ?Contract rdf:type fibo-fnd-agr-ctr:Contract;
                        :contractID ?contractId;
              FILTER(?contractId = "{2}")}}""").format(self.prefix(), '\'{}\'^^xsd:dateTime'.format(violation_date), id)

        # print(query)
        return query

    def insert_query(self, ContractId, ContractType, Purpose,
                     EffectiveDate, ExecutionDate, EndDate, Medium, ContractStatus, ContractCategory, ConsentId,
                     ConsiderationDescription, ConsiderationValue, Contractors, Terms, Signatures):
        insquery = textwrap.dedent("""{0} 
            INSERT DATA {{
            :{1} rdf:type fibo-fnd-agr-ctr:Contract;
                       :contractType :{2};
                       :forPurpose "{3}";
                        fibo-fnd-agr-ctr:hasEffectiveDate {4};
                        fibo-fnd-agr-ctr:hasExecutionDate {5};
                        :hasEndDate {6};
                        :inMedium {7};
                        :hasContractStatus :{8};
                        :hasContractCategory :{9};
                        :consentID "{10}";
                        dct:description "{11}";
                        rdf:value {12};
                         {13};
                         {14};
                         {15} ;
                         :contractID "{1}" .
                   }}       
               
          """.format(self.prefix(), ContractId, ContractType, Purpose,
                     '\'{}\'^^xsd:dateTime'.format(EffectiveDate), '\'{}\'^^xsd:dateTime'.format(ExecutionDate),
                     '\'{}\'^^xsd:dateTime'.format(EndDate), Medium, ContractStatus, ContractCategory, ConsentId,
                     ConsiderationDescription, ConsiderationValue, Contractors, Terms, Signatures))
        return insquery

    def insert_query_contractor(self, ContractorId, Name, Email, Phone, Address, Territory, Country, Role, Vat,
                                CompanyId, CreateDate):
        create_date = datetime.now()
        insquery = textwrap.dedent("""{0} 
        INSERT DATA {{
            :{1} rdf:type prov:Agent;
                        :hasName "{2}";
                        :hasEmail "{3}";
                        :hasTelephone "{4}";
                        :hasPostalAddress "{5}";
                        :hasTerritory "{6}";
                        :hasCountry "{7}";
                        :hasRole :{8} ;
                        :hasVATIN "{9}" ;
                        :hasCompany "{10}";
                        :hasCreationDate {11};
                        :contractorID "{1}" .
                   }}       
          """.format(self.prefix(), ContractorId, Name, Email, Phone, Address, Territory, Country, Role, Vat,
                     CompanyId, '\'{}\'^^xsd:dateTime'.format(create_date)))
        # print(insquery)
        return insquery

    def insert_query_company(self, CompanyId, Name, Email, Phone, Address, Territory, Country, Vat, CreateDate):
        # create_date = datetime.now()
        insquery = textwrap.dedent("""{0} 
        INSERT DATA {{
            :{1} rdf:type prov:Organization;
                        :hasName "{2}";
                        :hasEmail "{3}";
                        :hasTelephone "{4}";
                        :hasPostalAddress "{5}";
                        :hasTerritory "{6}";
                        :hasCountry "{7}";
                        :hasVATIN "{8}";
                        :hasCreationDate {9};
                        :companyID "{1}" .
                        
                   }}       
          """.format(self.prefix(), CompanyId, Name, Email, Phone, Address, Territory, Country, Vat,
                     '\'{}\'^^xsd:dateTime'.format(CreateDate)))
        return insquery

    def insert_query_term(self, TermId, TermTypeId, Obligations, Description, CreateDate):
        insquery = textwrap.dedent("""{0} 
        INSERT DATA {{
            :{1} rdf:type :TermsAndConditions;
                        :hasTermTypes "{2}";
                         {3};
                        dct:description "{4}";
                        :hasCreationDate {5};
                        :termID "{1}" .
                   }}       
          """.format(self.prefix(), TermId, TermTypeId, Obligations, Description,
                     '\'{}\'^^xsd:dateTime'.format(CreateDate)))
        return insquery

    def insert_query_term_type(self, TermTypeId, Name, Description, CreateDate):
        # create_date = datetime.now()
        insquery = textwrap.dedent("""{0} 
        INSERT DATA {{
            :{1} rdf:type :TermTypes;
                        :hasName "{2}";
                        dct:description "{3}";
                        :hasCreationDate {4};
                        :termTypeID "{1}" .
                   }}       
          """.format(self.prefix(), TermTypeId, Name, Description, '\'{}\'^^xsd:dateTime'.format(CreateDate)))
        return insquery

    def insert_query_obligation(self, ObligationId, Description, ContractorId, ContractIdB2C, State,
                                ExecutionDate, EndDate, FulfillmentDate):
        # create_date = datetime.now()
        insquery = textwrap.dedent("""{0} 
        INSERT DATA {{
            :{1} rdf:type :Obligation;
                        dct:description "{2}";
                        :contractorID "{3}";
                        dct:identifier "{4}";
                        :hasStates :{5};
                        fibo-fnd-agr-ctr:hasExecutionDate {6};
                        :hasEndDate {7};
                        :fulfillmentDate {8};
                        :obligationID "{1}" .
                   }}       
          """.format(self.prefix(), ObligationId, Description, ContractorId, ContractIdB2C, State,
                     '\'{}\'^^xsd:dateTime'.format(ExecutionDate), '\'{}\'^^xsd:dateTime'.format(EndDate),
                     '\'{}\'^^xsd:dateTime'.format(FulfillmentDate)))
        # print(insquery)
        return insquery

    def insert_query_contract_signature(self, SignatureId, ContractorId, CreateDate, Signature):
        # create_date = datetime.now()
        insquery = textwrap.dedent("""{0} 
        INSERT DATA {{
            :{1} rdf:type :Signature;
                        :contractorID "{2}";
                        :hasCreationDate {3};
                        :hasSignature "{4}";
                        :signatureID "{1}"
                   }}       
          """.format(self.prefix(), SignatureId, ContractorId, '\'{}\'^^xsd:dateTime'.format(CreateDate),
                     Signature))
        # print(insquery)
        return insquery
