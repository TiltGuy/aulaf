from typing import List, Dict

class ContextManager:
  
  """Manages conversation context for chat interactions."""
  
  def __init__(self):
    self.messages: List[Dict] = []
    
  def add_messages(self, role:str, content:str):
    """"Adds a message to the conversation context."""
    self.messages.append({"role": role, "content": content})
  
  def get_messages(self) -> List[Dict]:
    """Retrieves the current conversation context."""
    Allmessages = [{"role": msg["role"], "content": msg["content"]} for msg in self.messages]
    return Allmessages
  
  def clear_messages(self):
    """Clears the conversation context."""
    self.messages = []