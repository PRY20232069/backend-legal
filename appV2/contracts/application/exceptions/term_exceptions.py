from appV2._shared.application.exceptions.base_exceptions import BaseBadRequestError, BaseError, BaseNotFoundError


class TermNotFoundError(BaseNotFoundError):
    message = 'Term does not exist.'


class CreateTermError(BaseBadRequestError):
    message = 'An error occurred while creating a term'

    
class GenerateTermInterpretationError(BaseError):
    message = 'An error occurred while generating term interpretation'

    
class MatchConsumerProtectionLawError(BaseError):
    message = 'An error occurred while matching consumer protection law'