from appV2._shared.application.exceptions.base_exceptions import BaseBadRequestError, BaseConflictError, BaseNotFoundError


class TermEvaluationNotFoundError(BaseNotFoundError):
    message = 'Term evaluation does not exist.'


class TermEvaluationAlreadyExistsError(BaseConflictError):
    message = 'Term evaluation already exists'


class CreateTermEvaluationError(BaseBadRequestError):
    message = 'An error occurred while creating a term evaluation'


class UpdateTermEvaluationError(BaseBadRequestError):
    message = 'An error occurred while updating a term evaluation'


class DeleteTermEvaluationError(BaseBadRequestError):
    message = 'An error occurred while deleting a term evaluation'