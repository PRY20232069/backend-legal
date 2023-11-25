import pandas as pd
import openai
import ast
from settings import OPENAI_API_KEY
from scipy.spatial.distance import cosine


class ConsumerProtectionLawMatcher:
    def __init__(self):
        self.protection_laws = pd.read_csv('./datasets/consumer_protection_laws.csv')
        
        openai.api_key = OPENAI_API_KEY
        self.openAIClient = openai
        self.openAIClient.api_timeout = 360 # 6 minutos

    def getConsumerProtectionLaw(self, term_description) -> str:
        return self.__matchConsumerProtectionLaw__(term_description)
    
    
    def __matchConsumerProtectionLaw__(self, term_description) -> str:
        term_embedding = self.__get_embeddings__(term_description)

        def calculate_similarity(row):
            law_embedding = ast.literal_eval(row['embeddings'])
            return self.__cosine_similarity__(term_embedding, law_embedding)

        result_similarities = self.protection_laws.apply(calculate_similarity, axis=1)
        most_similar_law = self.protection_laws.loc[result_similarities.idxmin(), 'rule']

        return most_similar_law
    
    
    
    def __get_embeddings__(self, term_description):
        try: 
            response = self.openAIClient.embeddings.create(
                input=[term_description],
                model="text-embedding-ada-002"
            )

            return response.data[0].embedding
        except Exception as e:
            print(e)
            return None
    
    def __cosine_similarity__(self, vec1, vec2):
        return 1 - cosine(vec1, vec2)