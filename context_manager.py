from typing import List, Dict
import json
from pathlib import Path

### TODO: Rework the messages attribute to put it in a separate class with type-hints ==> better to work with in the IDE
### TODO: WIP keep pushing the save and load methods for the context manager

class ContextManager:
  
  """
  Manages conversation context for chat interactions.
  Attributes:
    messages: Context's full conversation with roles (user,assistant,system) specified for each messages (List[Dict])
      - role (str): Either 'user', 'assistant' or 'system'
      - content (str): the message content
  """
  
  def __init__(self):
    
    self.save_dir = Path.home()/".aulaf"
    self.save_dir.mkdir(exist_ok=True)
    
    self.context_file = self.save_dir/"current_context.json"
    
    self.messages: List[Dict] = []
    
    self.load()
    
    
  def add_messages(self, role:str, content:str):
    """
    Adds a single message to the conversation context.
    Args:
      self : select the current instance of context_manager
      role : the role of that specific message (user,assistant or system)
      content : the content of this single message
    """
    self.messages.append({"role": role, "content": content})
    self.save()
  
  def get_messages(self) -> List[Dict]:
    """
    Retrieves the current conversation context.
    Args:
      self : select the current instance of context_manager
    
    Returns:
      Dict with all the current conversation and the roles (user, assistant, system) specified for each one of the messages
    """
    Allmessages = [{"role": msg["role"], "content": msg["content"]} for msg in self.messages]
    return Allmessages
  
  def clear_messages(self):
    """Clears the conversation context."""
    self.messages = []
  
  def save(self):
    """Save the Context localy"""
    try:
      with open(self, "w", encoding='utf-8') as output_file_name:
        
        json.dump({
          'messages': self.messages
        }, output_file_name, indent=2, ensure_ascii=False)
    except IOError as e:
      print(f"Error when saving : {e}")
      print("Aborting Save ...")
  
  def load(self):
    if self.context_file.exists():
      try:
        with open(self,"r", encoding='utf-8') as file_to_load:
          data = json.load(file_to_load)
          self.messages = data.get('messages',[])
      except:
        print ("There isn't any context loaded. Creating one ...")
        self.messages = []
      
    