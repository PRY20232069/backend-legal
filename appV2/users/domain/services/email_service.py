from abc import abstractmethod

class EmailService:
    
    @abstractmethod
    def send_email(self, from_: str,
             to: list[str],
             subject: str,
             body: str,
             attachments = None) -> bool:
        raise NotImplementedError()