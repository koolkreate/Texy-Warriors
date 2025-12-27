# base_message.py
#I explain the class method data class yap here!
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
# This code isn't really used now, but may be useful in the future?
# So in the class we are using dataclass; this refers to a wrapper which automatically does the def ___init__self stuff, adds a to string function, and an eq function which allows us to compare instances of this class

@dataclass
class BaseMessage(ABC):
    """
    Abstract base class for all message types.
    
    Attributes:
        role (str): The role of the message sender (system/user/assistant)
        content (str): The content of the message
    """
    role: str
    content: str

    @abstractmethod
    def __post_init__(self):
        """Enforce constraints in subclasses"""
        pass


@dataclass
class SystemMessage(BaseMessage):
    """
    Represents a system message used to set context or instructions.
    
    Automatically sets role to 'system'.
    """
    def __post_init__(self):
        if self.role != "system":
            raise ValueError("SystemMessage must have role='system'")
    
    @classmethod #A class method is a method that would apply for the whole class; say i had a classs called fruit. a non class method would only apply for an instatiated object e.g apples or bananas; but a class method applies for any fruit and can keep track of all fruit for example; so that's how we keep track of all the messages.
    def from_content(cls, content: str) -> 'SystemMessage':
        """
        Convenience constructor for system messages.
        
        Args:
            content (str): System prompt content
            
        Returns:
            SystemMessage: New instance with role='system'
        """
        return cls(role="system", content=content)


@dataclass
class ChatMessage(BaseMessage):
    """
    Represents a chat message (user prompt or LLM response).
    
    Attributes:
        role (str): Either 'user' or 'assistant'
        content (str): Message content
        timestamp (str): ISO 8601 formatted timestamp
        model (Optional[str]): Model identifier (for assistant messages)
    """
    timestamp: str
    model: Optional[str] = None

    def __post_init__(self):
        if self.role not in ("user", "assistant"):
            raise ValueError("ChatMessage role must be 'user' or 'assistant'")
        # Validate timestamp format (basic check)
        try:
            datetime.fromisoformat(self.timestamp.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError("Timestamp must be in ISO 8601 format")

    @classmethod
    def from_user(cls, content: str, timestamp: Optional[str] = None) -> 'ChatMessage':
        """
        Create a user message with current timestamp.
        
        Args:
            content (str): User message content
            timestamp (Optional[str]): ISO timestamp (auto-generated if None)
            
        Returns:
            ChatMessage: New user message instance
        """
        if timestamp is None:
            timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        return cls(role="user", content=content, timestamp=timestamp)

    @classmethod
    def from_assistant(cls, content: str, model: str, timestamp: Optional[str] = None) -> 'ChatMessage':
        """
        Create an assistant message with current timestamp.
        
        Args:
            content (str): Assistant response content
            model (str): Model identifier
            timestamp (Optional[str]): ISO timestamp (auto-generated if None)
            
        Returns:
            ChatMessage: New assistant message instance
        """
        if timestamp is None:
            timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        return cls(role="assistant", content=content, timestamp=timestamp, model=model)