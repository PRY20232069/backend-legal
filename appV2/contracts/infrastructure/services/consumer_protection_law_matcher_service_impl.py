import ast
import openai
import pandas as pd
from typing import List
from scipy.spatial.distance import cosine

from appV2.contracts.domain.services.consumer_protection_law_matcher_service import ConsumerProtectionLawMatcherService

from settings import OPENAI_API_KEY

class ConsumerProtectionLawMatcherServiceImpl(ConsumerProtectionLawMatcherService):

    def __init__(self):
        self.protection_laws = pd.read_csv('./datasets/consumer_protection_laws.csv')
        
        openai.api_key = OPENAI_API_KEY
        self.open_ai_client = openai
        self.open_ai_client.api_timeout = 360 # 6 minutos
    
    def match(self, terms: List[str]) -> List[str]:

        laws: List[str] = []
        for term in terms:
            term_embedding = self.__get_embeddings__(term)

            def calculate_similarity(row):
                law_embedding = ast.literal_eval(row['embeddings'])
                return self.__cosine_similarity__(term_embedding, law_embedding)

            result_similarities = self.protection_laws.apply(calculate_similarity, axis=1)
            most_similar_law = self.protection_laws.loc[result_similarities.idxmin(), 'rule']

            laws.append(most_similar_law)

        return laws
    
    def __get_embeddings__(self, term: str):
        try: 
            response = self.open_ai_client.embeddings.create(
                input=[term],
                model="text-embedding-ada-002"
            )

            return response.data[0].embedding
        except Exception as e:
            print(e)
            return None
    
    def __cosine_similarity__(self, vec1, vec2):
        return 1 - cosine(vec1, vec2)