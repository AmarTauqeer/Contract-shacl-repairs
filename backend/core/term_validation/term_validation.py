from core.query_processor.QueryProcessor import QueryEngine


class TermValidation(QueryEngine):

    def __init__(self):
        super().__init__()

    def list_to_query(self, data, whatfor):
        """ Convert list of data processing information to SPARQL query strings
        :input: data<list> [
        :input: whatfor<string> - SPARQL property
        :returns: SPARQL query string
        """
        querydata = ""
        for vlaue in data:
            strs = ":" + whatfor + " :" + vlaue + ";\n"
            querydata = strs + querydata
        return querydata

    def delete_term(self, termID):
        # delete obligation first
        response = self.post_sparql(self.get_username(), self.get_password(),
                                    self.delete_term_by_id(termID))
        return response

    def post_data(self, validated_data, type, term_id):
        TermTypeId = validated_data["TermTypeId"]
        Obligations = validated_data["Obligations"]
        Description = validated_data["Description"]
        CreateDate = validated_data["CreateDate"]

        # remove empty string
        if Description=='string':
            Description=""

        if type == "insert":
            TermId = term_id
            respone = self.post_sparql(self.get_username(), self.get_password(),
                                       self.insert_query_term(TermId=TermId,
                                                              TermTypeId=TermTypeId,
                                                              Obligations=self.list_to_query(Obligations,
                                                                                             "hasObligations"),
                                                              Description=Description,
                                                              CreateDate=CreateDate,
                                                              )

                                       )
        else:
            TermId = validated_data["TermId"]
            if TermId != "":
                # delete from knowledge graph
                response = self.post_sparql(self.get_username(), self.get_password(),
                                            self.delete_term_by_id(TermId))

                # insert into kg
                respone = self.post_sparql(self.get_username(), self.get_password(),
                                           self.insert_query_term(TermId=TermId,
                                                                  TermTypeId=TermTypeId,
                                                                  Obligations=self.list_to_query(Obligations,
                                                                                                 "hasObligations"),
                                                                  Description=Description,
                                                                  CreateDate=CreateDate,
                                                                  )

                                           )
        return respone
