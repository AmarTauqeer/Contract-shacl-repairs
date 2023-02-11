# Automated Contracting Tool Improved with SHACL Repairs

Automated Contracting Tool, a component of smashHit. smashHit is a Horizon 2020 project with the primary objective of creating a secure and trustworthy data-sharing platform with a focus on consent and contract management in a distributed environment such as the automotiveindustry, insurance and smart cities following GDPR.

## Software Requirements

- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)
- [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/)
- [flask_apispec](https://flask-apispec.readthedocs.io/en/latest/index.html)
- [SPARQLWrapper](https://rdflib.dev/sparqlwrapper/)
- [unittest](https://docs.python.org/3/library/unittest.html)

## Steps to be followed
- git clone https://github.com/AmarTauqeer/Contract-shacl-repairs.git
- go to the backend folder
- update the .env file
- sudo docker-compose -f docker-compose.yml up

## Running Locally

Run the command below from the root directory for deployement and access via [http://localhost:5001](http://localhost:5001). The Swagger API documentation can be accessed via [http://localhost:5001/swagger-ui/](http://localhost:5001/swagger-ui/).

```bash
python -m flask run

```

## Important Note For Testing REST Endpoints
- For hasContractStatus choose from the list (statusCreated, statusUpdate)
- For hasStates choose from the list (statePending, stateInvalid, stateValid)
- For hasRole choose from the list (DataSubject, DataController, DataProcessor)
- For hasContractCategory choose from the list (categoryBusinessToConsumer, categoryBusinessToBusiness)

## Steps to create/update a contract

- Create term types and companies.
- Create contractors (need company id).
- Create a contract with basic information except contract terms, contract obligations, and contract signatures.
- Use the contract id from the previous step and create contract terms, contract obligations and contract signatures.
- Update the contract with terms, contractors and signatures.




## Contracts System Architecture
![](/backend/images/semantic-contract-architecture.png)

## Contracts REST APIs Endpoints
![](/backend/images/contract-api-first-part.png)
![](/backend/images/contract-api-second-part.png)

## Developer

- Amar Tauqeer
  amar.tauqeer@sti2.at, amar.tauqeer@gmail.com
- Web: "https://amartauqeer.github.io/amar-tauqeer-portfolio/"
- LinkedIn: "https://www.linkedin.com/in/amar-tauqeer/"

## Project

- [smashHit](https://www.smashhit.eu/)

## License

MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions: 

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
