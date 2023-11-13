# from analysis.services.terms_service import TermsService
# from analysis.services.term_query_service import TermQueryService
# from analysis.application.settings.openai_settings import OpenAISettings
# from shared.utils.mediator import Mediator
# from openai import OpenAI


# # ---------------------
# # Mediator
# # ---------------------
# mediator = Mediator()


# # ---------------------
# # Other Dependencies
# # ---------------------
# openAISettings = OpenAISettings()
# openAIClient = OpenAI(api_key=openAISettings.api_key)


# # ---------------------
# # Command Handlers
# # ---------------------
# generateTermExplanationCommandHandler = GenerateTermExplanationCommandHandler(openAIClient, openAISettings)
# uploadContractCommandHandler = UploadContractCommandHandler()

# mediator.register(GenerateTermExplanationCommand, generateTermExplanationCommandHandler)
# mediator.register(UploadContractCommand, uploadContractCommandHandler)


# # ---------------------
# # Query Handlers
# # ---------------------
# getAllTermsByContractIdQueryHandler = GetAllTermsByContractIdQueryHandler()

# mediator.register(GetAllTermsByContractIdQuery, getAllTermsByContractIdQueryHandler)


# # ---------------------
# # Event Handlers
# # ---------------------
# termExplanationGeneratedEventHandler = TermExplanationGeneratedEventHandler()



# # ---------------------
# # Services
# # ---------------------
# term_command_service = TermsService(mediator)
# term_query_service = TermQueryService(mediator)
# contract_command_service = ContractCommandService(mediator)
# contract_query_service = ContractQueryService(mediator)