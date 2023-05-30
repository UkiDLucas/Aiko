
from datetime import datetime

def query_private_embedings(keywords, retrievalQA):

        now = datetime.now()
        print("\n\n> Start local query ", now.strftime("%H:%M:%S") )
        
        text_snippet_Dict = retrievalQA(keywords)
        print("\n\n> answer from the chain: ", text_snippet_Dict , "\n\n End local query ", now.strftime("%H:%M:%S"))
        return text_snippet_Dict