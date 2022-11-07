import requests

from resources.contract_obligation import ObligationById, GetObligationByTermId, ObligationDeleteById
from resources.imports import *
from resources.schemas import *


class GetTerms(MethodResource, Resource):
    @doc(description='Terms', tags=['Terms'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="terms", termID=None,
                                   contractRequester=None, contractProvider=None, ))
        response = response["results"]['bindings']
        if len(response) != 0:
            term_array = []
            for r in response:
                term_id = r['termId']['value']
                # get obligation
                obl = GetObligationByTermId.get(self, term_id)
                obl = obl.json
                obligation_array = []
                if obl != 'No record found for this ID':
                    for o in obl:
                        oid = o['obligationId']
                        obligation_array.append(oid)

                data = {
                    'termId': r['termId']['value'],
                    'termTypeId': r['termTypeId']['value'],
                    'obligations': obligation_array,
                    'description': r['description']['value'],
                    'createDate': r['createDate']['value']
                }
                term_array.append(data)
            return term_array
        return 'Record does not exist'


class TermById(MethodResource, Resource):
    @doc(description='Terms', tags=['Terms'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, termID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="termID", contractID=None,
                                   contractRequester=None, contractProvider=None, termID=termID))
        res = response["results"]['bindings']

        obligation_array = []
        if len(res) > 0:
            res = res[0]
            term_id = res['termId']['value']
            # get obligation
            obl = GetObligationByTermId.get(self, term_id)
            obl = obl.json

            if obl != 'No record found for this ID':
                for o in obl:
                    oid = o['obligationId']
                    obligation_array.append(oid)
            data = {
                'termId': res['termId']['value'],
                'termTypeId': res['termTypeId']['value'],
                'obligations': obligation_array,
                'description': res['description']['value'],
                'createDate': res['createDate']['value']

            }
            return data
        return "No record available for this term id"


class TermDeleteById(MethodResource, Resource):
    @doc(description='Terms', tags=['Terms'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    # @use_kwargs(ContractRequestSchema)
    def delete(self, termID):
        # get contract status from db
        result = TermById.get(self, termID)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)

        if decoded_data != 'No record available for this term id':
            if decoded_data['termId'] == termID:
                av = TermValidation()
                response = av.delete_term(termID)
                if (response):
                    # delete obligation
                    obl = GetObligationByTermId.get(self, termID)
                    my_json = obl.data.decode('utf-8')
                    decoded_data = json.loads(my_json)
                    if decoded_data != 'No record found for this ID':
                        obl_data = decoded_data
                        for o in obl_data:
                            obligation_id = o['obligationId'];
                            ObligationDeleteById.delete(self, obligation_id)
                    return jsonify({'Success': "Record deleted successfully."})
                else:
                    return jsonify({'Error': "Record not deleted due to some errors."})
            return jsonify({'Error': "Record does not match."})
        return jsonify({'Error': "Record does not exist."})


class TermCreate(MethodResource, Resource):
    @doc(description='Terms', tags=['Terms'])
    # @check_for_session
    # @Credentials.check_for_token
    @use_kwargs(TermRequestSchema)
    def post(self, **kwargs):
        schema_serializer = TermRequestSchema()
        data = request.get_json(force=True)
        uuidOne = uuid.uuid1()
        term_id = "term_" + str(uuidOne)
        # shacl validation
        validation_data= [{
                'validation':'term',
                'termId':term_id,
                'termTypeId': data['TermTypeId'],
                'createDate': data['CreateDate'],
                'description': data['Description'],
            }]

        print(f"validation data= {validation_data}")
        # send data to validator and receive result
        validator_url = "http://127.0.0.1:8080/RestDemo/validation"
        r = requests.post(validator_url, json=validation_data)
        validation_result = r.text
        # print(validation_result)

        if validation_result!="":
            return  validation_result
        # if validation_result!="":
        #     validation_result_data={}
        #     if "hasName" in validation_result:
        #         validation_result_data['hasName']='check name field'
        #     if 'description' in validation_result:
        #         validation_result_data['description']='check description field'
        #     return validation_result_data

        validated_data = schema_serializer.load(data)
        # print(validated_data)
        av = TermValidation()
        response = av.post_data(validated_data, type="insert", term_id=term_id)
        if response == 'Success':
            contract_obj = TermById.get(self, term_id)
            contract_obj = contract_obj.json
            return contract_obj
        else:
            return jsonify({'Error': "Record not inserted due to some errors."})


class TermUpdate(MethodResource, Resource):
    @doc(description='Terms', tags=['Terms'])
    # @check_for_session
    # @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    @use_kwargs(TermUpdateSchema)
    def put(self, **kwargs):
        schema_serializer = TermUpdateSchema()
        data = request.get_json(force=True)
        term_id = data['TermId']
        # get contract status from db
        result = TermById.get(self, term_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        if decoded_data != 'No record available for this term id':
            if decoded_data['termId'] == term_id:
                # shacl validation
                validation_data = [{
                    'validation': 'term',
                    'termId': term_id,
                    'termTypeId': data['TermTypeId'],
                    'createDate': data['CreateDate'],
                    'description': data['Description'],
                }]

                print(f"validation data= {validation_data}")
                # send data to validator and receive result
                validator_url = "http://127.0.0.1:8080/RestDemo/validation"
                r = requests.post(validator_url, json=validation_data)
                validation_result = r.text
                # print(validation_result)

                if validation_result != "":
                    return jsonify({'validation_error':validation_result})

                validated_data = schema_serializer.load(data)
                av = TermValidation()
                response = av.post_data(validated_data, type="update", term_id=None)
                if (response):
                    return jsonify({'Success': "Record updated successfully."})
                else:
                    return jsonify({'Error': "Record not updated due to some errors."})
            else:
                return jsonify({'Error': "Record doesn't exist ."})


class GetContractTerms(MethodResource, Resource):
    @doc(description='Terms', tags=['Terms'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, contractID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractTerms",
                                   contractID=contractID,
                                   contractRequester=None, contractProvider=None, contractorID=None, termID=None
                                   ))
        data = response["results"]["bindings"]
        # print(data)
        if len(data) != 0:
            term_arry = []
            for d in data:
                obligation_arry = []
                termId = d['termId']['value']
                obl = GetObligationByTermId.get(self, termId)
                my_json = obl.data.decode('utf-8')
                decoded_data = json.loads(my_json)
                if decoded_data != 'No record found for this ID':
                    obl_data = decoded_data
                    for o in obl_data:
                        obligation_id = o['obligationId'];
                        obligation_arry.append(obligation_id)

                new_data = {'contractId': contractID, 'termId': termId, 'description': d['description']['value'],
                            'obligations': obligation_arry}
                term_arry.append(new_data)
            # print(f'term = {term_arry}')
            return term_arry
        return 'No record found for this ID'


# get terms by obligation id
class TermByObligationId(MethodResource, Resource):
    @doc(description='Terms', tags=['Terms'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, obligationID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="termByObligationId",
                                   contractID=None,
                                   contractRequester=None, contractProvider=None, obligationID=obligationID))
        res = response["results"]['bindings']
        if len(res) > 0:
            data = {
                'termId': res[0]['termId']['value'],
                'description': res[0]['description']['value'],
                'createDate': res[0]['createDate']['value']
            }
            return data
        return "No record available for this term id"
