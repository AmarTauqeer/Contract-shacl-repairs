import requests

from resources.imports import *
from resources.schemas import *
from resources.validation_shacl_insert_update import ValidationShaclInsertUpdate


class CompanyUpdate(MethodResource, Resource):
    @doc(description='Company', tags=['Company'])
    # @check_for_session
    # @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    @use_kwargs(CompanyUpdateSchema)
    def put(self, **kwargs):
        schema_serializer = CompanyUpdateSchema()
        data = request.get_json(force=True)
        company_id = data['CompanyId']

        result = CompanyById.get(self, company_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        if len(decoded_data) > 0:
            # # shacl validation
            # validation_data = [{
            #     'validation': 'company',
            #     'companyId': company_id,
            #     'country': data['Country'],
            #     'createDate': data['CreateDate'],
            #     'email': data['Email'],
            #     'name': data['Name'],
            #     'address': data['Address'],
            #     'phone': data['Phone'],
            #     'territory': data['Territory'],
            #     'vat': data['Vat'],
            # }]
            #
            # print(f"validation data= {validation_data}")
            # # send data to validator and receive result
            # validator_url = "http://138.232.18.138:8080/RestDemo/validation"
            # r = requests.post(validator_url, json=validation_data)
            # validation_result = r.text
            # # print(validation_result)
            #
            # if validation_result != "":
            #     return jsonify({'validation_error':validation_result})

            validation_result = ValidationShaclInsertUpdate.validation_shacl_insert_update(self, case="company",
                                                                                           compid=company_id,
                                                                                           name=decoded_data['Name'],
                                                                                           email=decoded_data['Email'],
                                                                                           phone=decoded_data['Phone'],
                                                                                           createdate=decoded_data[
                                                                                               'CreateDate'],
                                                                                           country=decoded_data['Country'],
                                                                                           territory=decoded_data['Territory'],
                                                                                           address=decoded_data['Address'],
                                                                                           vat=decoded_data['Vat'],
                                                                                           )

            # print(validation_result['contractor_violoations'])

            if 'sh:Violation' in validation_result['company_violoations']:
                return validation_result['company_violoations']
            validated_data = schema_serializer.load(data)

            av = CompanyValidation()
            response = av.post_data(validated_data, type="update", company_id=None)
            if (response):
                return jsonify({'Success': "Record updated successfully."})
            else:
                return jsonify({'Error': "Record not updated due to some errors."})
        else:
            return jsonify({'Error': "Record doesn't exist ."})


class CompanyById(MethodResource, Resource):
    @doc(description='Company', tags=['Company'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, companyID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="companyID", contractID=None,
                                   contractRequester=None, contractProvider=None, companyID=companyID))
        res = response["results"]['bindings']
        if len(res) > 0:
            data = {
                'companyId': res[0]['companyId']['value'],
                'name': res[0]['name']['value'],
                'phone': res[0]['phone']['value'],
                'email': res[0]['email']['value'],
                'country': res[0]['country']['value'],
                'territory': res[0]['territory']['value'],
                'address': res[0]['address']['value'],
                'vat': res[0]['vat']['value'],
                'createDate': res[0]['createDate']['value'],
            }
            return data
        return "No record is found for this ID"


class CompanyCreate(MethodResource, Resource):
    @doc(description='Company', tags=['Company'])
    # @check_for_session
    # @Credentials.check_for_token
    @use_kwargs(CompanyRequestSchema)
    def post(self, **kwargs):
        schema_serializer = CompanyRequestSchema()
        data = request.get_json(force=True)
        uuidOne = uuid.uuid1()
        company_id = "cm_" + str(uuidOne)
        validation_result = ValidationShaclInsertUpdate.validation_shacl_insert_update(self, case="company",
                                                                                       compid=company_id,
                                                                                       name=data['Name'],
                                                                                       email=data['Email'],
                                                                                       phone=data['Phone'],
                                                                                       createdate=data['CreateDate'],
                                                                                       country=data['Country'],
                                                                                       territory=data['Territory'],
                                                                                       address=data['Address'],
                                                                                       vat=data['Vat'],
                                                                                       )

        # print(validation_result['contractor_violoations'])

        if 'sh:Violation' in validation_result['company_violoations']:
            return validation_result['company_violoations']

        # # shacl validation
        # validation_data= [{
        #         'validation':'company',
        #         'companyId':company_id,
        #         'country': data['Country'],
        #         'createDate': data['CreateDate'],
        #         'email': data['Email'],
        #         'name': data['Name'],
        #         'address': data['Address'],
        #         'phone': data['Phone'],
        #         'territory': data['Territory'],
        #         'vat': data['Vat'],
        #     }]
        #
        # print(f"validation data= {validation_data}")
        # # send data to validator and receive result
        # validator_url = "http://138.232.18.138:8080/RestDemo/validation"
        # r = requests.post(validator_url, json=validation_data)
        # validation_result = r.text
        # # print(validation_result)
        #
        # if validation_result!="":
        #     return  validation_result
        # if validation_result!="":
        #     validation_result_data={}
        #     if "hasName" in validation_result:
        #         validation_result_data['hasName']='check name field'
        #     if 'description' in validation_result:
        #         validation_result_data['description']='check description field'
        #     return validation_result_data


        validated_data = schema_serializer.load(data)
        av = CompanyValidation()

        response = av.post_data(validated_data, type="insert", company_id=company_id)

        if response == 'Success':
            company_obj = CompanyById.get(self, company_id)
            company_obj = company_obj.json
            return company_obj
        else:
            return jsonify({'Error': "Record not inserted due to some errors."})


class CompanyDeleteById(MethodResource, Resource):
    @doc(description='Company', tags=['Company'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    # @use_kwargs(ContractRequestSchema)
    def delete(self, companyID):
        # get contract status from db
        result = CompanyById.get(self, companyID)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)

        if decoded_data != 'No record is found for this ID':
            if decoded_data['companyId'] == companyID:
                av = CompanyValidation()
                response = av.delete_company(companyID)
                if (response):
                    return jsonify({'Success': "Record deleted successfully."})
                else:
                    return jsonify({'Error': "Record not deleted due to some errors."})
        return "No record is found to be deleted."


class GetCompany(MethodResource, Resource):
    @doc(description='Company', tags=['Company'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="companies", companyID=None,
                                   contractRequester=None, contractProvider=None, ))
        response = response["results"]['bindings']
        data_array = []
        if len(response) >= 1:
            for r in response:
                data = {
                    'companyId': r['companyId']['value'],
                    'name': r['name']['value'],
                    'phone': r['phone']['value'],
                    'email': r['email']['value'],
                    'country': r['country']['value'],
                    'territory': r['territory']['value'],
                    'address': r['address']['value'],
                    'vat': r['vat']['value'],
                    'createDate': r['createDate']['value'],
                }
                data_array.append(data)
            return data_array
        return "No record is found"
