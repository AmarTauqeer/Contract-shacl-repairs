# from resources.contracts import ContractByContractId
from core.security.RsaAesDecryption import RsaAesDecrypt
from resources.imports import *
from resources.schemas import *


class GetObligations(MethodResource, Resource):
    @doc(description='Obligations', tags=['Obligations'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="obligations", termID=None,
                                   contractRequester=None, contractProvider=None, ))
        data = response["results"]['bindings']
        if len(data) != 0:

            obligation_sub_array = []
            for d in data:
                # print(d)
                obligation_id = d['obligationId']['value']

                # get contract id, term id and contractor id
                obl = ObligationById.get(self, obligation_id)
                obl_data = obl.json
                # print(obl_data)
                new_data = {
                    'obligationId': obligation_id,
                    'state': obl_data[0]['state'],
                    'obligationDescription': obl_data[0]['obligationDescription'],
                    'exectionDate': obl_data[0]['executionDate'],
                    'endDate': obl_data[0]['endDate'],
                    'fulfillmentDate': obl_data[0]['fulfillmentDate'],
                    'contractIdB2C': obl_data[0]['contractIdB2C'],
                    'contractorId': obl_data[0]['contractorId'],
                }
                obligation_sub_array.append(new_data)
            if len(obligation_sub_array) != 0:
                return obligation_sub_array
        return 'No record found'


class GetObligationByTermId(MethodResource, Resource):
    @doc(description='Obligations', tags=['Obligations'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, termID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="termObligation",
                                   contractID=None,
                                   contractRequester=None, contractProvider=None, contractorID=None, termID=termID
                                   ))
        data = response["results"]['bindings']
        # print(len(data))
        if len(data) != 0:
            obligation_array = []
            for d in data:
                obligation_id = d['obligationId']['value']
                new_data = {'obligationId': obligation_id,
                            'state': d['state']['value'][45:],
                            'obligationDescription': d['obligationDescription']['value'],
                            'exectionDate': d['executionDate']['value'],
                            'endDate': d['endDate']['value'],
                            'fulfillmentDate': d['fulfillmentDate']['value'],
                            'contractIdB2C': d['contractIdB2C']['value'],
                            'termId': termID,
                            }
                obligation_array.append(new_data)
            return obligation_array
        return 'No record found for this ID'


class ObligationById(MethodResource, Resource):
    @doc(description='Obligations', tags=['Obligations'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, obligationID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="obligationID",
                                   obligationID=obligationID,
                                   contractRequester=None, contractProvider=None))
        data = response["results"]['bindings']
        # print(data)
        if len(data) != 0:
            identifier_array = []
            obligation_array = []
            for d in data:
                obj_dec = RsaAesDecrypt()
                data = {'obligation_id': obligationID,
                        'description': d['obligationDescription']['value'],
                        # 'contractor_id': d['obligationDescription']['value'],
                        }
                decrypted_result = obj_dec.rsa_aes_decrypt(data)
                description = decrypted_result[0]['description']

                new_data = {'obligationId': obligationID,
                            'state': d['state']['value'][45:],
                            'obligationDescription': description,  # d['obligationDescription']['value'],
                            'executionDate': d['executionDate']['value'],
                            'endDate': d['endDate']['value'],
                            'fulfillmentDate': d['fulfillmentDate']['value'],
                            'contractorId': d['contractorId']['value'],
                            'contractIdB2C': d['contractIdB2C']['value'],
                            }
                obligation_array.append(new_data)
            if len(obligation_array) != 0:
                return obligation_array
        return 'No recrod found for this ID'


class GetObligationIdentifierById(MethodResource, Resource):
    @doc(description='Obligations', tags=['Obligations'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, obligationID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="obligationIdentifier",
                                   obligationID=obligationID,
                                   contractRequester=None, contractProvider=None))
        res = response["results"]['bindings']
        print(res)
        data = []
        if len(res) != 0:
            for r in res:
                a = r['contractIdB2C']['value']
                data.append(a)
            return data
        return 'No record found for this ID'


class ObligationCreate(MethodResource, Resource):
    @doc(description='Obligations', tags=['Obligations'])
    # @check_for_session
    # @Credentials.check_for_token
    @use_kwargs(ObligationRequestSchema)
    def post(self, **kwargs):
        schema_serializer = ObligationRequestSchema()
        data = request.get_json(force=True)
        print(data)
        uuidOne = uuid.uuid1()
        obligation_id = "ob_" + str(uuidOne)

        # # shacl validation
        # validation_data= [{
        #         'type_validation':'termtypes',
        #         'typeId':term_id,
        #         'name': data['Name'],
        #         'description': data['Description'],
        #     }]
        #
        # print(f"validation data= {validation_data}")
        # # send data to validator and receive result
        # validator_url = "http://localhost:8080/RestDemo/demo"
        # r = requests.post(validator_url, json=validation_data)
        # validation_result = r.text
        # print(validation_result)
        # if validation_result!="":
        #     return  validation_result


        validated_data = schema_serializer.load(data)
        av = ObligationValidation()
        response = av.post_data(validated_data, type="insert", obligation_id=obligation_id)
        if response == 'Success':
            contract_obj = ObligationById.get(self, obligation_id)
            contract_obj = contract_obj.json
            return contract_obj
        return jsonify({'Error': "Record not inserted due to some errors."})


