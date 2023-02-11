import json
import rootpath

import requests
from requests.structures import CaseInsensitiveDict

from resources.contract_obligation import GetObligationIdentifierById, ObligationStatusUpdateById, \
    GetObligationByTermId, ObligationById
from resources.contract_terms import TermById, TermByObligationId, GetContractTerms
from resources.contractors import ContractorById
from resources.contracts import ContractByContractId, ContractStatusUpdateById, GetContractContractors, Contracts, \
    ContractByContractor, ContractByTermId

from resources.ccv_helper import CCVHelper

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

        obligatons = response["results"]['bindings']
        current_datetime=str(datetime.now())
        current_date_time = CCVHelper.iso_date_conversion(self, current_datetime[:19])

        print(f"current date = {current_date_time}")
        # array for violation message
        all_violation_messages = []

        # loop over all obligations
        for x in obligatons:
            obligation_id = x["obligationId"]["value"]
            obligation_edate = x["endDate"]["value"][:19]
            obl_state = x["state"]["value"][45:]
            obl_desc = x["obligationDescription"]["value"]

            #  get terms
            get_term = TermByObligationId.get(self, obligation_id)
            my_json = get_term.data.decode('utf-8')
            data = json.loads(my_json)
            term_id = data['termId']

            # get contract by term
            contract = ContractByTermId.get(self, term_id)
            contract_data = contract.json
            contract_id = contract_data["contractId"]

            # initialize b2c data, b2b data, status and id
            b2c = b2c_contract_status = b2c_contract_id = ""
            b2b = b2b_contract_status = b2b_contract_id = ""

            # initialize consent state
            consent = "empty"
            # consent="2e0c2cc4bc0c4e1b"

            # check the contract b2c or b2b
            if 'contb2c_' in contract_id:
                b2c = contract_id
            if 'contb2b_' in contract_id:
                b2b = contract_id

            # convert obligation end date time to date
            date_time_obj=CCVHelper.iso_date_conversion(self, obligation_edate)

            # get b2c contract
            b2c_data = ContractByContractId.get(self, b2c)
            b2c_data = b2c_data.json

            # get consent id if contract is b2c
            if b2c_data != 'No data found for this ID':
                consent = b2c_data['consentId']

            # get b2b contract
            b2b_data = ContractByContractId.get(self, b2b)
            b2b_data = b2b_data.json

            if b2b_data != 'No data found for this ID':
                consent = b2b_data['consentId']
                b2b_contract_id = b2b_data["contractId"]
                b2b_contract_status = b2b_data["contractStatus"]

            if consent == "string" or consent == "":
                consent = "empty"

            # handle single business to business contract (first scenario)
            if b2b != "" and consent == "empty":
                print(f'b2b without consent')

                # make shacl validation
                scenario = "ccv_first_scenario"
                iso_date_b2b_edate = CCVHelper.iso_date_conversion(self,b2b_data['endDate'][:19])
                iso_date_b2b_exdate = CCVHelper.iso_date_conversion(self,b2b_data['executionDate'][:19])
                iso_date_b2b_effdate = CCVHelper.iso_date_conversion(self,b2b_data['effectiveDate'][:19])
                # print(iso_date_b2b_edate)

                all_violation_messages.append(
                    CCVHelper.shacl_validation(self, scenario=scenario, contid=b2b_contract_id,
                                               conttype=b2b_data['contractType'],
                                               purpose=b2b_data['purpose'], contcategory=b2b_data['contractCategory'],
                                               contstatus=b2b_contract_status, enddate=iso_date_b2b_edate,
                                               effecdate=iso_date_b2b_effdate, exedate=iso_date_b2b_exdate,
                                               oblstate=obl_state, currentdate=current_date_time))

                # actual check to detect violation
                if current_date_time >= date_time_obj and obl_state == 'statePending' \
                        and b2b_contract_status not in (
                        'statusViolated', 'statusTerminated', 'statusExpired'):
                    print('b2b violation')
                    # ContractStatusUpdateById.get(self, b2b_contract_id, 'statusViolated')
                    # ObligationStatusUpdateById.get(self, id, 'stateViolated')
                    # CCVHelper.send_email(self, 'violation', b2b, obl_desc, obligation_id)

            if b2c_data != 'No data found for this ID':
                b2c_contract_id = b2c_data["contractId"]
                b2c_contract_status = b2c_data["contractStatus"]

            # handle business to consumer and business to business contract based on consent
            if b2c != "" and b2b != "" and consent != "empty":
                print(f'b2c, b2b  with consent')
                # get consent id from b2c
                consent_id = b2c_data["consentId"]

                # get consent state from automatic contacting tool (consent component)
                consent_state = CCVHelper.get_consent_state(self, consent_id)

                scenario = "ccv_second_scenario"
                iso_date_b2b_edate = CCVHelper.iso_date_conversion(self,b2b_data['endDate'][:19])
                iso_date_b2b_exdate = CCVHelper.iso_date_conversion(self,b2b_data['executionDate'][:19])
                iso_date_b2b_effdate = CCVHelper.iso_date_conversion(self,b2b_data['effectiveDate'][:19])

                all_violation_messages.append(
                    CCVHelper.shacl_validation(self, scenario=scenario, contid=b2b_contract_id,
                                               conttype=b2b_data['contractType'],
                                               purpose=b2b_data['purpose'], contcategory=b2b_data['contractCategory'],
                                               contstatus=b2b_contract_status, enddate=iso_date_b2b_edate,
                                               effecdate=iso_date_b2b_effdate, exedate=iso_date_b2b_exdate,
                                               oblstate=obl_state, consstate=consent_state, currentdate=current_date_time))

                # actual check for expiration
                if consent_state in ['Invalid', 'Expired'] and b2b_contract_status \
                        not in ('statusViolated', 'statusTerminated', 'statusExpired'):
                    print('if')
                    # update b2b contract status
                    # ContractStatusUpdateById.get(self, b2b_contract_id, 'statusExpired')
                    # update b2b obligation
                    # ObligationStatusUpdateById.get(self, obligation_id, 'stateInvalid')
                    # CCVHelper.send_email(self, 'expire', b2b_contract_id, obl_desc, obligation_id)
                else:
                    # current_date_time = date(2023, 4, 24)
                    if current_date_time >= date_time_obj and obl_state == 'statePending' \
                            and b2b_contract_status not in (
                            'statusViolated', 'statusTerminated', 'statusExpired'):
                        print('violation')
                        # ContractStatusUpdateById.get(self, b2b_contract_id, 'statusViolated')
                        # ObligationStatusUpdateById.get(self, obligation_id, 'stateViolated')
                        # CCVHelper.send_email(self, 'violation', b2b_contract_id, obl_desc, obligation_id)

            # handle single business to consumer contract based on consent
            elif b2c != "" and consent != "empty":
                print(f'b2c single with consent')

                # print(b2c_data)
                consent_id = b2c_data["consentId"]
                consent_state = CCVHelper.get_consent_state(self, consent_id)
                # print(f"consent state={consent_state}")
                scenario = "ccv_third_if_part_scenario"

                iso_date_b2c_edate = CCVHelper.iso_date_conversion(self,b2c_data['endDate'][:19])
                iso_date_b2c_exdate = CCVHelper.iso_date_conversion(self,b2c_data['executionDate'][:19])
                iso_date_b2c_effdate = CCVHelper.iso_date_conversion(self,b2c_data['effectiveDate'][:19])

                all_violation_messages.append(
                    CCVHelper.shacl_validation(self, scenario=scenario, contid=b2c_contract_id,
                                               conttype=b2c_data['contractType'],
                                               purpose=b2c_data['purpose'], contcategory=b2c_data['contractCategory'],
                                               contstatus=b2c_contract_status, enddate=iso_date_b2c_edate,
                                               effecdate=iso_date_b2c_effdate, exedate=iso_date_b2c_exdate,
                                               oblstate=obl_state, consstate=consent_state, currentdate=current_date_time))

                if consent_state in ['Invalid', 'Expired'] and b2c_contract_status \
                        not in ('statusViolated', 'statusTerminated', 'statusExpired'):
                    print('if')
                    # update contract status
                    # ContractStatusUpdateById.get(self, b2c_contract_id, 'statusExpired')
                    # update b2b obligation
                    # ObligationStatusUpdateById.get(self, obligation_id, 'stateInvalid')
                    # CCVHelper.send_email(self, 'expire', b2c, obl_desc, obligation_id)
                else:
                    print('if consent is not invalid or expired')

                    scenario = "ccv_third_else_part_scenario"
                    iso_date_b2c_edate = CCVHelper.iso_date_conversion(self, b2c_data['endDate'][:19])
                    iso_date_b2c_exdate = CCVHelper.iso_date_conversion(self, b2c_data['executionDate'][:19])
                    iso_date_b2c_effdate = CCVHelper.iso_date_conversion(self, b2c_data['effectiveDate'][:19])

                    all_violation_messages.append(
                        CCVHelper.shacl_validation(self, scenario=scenario, contid=b2c_contract_id,
                                                   conttype=b2c_data['contractType'],
                                                   purpose=b2c_data['purpose'],
                                                   contcategory=b2c_data['contractCategory'],
                                                   contstatus=b2c_contract_status, enddate=iso_date_b2c_edate,
                                                   effecdate=iso_date_b2c_effdate,
                                                   exedate=iso_date_b2c_exdate,
                                                   oblstate=obl_state, consstate=consent_state, currentdate=current_date_time))

                    # current_date_time = date(2023, 4, 24)
                    if current_date_time >= date_time_obj and obl_state == 'statePending' \
                            and b2c_contract_status not in (
                            'statusViolated', 'statusTerminated', 'statusExpired'):
                        print('else')
                        # ContractStatusUpdateById.get(self, b2c_contract_id, 'statusViolated')
                        # ObligationStatusUpdateById.get(self, id, 'stateViolated')
                        # CCVHelper.send_email(self, 'violation', b2c, obl_desc, obligation_id)

            # handle single business to consumer contract
            elif b2c != "" and consent == "empty":
                print(f'b2c without consent')

                scenario = "ccv_fourth_scenario"
                # print(scenario)
                # print(f"b2c_data= {b2c_data}")
                iso_date_b2c_edate = CCVHelper.iso_date_conversion(self, b2c_data['endDate'][:19])
                iso_date_b2c_exdate = CCVHelper.iso_date_conversion(self, b2c_data['executionDate'][:19])
                iso_date_b2c_effdate = CCVHelper.iso_date_conversion(self, b2c_data['effectiveDate'][:19])

                all_violation_messages.append(
                    CCVHelper.shacl_validation(self, scenario=scenario, contid=b2c_contract_id,
                                               conttype=b2c_data['contractType'],
                                               purpose=b2c_data['purpose'], contcategory=b2c_data['contractCategory'],
                                               contstatus=b2c_contract_status, enddate=iso_date_b2c_edate,
                                               effecdate=iso_date_b2c_effdate, exedate=iso_date_b2c_exdate,
                                               oblstate=obl_state, currentdate=current_date_time))

                # print(b2c_data)
                if current_date_time >= date_time_obj and obl_state == 'statePending' \
                        and b2c_contract_status not in (
                        'statusViolated', 'statusTerminated', 'statusExpired'):
                    print('if')
                    # ContractStatusUpdateById.get(self, b2c_contract_id, 'statusViolated')
                    # ObligationStatusUpdateById.get(self, id, 'stateViolated')
                    # CCVHelper.send_email(self, 'violation', b2c, obl_desc, obligation_id)
        print(all_violation_messages)

        """
            if the consent expires and data controller still use that consent
        """
        # get all contracts
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

                    # get term by contract
                    terms = GetContractTerms.get(self, contract_id)
                    my_json = terms.data.decode('utf-8')
                    terms_data = json.loads(my_json)
                    for term in terms_data:
                        # obligations
                        obligations = term['obligations']
                        # loop over obligations
                        for ob in obligations:
                            obl = ObligationById.get(self, ob)
                            my_json = obl.data.decode('utf-8')
                            decoded_data = json.loads(my_json)
                            if decoded_data != 'No record found for this ID':
                                # obligation data
                                obl_data = decoded_data
                                for o in obl_data:
                                    contractIdB2C = o['contractIdB2C']
                                    if contractIdB2C != '':
                                        c_obj1 = ContractByContractId.get(self, contractIdB2C)
                                        c_obj1 = c_obj1.json
                                        consent_id = c_obj1['consentId']

                                        if consent_id != '':
                                            consent_state = CCVHelper.get_consent_state(self, consent_id)

                                            scenario = "ccv_fifth_scenario"
                                            all_violation_messages.append(
                                                CCVHelper.shacl_validation(self, scenario=scenario,
                                                                           contid=c_obj1['contractId'],
                                                                           contstatus=b2c_contract_status,
                                                                           consstate=consent_state, currentdate=current_date_time))

                                            if consent_state == 'Invalid' and contract_status not in ['statusExpired',
                                                                                                      'statusTerminated']:
                                                # get contractors
                                                contractors = GetContractContractors.get(self, contract_id)
                                                contractors = contractors.json
                                                for con in contractors:
                                                    contractor = ContractorById.get(self, con['contractorId'])
                                                    contractor = contractor.json
                                                    email = contractor['email']
                                                    message = 'The consent = ' + str(
                                                        consent_id) + ' ' + 'has been expired/invalid but the contract =' \
                                                              + contract + ' is still running based on this consent '

                                                    # mail = Mailer(email=os.environ.get('MAIL_USERNAME'),
                                                    #               password=os.environ.get('MAIL_PASSWORD'))
                                                    # mail.settings(provider=mail.MICROSOFT)
                                                    # mail.send(receiver=email,
                                                    #           subject='Violation/Expiration of Obligation',
                                                    #           message=message)

        return all_violation_messages
        # return 'Success'
