import re
import openai
from typing import List, Tuple

from appV2.contracts.domain.services.term_interpretation_generator_service import TermInterpretationGeneratorService
from appV2.contracts.application.exceptions.term_exceptions import GenerateTermInterpretationError

from settings import OPENAI_API_KEY, NUMBER_OF_TERMS_PROCESSED_IN_PARALLEL, OPENAI_MODEL_ID_1X1, OPENAI_SYSTEM_CONTENT_1X1, OPENAI_MODEL_ID_3X3, OPENAI_SYSTEM_CONTENT_3X3

class TermInterpretationGeneratorServiceImpl(TermInterpretationGeneratorService):

    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        self.open_ai_client = openai
        self.open_ai_client.api_timeout = 360 # 6 minutos

    def generate(self, terms: List[str]) -> List[Tuple[bool, str]]:
        if len(terms) > NUMBER_OF_TERMS_PROCESSED_IN_PARALLEL:
            print(f"APP ERROR: The number of terms to process must be less than or equal to {NUMBER_OF_TERMS_PROCESSED_IN_PARALLEL}")
            raise GenerateTermInterpretationError()

        terms_input, terms_output = self.get_interpretations_3x3(terms)

        messages = re.findall(r'\d+: .+?(?====)', terms_output)
        messages = [message.split(': ')[1] for message in messages]
        
        if (messages is None or len(messages) < len(terms)):
            print("APP INFO: Fewer interpretations were generated than expected. Using model 1x1")
            
            messages = []
            for term in terms:
                term_input, term_output = self.get_interpretation_1x1(term)
                message = term_output.split('===')[0]
                messages.append(message)

        return self.get_interpretations_formatted(messages)


    def get_interpretations_formatted(self, messages: List[str]):
        interpretations = []

        for message in messages:
            parts = message.split('. ')
            
            abusive = parts[0] == 'Sí'
            explanation = ' '.join(parts[1:])
            interpretations.append((abusive, explanation))
            
        return interpretations



    def get_interpretations_3x3(self, terms: List[str]) -> Tuple[str, str]:
        try:
            terms_input = ''.join([f'{i+1}: {term}###' for i, term in enumerate(terms)])

            response = self.open_ai_client.chat.completions.create(
                model=OPENAI_MODEL_ID_3X3,
                messages=[
                    {"role": "system", "content": OPENAI_SYSTEM_CONTENT_3X3},
                    {"role": "user", "content": terms_input},
                ]
            )

            terms_output = response.choices[0].message.content

            return (terms_input, terms_output)
        except Exception as e:
            print(e)
            return None


    def get_interpretation_1x1(self, term: str):
        try:
            term_input = f"{term}###"

            response = self.open_ai_client.chat.completions.create(
                model=OPENAI_MODEL_ID_1X1,
                messages=[
                    {"role": "system", "content": OPENAI_SYSTEM_CONTENT_1X1},
                    {"role": "user", "content": term_input }
                ]
            )
            term_output = response.choices[0].message.content
            return (term_input, term_output)
        except Exception as e:
            print(e)
            return None