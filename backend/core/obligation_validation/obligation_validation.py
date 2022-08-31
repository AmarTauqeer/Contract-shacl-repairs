import os

from core.query_processor.QueryProcessor import QueryEngine
from core.security.RsaAesEncryption import RsaAesEncrypt


class ObligationValidation(QueryEngine):

    def __init__(self):
        super().__init__()

    def delete_obligation(self, obligationID):
        response = self.post_sparql(self.get_username(), self.get_password(),
                                    self.delete_obligation_by_id(obligationID))
        # delete encryption file from the directory
        cwd = os.getcwd()
        file_name = cwd + '/core/security/bundle' + obligationID + '.enc'
        # remove file from the directory
        os.remove(file_name)

        return response

    def post_data(self, validated_data, type, obligation_id):
        Description = validated_data["Description"]
        ContractorId = validated_data["ContractorId"]
        State = validated_data["State"]
        ExecutionDate = validated_data["ExecutionDate"]
        EndDate = validated_data["EndDate"]
        FulfillmentDate = validated_data["FulfillmentDate"]
        ContractIdB2C = validated_data["ContractIdB2C"]

        if ContractIdB2C=='string':
            ContractIdB2C=""

        if Description=='string':
            Description=""

        # print(ContractId)

        if type == "insert":
            ObligationId = obligation_id
            ############## encryption ########################
            data = {'obligation_id': ObligationId, 'description': Description
                # , 'contractorId': ContractorId
                    }
            obj = RsaAesEncrypt()
            encrypted_data = obj.rsa_aes_encrypt(data)

            Description = encrypted_data[1]['description']
            # ContractorId = encrypted_data[2]['contractor_id']

            ############## end encryption ########################

            # print('insert')
            respone = self.post_sparql(self.get_username(), self.get_password(),
                                       self.insert_query_obligation(ObligationId=ObligationId,
                                                                    Description=Description,
                                                                    ContractorId=ContractorId,
                                                                    ContractIdB2C=ContractIdB2C,
                                                                    State=State,
                                                                    ExecutionDate=ExecutionDate,
                                                                    EndDate=EndDate,
                                                                    FulfillmentDate=FulfillmentDate
                                                                    )

                                       )
        else:
            ObligationId = validated_data["ObligationId"]

            ############## encryption ########################
            data = {'obligation_id': ObligationId, 'description': Description, 'contractorId': ContractorId}
            obj = RsaAesEncrypt()
            encrypted_data = obj.rsa_aes_encrypt(data)

            Description = encrypted_data[1]['description']
            ContractorId = encrypted_data[2]['contractor_id']

            ############## end encryption ########################


            if ObligationId != "":
                # delete from knowledge graph
                response = self.post_sparql(self.get_username(), self.get_password(),
                                            self.delete_obligation_by_id(ObligationId))

                # insert into kg
                respone = self.post_sparql(self.get_username(), self.get_password(),
                                           self.insert_query_obligation(ObligationId=ObligationId,
                                                                        Description=Description,
                                                                        ContractorId=ContractorId,
                                                                        ContractIdB2C=ContractIdB2C,
                                                                        State=State,
                                                                        ExecutionDate=ExecutionDate,
                                                                        EndDate=EndDate,
                                                                        FulfillmentDate=FulfillmentDate
                                                                        )

                                           )
        return respone
