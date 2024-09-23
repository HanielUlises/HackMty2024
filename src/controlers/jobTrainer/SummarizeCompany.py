from openai import OpenAI
import data_base_handler as dbh
import httpx



#from transformers import pipeline
class Client:
    def __init__(self):
        self.client = OpenAI(
            api_key="-",
            base_url="http://198.145.126.109:8080/v1"
        )
        self.index = dbh.init_pinecone()
        self.mongo = dbh.connect_to_company_information(uri=dbh.DATA_BASE_URI)
        


class SummarizeCompany:


    def __init__(self):
        conections = Client()
        self.client=conections.client
        self.index = conections.index
        self.mongo = conections.mongo
        self.file_text=""
        self.pattern_or_ideas=""

    #def ReSummarize(self):
    #   reSum = pipeline("summarization", model="Falconsai/text_summarization")
    #   print(reSum)

    async def relevantIdeas(self, promt):
        
        
            conection = dbh.connect_to_company_information(dbh.DATA_BASE_URI)
            document = conection.find_one() # Fetch one document directly to avoid looping
            
            if document: 
                self.file_text = document.get("content")
                
                try:
                
                    async with httpx.AsyncClient(timeout=30.0) as client:
                        response = await client.post(
                        url="http://198.145.126.109:8080/v1/chat/completions",
                        json={
                            "model":"tgi",
                            "messages":[{"role": "system", "content": promt + self.file_text[:500]}],
                            "stream":False    
                        }
                        )
                        pattern_idea = response.json()["choices"][0]["message"]["content"]
                        self.pattern_or_ideas += pattern_idea
                    return self.pattern_or_ideas
            
                except httpx.ReadTimeout:
                    return "Error: the equest to the API timed out"
                except Exception as e:
                    return f"Error generating code: {str(e)}"

#PROMTS
#You are a text analyst. You have to extract the main ideas from the following text:
#You are a pattern detection specialist. You have to find patterns in the following text:"
