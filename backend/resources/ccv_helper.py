from datetime import datetime
import os

from flask_apispec import MethodResource
from flask_restful import Resource
from mailer import Mailer
from pyshacl import validate
from rdflib import Graph
from requests.structures import CaseInsensitiveDict

import textwrap
import rootpath
import requests

from resources.contracts import GetContractContractors

# get shacl shapes
main_directory = f"{rootpath.detect()}/resources/data-graphs-files"
file_name = '/ccv_shacl_shapes.ttl'
complete_path = main_directory + file_name
file = open(complete_path, 'r')
content = file.read()
shapes = content
file.close()
shacl_file = shapes


def prefix():
    prefix = textwrap.dedent("""@prefix base: <http://ontologies.atb-bremen.de/smashHitCore#> .
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

    """)
    return prefix


class CCVHelper(MethodResource, Resource):

    def shacl_validation(self, contid=None, contstatus=None, contcategory=None, conttype=None, oblstate=None,
                         consstate=None, purpose=None, enddate=None, exedate=None, effecdate=None, scenario=None,
                         currentdate=None):
        if scenario == "ccv_fourth_scenario":
            data_graph = """
                            {0}
                            base:{1} a base:CCVFourth;
                            base:contractType base:{2};
                            base:forPurpose "{3}";
                            base:hasContractCategory base:{4};
                            base:hasContractStatus base:{5};
                            base:hasEndDate "{6}"^^xsd:dateTime;
                            fibo-fnd-agr-ctr:hasEffectiveDate "{7}"^^xsd:dateTime;
                            fibo-fnd-agr-ctr:hasExecutionDate "{8}"^^xsd:dateTime ;
                            base:hasStates base:{9};
                            base:currentDateTime "{10}"^^xsd:dateTime .
                            """.format(prefix(), contid, conttype, purpose, contcategory, contstatus,
                                       enddate, effecdate, exedate, oblstate, currentdate)
            # print(data_graph)
            ## create data graph file for validation
            main_directory = f"{rootpath.detect()}/resources/data-graphs-files"
            file_name = '/ccv_fourth_scenario.ttl'
            complete_path = main_directory + file_name
            with open(complete_path, 'w') as fp:
                fp.write(data_graph)
                pass
            # print(os.path.isfile(complete_path))
            # print(b2c_data)

            d = Graph().parse(data=data_graph, format="turtle")
            s = Graph().parse(data=shacl_file, format="turtle")
            conforms, report, message = validate(d, shacl_graph=s, advanced=True, debug=False)
            print(message)
            violation_data = {
                'ccv_fourth_scenario': message
            }

            return violation_data
        elif scenario == "ccv_third_else_part_scenario":

            data_graph = """
                            {0}
                            base:{1} a base:CCVThirdElse;
                            base:contractType base:{2};
                            base:forPurpose "{3}";
                            base:hasContractCategory base:{4};
                            base:hasContractStatus base:{5};
                            base:hasEndDate "{6}"^^xsd:dateTime;
                            fibo-fnd-agr-ctr:hasEffectiveDate "{7}"^^xsd:dateTime;
                            fibo-fnd-agr-ctr:hasExecutionDate "{8}"^^xsd:dateTime;
                            base:hasStates base:{9};
                            base:consentState "{10}";
                            base:currentDateTime "{11}"^^xsd:dateTime .
                            """.format(prefix(), contid, conttype, purpose, contcategory, contstatus,
                                       enddate,
                                       effecdate, exedate, oblstate, consstate, currentdate)

            # print(data_graph)
            ## create data graph file for validation
            main_directory = f"{rootpath.detect()}/resources/data-graphs-files"
            file_name = '/ccv_third_else_part_scenario.ttl'
            complete_path = main_directory + file_name
            with open(complete_path, 'w') as fp:
                fp.write(data_graph)
                pass
            # print(os.path.isfile(complete_path))
            # print(b2c_data)

            d = Graph().parse(data=data_graph, format="turtle")
            s = Graph().parse(data=shacl_file, format="turtle")
            conforms, report, message = validate(d, shacl_graph=s, advanced=True, debug=False)
            violation_data = {
                'ccv_third_else_part_scenario': message
            }
            return violation_data
        elif scenario == "ccv_third_if_part_scenario":
            data_graph = """
                            {0}
                            base:{1} a base:CCVThirdIf;
                            base:contractType base:{2};
                            base:forPurpose "{3}";
                            base:hasContractCategory base:{4};
                            base:hasContractStatus base:{5};
                            base:hasEndDate "{6}"^^xsd:dateTime;
                            fibo-fnd-agr-ctr:hasEffectiveDate "{7}"^^xsd:dateTime;
                            fibo-fnd-agr-ctr:hasExecutionDate "{8}"^^xsd:dateTime;
                            base:hasStates base:{9};
                            base:consentState "{10}";
                            base:currentDateTime "{11}"^^xsd:dateTime .
                            """.format(prefix(), contid, conttype, purpose, contcategory, contstatus,
                                       enddate,
                                       effecdate, exedate, oblstate, consstate, currentdate)

            # print(data_graph)
            ## create data graph file for validation
            main_directory = f"{rootpath.detect()}/resources/data-graphs-files"
            file_name = '/ccv_third_if_part_scenario.ttl'
            complete_path = main_directory + file_name
            with open(complete_path, 'w') as fp:
                fp.write(data_graph)
                pass
            # print(os.path.isfile(complete_path))
            # print(b2c_data)

            d = Graph().parse(data=data_graph, format="turtle")
            s = Graph().parse(data=shacl_file, format="turtle")
            conforms, report, message = validate(d, shacl_graph=s, advanced=True, debug=False)
            violation_data = {
                'ccv_third_if_part_scenario': message
            }
            return violation_data
        elif scenario == "ccv_second_scenario":
            data_graph = """
                            {0}
                            base:{1} a base:CCV2nd;
                            base:contractType base:{2};
                            base:forPurpose "{3}";
                            base:hasContractCategory base:{4};
                            base:hasContractStatus base:{5};
                            base:hasEndDate "{6}"^^xsd:dateTime;
                            fibo-fnd-agr-ctr:hasEffectiveDate "{7}"^^xsd:dateTime;
                            fibo-fnd-agr-ctr:hasExecutionDate "{8}"^^xsd:dateTime ;
                            base:hasStates base:{9};
                            base:consentState "{10}";
                            base:currentDateTime "{11}"^^xsd:dateTime .

                            """.format(prefix(), contid, conttype, purpose, contcategory, contstatus,
                                       enddate, effecdate, exedate, oblstate, consstate, currentdate)

            # print(data_graph)
            ## create data graph file for validation
            main_directory = f"{rootpath.detect()}/resources/data-graphs-files"
            file_name = '/ccv_second_scenario.ttl'
            complete_path = main_directory + file_name
            with open(complete_path, 'w') as fp:
                fp.write(data_graph)
                pass
            # print(os.path.isfile(complete_path))
            # print(b2c_data)

            d = Graph().parse(data=data_graph, format="turtle")
            s = Graph().parse(data=shacl_file, format="turtle")
            conforms, report, message = validate(d, shacl_graph=s, advanced=True, debug=False)
            violation_data = {
                'ccv_second_scenario': message
            }
            return violation_data
        elif scenario == "ccv_first_scenario":
            data_graph = """
            {0}
            base:{1} a base:CCV1st;
            base:contractType base:{2};
            base:forPurpose "{3}";
            base:hasContractCategory base:{4};
            base:hasContractStatus base:{5};
            base:hasEndDate "{6}"^^xsd:dateTime;
            fibo-fnd-agr-ctr:hasEffectiveDate "{7}"^^xsd:dateTime;
            fibo-fnd-agr-ctr:hasExecutionDate "{8}"^^xsd:dateTime ;
            base:hasStates base:{9};
            base:currentDateTime "{10}"^^xsd:dateTime .

            """.format(prefix(), contid, conttype, purpose, contcategory, contstatus, enddate,
                       effecdate, exedate, oblstate, currentdate)

            # print(data_graph)
            ## create data graph file for validation
            main_directory = f"{rootpath.detect()}/resources/data-graphs-files"
            file_name = '/ccv_first_scenario.ttl'
            complete_path = main_directory + file_name
            with open(complete_path, 'w') as fp:
                fp.write(data_graph)
                pass
            # print(os.path.isfile(complete_path))
            # print(b2c_data)

            d = Graph().parse(data=data_graph, format="turtle")
            s = Graph().parse(data=shacl_file, format="turtle")
            conforms, report, message = validate(d, shacl_graph=s, advanced=True, debug=False)
            violation_data = {
                'ccv_first_scenario': message
            }
            return violation_data
        elif scenario == "ccv_fifth_scenario":
            data_graph = """
            {0}
            base:{1} a base:CCVFifth;
            base:hasContractStatus base:{2};
            base:consentStates "{3}";
            base:currentDateTime "{4}"^^xsd:dateTime .

            """.format(prefix(), contid, contstatus, consstate, currentdate)

            # print(data_graph)
            ## create data graph file for validation
            main_directory = f"{rootpath.detect()}/resources/data-graphs-files"
            file_name = '/ccv_fifth_scenario.ttl'
            complete_path = main_directory + file_name
            with open(complete_path, 'w') as fp:
                fp.write(data_graph)
                pass
            # print(os.path.isfile(complete_path))
            # print(b2c_data)

            d = Graph().parse(data=data_graph, format="turtle")
            s = Graph().parse(data=shacl_file, format="turtle")
            conforms, report, message = validate(d, shacl_graph=s, advanced=True, debug=False)
            violation_data = {
                'consent_expired_contract_still_running_violoations': message
            }
            return violation_data

    def get_consent_state(self, consentid):
        consent_state='Invalid'
        # need credential for extracting information of consents
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"

        token = ""
        consent_id = consentid
        # consent_id = "ASFASDF23421"
        # for test
        data = {
            'username': os.getenv("username"),
            'password': os.getenv("pass"),
        }

        url_get_login = "http://138.232.18.138:5003/jwt/login/"
        resp1 = requests.post(url_get_login, headers=headers, json=data)
        token = resp1.json()['access_token']
        print(f'token={token}')

        url_get_consent_data = "http://138.232.18.138:5003/query/{0}/consent".format(consent_id)
        headers["Authorization"] = "Bearer " + token

        resp = requests.get(url_get_consent_data, headers=headers)
        result = resp.json()
        a = result["message"]
        a = eval(a)
        consent_data = a['consent_data']
        # print(f"consent data= {consent_data}")
        if consent_data:
            # print(consent_data)
            data_provider = consent_data[consent_id][0]['DataProvider']
            data_controller = consent_data[consent_id][1]['DataProcessorController']
            status = consent_data[consent_id][2]['status']

            # status=a.rfind('GRANTED')
            if status == 'GRANTED':
                consent_state = 'Valid'
            else:
                consent_state = 'Invalid'
            # print(consent_state)
        return consent_state

    def send_email(self, type, contract_id, obl_desc, obligation_id):
        # Email to contractors in case of violation
        message_violation_expiration = ''

        if type == 'violation':
            message_violation_expiration = 'has been violated'
        else:
            message_violation_expiration = 'has been expired'

        message = 'In contract id = ' + str(
            contract_id) + ' ' + obl_desc + ' with obligation id ' + obligation_id + \
                  ' ' + message_violation_expiration
        # get contract contractors
        res = GetContractContractors.get(self, contract_id)
        contractors = res.json
        if contractors != 'No record found for this ID':
            for c in contractors:
                email = c['email']
                mail = Mailer(email=os.environ.get('MAIL_USERNAME'), password=os.environ.get('MAIL_PASSWORD'))
                mail.settings(provider=mail.MICROSOFT)
                mail.send(receiver=email, subject='Violation/Expiration of Obligation', message=message)

    def iso_date_conversion(self, date):
        date_time_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        iso_date = date_time_obj.isoformat()
        return iso_date
