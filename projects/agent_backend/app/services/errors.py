class ConversationNotFound(Exception):
    pass


class ConversationBusy(Exception):
    pass


class BusinessMessageSaveError(Exception):
    pass


class ConversationDeleteError(Exception):
    pass


class StructuredOutputError(Exception):
    pass
