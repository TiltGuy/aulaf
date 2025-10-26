import typer
from rich.console import Console
import ollama
from typing import Optional
from context_manager import ContextManager

### Typer app setup
app = typer.Typer()
### Rich console setup
console = Console()
### Context Manager setup
context = ContextManager()

@app.command()
def chat(
    message: Optional[str] = typer.Argument(None, help="The message to send to the model."),
    model: str = typer.Option("mistral", "--model", "-m")
    
):
    """💬 Chat with Aulaf (AUtomated Largely Adaptable Friend)"""
    
    if not message:
      user_input = ""
      #Interactive mode
      console.print("[bold green]Entering interactive chat mode. Type 'exit' to quit.[/bold green]")
      
      ## Add system prompt to respond only in user's language
      system_prompt = "You are a helpful assistant. Respond only in the user's language without providing translations."
      context.add_messages("system", system_prompt)
      while True:
        try:
          ## Simple input prompt
          user_input = console.input("[bold blue] Your message: ")
          ## if user wants to exit
          if user_input.lower() in ['exit', 'quit', '/q']:
            console.print("[bold red] Quitting Aulaf ... Farewell friend.")
            break
          
          context.add_messages("user", user_input)
          messages = context.get_messages()
          ### Just a debug line to see messages in context
          ##print("[dim] messages in Context : " + str(messages))
          
          with console.status("[dim]Aulaf is thinking..."):
            response = ollama.chat(model=model, messages = messages)
            
          answer = response['message']['content']
          context.add_messages("assistant", answer)
          console.print(f"[bold orange1] Aulaf: {answer}")
          
        except KeyboardInterrupt:
          console.print("[bold red] Quitting Aulaf ... Farewell friend.")
          break
        except Exception as e:
          console.print(f"[bold red] An error occurred: {e}")
    else:
      #One Single message mode
      with console.status("[dim]Aulaf is thinking..."):
        response = ollama.chat(model=model, messages=[{"role": "user", "content": message}])
            
      answer = response['message']['content']
      console.print(f"[bold orange1]Aulaf: {answer}")

@app.command()
def clear():
  """Clear the conversation context."""
  context.clear_messages()
  console.print("[bold green]Conversation context cleared.")
  
@app.command()
def status():
  """Show the current conversation context."""
  nb_messages = len(context.get_messages())
  console.print(f"[bold green]There are currently {nb_messages} in the conversation context.")


if __name__ == "__main__":
  app()