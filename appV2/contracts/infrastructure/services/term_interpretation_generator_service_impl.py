import openai
from typing import List

from appV2.contracts.domain.services.term_interpretation_generator_service import TermInterpretationGeneratorService

from settings import OPENAI_API_KEY, OPENAI_MODEL_ID, OPENAI_SYSTEM_CONTENT

class TermInterpretationGeneratorServiceImpl(TermInterpretationGeneratorService):

    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        self.open_ai_client = openai
        self.open_ai_client.api_timeout = 360 # 6 minutos

    def generate(self, terms: List[str]) -> List[str]:
        interpretations: List[str] = []

        for term in terms:
            result_interpretation = self.__get_interpretation__(term)
            interpretations.append(result_interpretation)

        return interpretations


    def __get_interpretation__(self, term: str):
        try:
            response = self.open_ai_client.chat.completions.create(
                model=OPENAI_MODEL_ID,
                messages=[
                    {"role": "system", "content": OPENAI_SYSTEM_CONTENT},
                    {"role": "user", "content": f"{term}###"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(e)
            return None