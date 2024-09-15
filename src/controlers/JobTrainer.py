from openai import OpenAI
from SummarizeCompany import Client
from SummarizeCompany import SummarizeCompany
import data_base_handler as dbh


class JobTrainer:
    def __init__(self):
        self.client = Client().client

    def generateProblem(self, context):
        response = self.client.chat.completions.create(
            model="tgi",
            messages=[
            {"role": "system", "content": "You are a trainer in a company who teaches newly hired employees."+
             "For their introduction, you ask them to solve a problem based on the context of the company. The context is as follows:"
             +context+"Tell me what problem you would give to the new employee."}
            ],stream=False
        )
        problem=response.choices[0].message.content
        print(problem)

        
if __name__ == '__main__':
    uri = dbh.DATA_BASE_URI

    check_conect=dbh.connect_to_company_information(uri)

    train = SummarizeCompany()
    context = train.relevantIdeas("You are a text analyst. You have to extract the main ideas from the following text:")
    trainer = JobTrainer()
    trainer.generateProblem(context)