class ObligationDeleteById(MethodResource, Resource):
    @doc(description='Obligations', tags=['Obligations'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    # @use_kwargs(ContractRequestSchema)
    def delete(self, obligationID):
        # get contract status from db
        result = ObligationById.get(self, obligationID)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        if decoded_data != 'No record found for this ID':
            av = ObligationValidation()
            response = av.delete_obligation(obligationID)
            if (response):
                return jsonify({'Success': "Record deleted successfully."})
            else:
                return jsonify({'Error': "Record not deleted due to some errors."})
        return jsonify({'Success': "No record found for this ID."})


class ContractObligationUpdate(MethodResource, Resource):
    @doc(description='Obligations', tags=['Obligations'])
    # @check_for_session
    # @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    @use_kwargs(ObligationRequestSchema)
    def put(self, **kwargs):
        schema_serializer = ObligationRequestSchema()
        data = request.get_json(force=True)
        obligation_id = data['ObligationId']

        result = ObligationById.get(self, obligation_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        if len(decoded_data) > 0:
            validated_data = schema_serializer.load(data)
            av = ObligationValidation()
            response = av.post_data(validated_data, type="update")
            if (response):
                return response
            else:
                return jsonify({'Error': "Record not updated due to some errors."})
        else:
            return jsonify({'Error': "Record doesn't exist ."})


class ObligationStatusUpdateByObligationId(MethodResource, Resource):
    @doc(description='Obligations', tags=['Obligations'])
    # @Credentials.check_for_token
    def get(self, obligationID, state):

        host_post = os.getenv("HOST_URI_POST")
        hostname = host_post
        userid = os.getenv("user_name")
        password = os.getenv("password")

        # updated_date = date.today()
        sparql = SPARQLWrapper(hostname)
        sparql.setHTTPAuth(BASIC)
        sparql.setCredentials(userid, password)
        query = textwrap.dedent("""
         PREFIX : <http://ontologies.atb-bremen.de/smashHitCore#>
         PREFIX dct: <http://purl.org/dc/terms/>
         PREFIX prov: <http://www.w3.org/ns/prov#>
         PREFIX fibo-fnd-agr-ctr: <https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/>
            DELETE {{?Obligation :hasStates :statePending.
                    ?Obligation :hasStates :stateViolated.
                    ?Obligation :hasStates :stateFulfilled.
                    ?Obligation :hasStates :stateInvalid.
                    ?Obligation :hasStates :stateExpired.}}
            INSERT {{?Obligation :hasStates :{1}.}}
            where {{
                     ?Obligation rdf:type :Obligation;
                                 :hasStates ?state;
                                 :obligationID ?obligationId .
                     FILTER(?obligationId = "{0}") .
    }}""").format(obligationID, state)

        sparql.setQuery(query)
        sparql.method = "POST"
        sparql.queryType = "INSERT"
        sparql.setReturnFormat('json')
        result = sparql.query()
        if str(result.response.read().decode("utf-8")) == "":
            return "Success"
        else:
            return "Fail"


class ObligationStatusUpdateById(MethodResource, Resource):
    @doc(description='Contract Obligations', tags=['Contract Obligations'])
    # @Credentials.check_for_token
    def get(self, obligationID, state):

        host_post = os.getenv("HOST_URI_POST")
        hostname = host_post
        userid = os.getenv("user_name")
        password = os.getenv("password")

        violation_date = date.today()
        sparql = SPARQLWrapper(hostname)
        sparql.setHTTPAuth(BASIC)
        sparql.setCredentials(userid, password)
        query = textwrap.dedent("""
         PREFIX : <http://ontologies.atb-bremen.de/smashHitCore#>
         PREFIX dct: <http://purl.org/dc/terms/>
         PREFIX prov: <http://www.w3.org/ns/prov#>
         PREFIX fibo-fnd-agr-ctr: <https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/>
         
            DELETE {{?Obligation :hasStates :stateValid.
                    ?Obligation :hasStates :statePending.
                    ?Obligation :hasStates :stateViolated.
                    ?Obligation :hasStates :stateFulfilled.
                    }}
            INSERT {{?Obligation :hasStates :{2}.
            ?obligationId :RevokedAtTime {0}.
            }}
             WHERE {{
             ?Obligation rdf:type :Obligation;
             :obligationID ?obligationId .
              FILTER(?obligationId = "{1}")
             }}""").format('\'{}\'^^xsd:dateTime'.format(violation_date), obligationID, state)

        sparql.setQuery(query)
        sparql.method = "POST"
        sparql.queryType = "INSERT"
        sparql.setReturnFormat('json')
        result = sparql.query()

        if str(result.response.read().decode("utf-8")) == "":
            return "Success"
        else:
            return "Fail"
