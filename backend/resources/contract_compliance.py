import json

import requests
from requests.structures import CaseInsensitiveDict

from resources.contract_obligation import GetObligationIdentifierById, ObligationStatusUpdateById, \
    GetObligationByTermId, ObligationById
from resources.contract_terms import TermById, TermByObligationId, GetContractTerms
from resources.contractors import ContractorById
from resources.contracts import ContractByContractId, ContractStatusUpdateById, GetContractContractors, Contracts, \
    ContractByContractor, ContractByTermId
from resources.imports import *
from resources.schemas import *
from mailer import Mailer

from datetime import datetime, date


class GetContractCompliance(MethodResource, Resource):
    @doc(description='Contract Compliance', tags=['Contract Compliance'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="compliance", termID=None,
                                   contractRequester=None, contractProvider=None, ))

        print('scheduler')
        # self.get_consent_state("test")
        obligatons = response["results"]['bindings']
        # current_data = date(2024, 4, 5)
        current_data = date.today()

        for x in obligatons:
            obligation_id = x["obligationId"]["value"]
            edate = x["endDate"]["value"][:10]
            obl_state = x["state"]["value"][45:]
            obl_desc = x["obligationDescription"]["value"]
            contractor_id = x["contractorId"]["value"][45:]


            #  get terms
            get_term = TermByObligationId.get(self, obligation_id)
            my_json = get_term.data.decode('utf-8')
            data = json.loads(my_json)
            term_id = data['termId']

            contract = ContractByTermId.get(self, term_id)
            contract_data = contract.json

            contract_id = contract_data["contractId"]
            contract_status = contract_data["contractStatus"]

            b2c = b2c_contract_status = b2c_contract_id = ""
            b2b = b2b_contract_status = b2b_contract_id = ""

            # get contract status
            if 'contb2c_' in contract_id:
                b2c = contract_id
            if 'contb2b_' in contract_id:
                b2b = contract_id

            consent = "empty"
            date_time_str = edate
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d').date()

            b2c_data = ContractByContractId.get(self, b2c)
            b2c_data = b2c_data.json

            if b2c_data != 'No data found for this ID':
                consent = b2c_data['consentId']

            b2b_data = ContractByContractId.get(self, b2b)
            b2b_data = b2b_data.json

            if b2b_data != 'No data found for this ID':
                consent = b2b_data['consentId']

            if consent == "string" or consent == "":
                consent = "empty"

            # handle single business to business contract
            if b2b != "" and consent == "empty":
                print(f'b2b without consent')

                b2b_data = ContractByContractId.get(self, b2b)
                b2b_data = b2b_data.json
                b2b_contract_status = b2b_data["contractStatus"]
                b2b_contract_id = b2b_data["contractId"]
                # print(b2c_data)
                if current_data >= date_time_obj and obl_state == 'statePending' \
                        and b2b_contract_status not in (
                        'statusViolated', 'statusTerminated', 'statusExpired'):
                    ContractStatusUpdateById.get(self, b2b_contract_id, 'statusViolated')
                    ObligationStatusUpdateById.get(self, id, 'stateViolated')
                    self.send_email('violation', b2b, obl_desc, obligation_id)

            if b2c_data != 'No data found for this ID':
                b2c_contract_status = b2c_data["contractStatus"]
                b2c_contract_id = b2c_data["contractId"]

            # handle business to consumer and business to business contract based on consent
            if b2c != "" and b2b != "" and consent != "empty":
                print(f'b2c, b2b  with consent')

                b2b_data = ContractByContractId.get(self, b2b)
                b2b_data = b2b_data.json
                b2b_contract_status = b2b_data["contractStatus"]
                b2b_contract_id = b2b_data["contractId"]

                # print(b2c_data)
                consent_id = b2c_data["consentId"]

                consent_state = self.get_consent_state(consent_id)
                # consent based status
                if consent_state in ['Invalid', 'Expired'] and b2b_contract_status \
                        not in ('statusViolated', 'statusTerminated', 'statusExpired'):
                    print('if')
                    # update b2b contract status
                    ContractStatusUpdateById.get(self, b2b_contract_id, 'statusExpired')
                    # update b2b obligation
                    ObligationStatusUpdateById.get(self, obligation_id, 'stateInvalid')
                    self.send_email('expire', b2b_contract_id, obl_desc, obligation_id)
                else:
                    # current_data = date(2023, 4, 24)
                    if current_data >= date_time_obj and obl_state == 'statePending' \
                            and b2b_contract_status not in (
                            'statusViolated', 'statusTerminated', 'statusExpired'):
                        # print('violation')
                        ContractStatusUpdateById.get(self, b2b_contract_id, 'statusViolated')
                        ObligationStatusUpdateById.get(self, obligation_id, 'stateViolated')
                        self.send_email('violation', b2b_contract_id, obl_desc, obligation_id)

            # handle single business to consumer contract based on consent
            elif b2c != "" and consent != "empty":
                print(f'b2c single with consent')

                # print(b2c_data)
                consent_id = b2c_data["consentId"]
                consent_state = self.get_consent_state(consent_id)

                if consent_state in ['Invalid', 'Expired'] and b2c_contract_status \
                        not in ('statusViolated', 'statusTerminated', 'statusExpired'):
                    # update contract status
                    ContractStatusUpdateById.get(self, b2c_contract_id, 'statusExpired')
                    # update b2b obligation
                    ObligationStatusUpdateById.get(self, obligation_id, 'stateInvalid')
                    self.send_email('expire', b2c, obl_desc, obligation_id)
                else:
                    # current_data = date(2023, 4, 24)
                    if current_data >= date_time_obj and obl_state == 'statePending' \
                            and b2c_contract_status not in (
                            'statusViolated', 'statusTerminated', 'statusExpired'):
                        ContractStatusUpdateById.get(self, b2c_contract_id, 'statusViolated')
                        ObligationStatusUpdateById.get(self, id, 'stateViolated')
                        self.send_email('violation', b2c, obl_desc, obligation_id)

            # handle single business to consumer contract
            elif b2c != "" and consent == "empty":
                print(f'b2c without consent')

                # print(b2c_data)
                if current_data >= date_time_obj and obl_state == 'statePending' \
                        and b2c_contract_status not in (
                        'statusViolated', 'statusTerminated', 'statusExpired'):
                    ContractStatusUpdateById.get(self, b2c_contract_id, 'statusViolated')
                    ObligationStatusUpdateById.get(self, id, 'stateViolated')
                    self.send_email('violation', b2c, obl_desc, obligation_id)

        """
            if the consent expires and data controller still use that cosent
        """
        # list contracts
        all_contracts_data = Contracts.get(self)
        all_contracts_data = all_contracts_data.json

        if all_contracts_data != 'No record is found':

            for b in all_contracts_data:

                contract = b['contractId']
                # list of b2b contracts
                if 'contb2b_' in contract:
                    c_obj = ContractByContractId.get(self, contract)
                    c_obj = c_obj.json
                    contract_status = c_obj['contractStatus']
                    contract_id = c_obj['contractId']
                    terms = GetContractTerms.get(self, contract_id)
                    my_json = terms.data.decode('utf-8')
                    terms_data = json.loads(my_json)
                    for term in terms_data:
                        obligations = term['obligations']
                        for ob in obligations:
                            print(ob)
                            obl = ObligationById.get(self, ob)
                            my_json = obl.data.decode('utf-8')
                            decoded_data = json.loads(my_json)
                            if decoded_data != 'No record found for this ID':
                                obl_data = decoded_data
                                for o in obl_data:
                                    contractIdB2C = o['contractIdB2C']
                                    if contractIdB2C != '':
                                        c_obj1 = ContractByContractId.get(self, contractIdB2C)
                                        c_obj1 = c_obj1.json
                                        consent_id = c_obj1['consentId']
                                        if consent_id != '':
                                            consent_state = self.get_consent_state(consent_id)
                                            if consent_state == 'Invalid' and contract_status not in ['statusExpired',
                                                                                                      'statusTerminated']:


                                                contractors = GetContractContractors.get(self, contract_id)
                                                contractors = contractors.json
                                                for con in contractors:
                                                    contractor = ContractorById.get(self, con['contractorId'])
                                                    contractor = contractor.json
                                                    email = contractor['email']
                                                    message = 'The consent = ' + str(
                                                        consent_id) + ' ' + 'has been expired/invalid but the contract =' \
                                                              + contract + ' is still running based on this consent '

                                                    mail = Mailer(email=os.environ.get('MAIL_USERNAME'),
                                                                  password=os.environ.get('MAIL_PASSWORD'))
                                                    mail.settings(provider=mail.MICROSOFT)
                                                    mail.send(receiver=email,
                                                              subject='Violation/Expiration of Obligation',
                                                              message=message)

        return 'Success'

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

    def get_consent_state(self, consentid):
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

        url_get_consent_data = "http://138.232.18.138:5003/query/{0}/consent".format(consent_id)
        headers["Authorization"] = "Bearer " + token

        resp = requests.get(url_get_consent_data, headers=headers)
        result = resp.json()
        a = result["message"]
        a = eval(a)
        consent_data = a['consent_data']
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
