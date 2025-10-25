import typer
from rich.console import Console
import ollama
from typing import Optional

app = typer.Typer()
console = Console()

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
      while True:
        try:
          ## Simple input prompt
          user_input = console.input("[bold blue] Your message: ")
          ## if user wants to exit
          if user_input.lower() in ['exit', 'quit', '/q']:
            console.print("[bold red]Quitting Aulaf ... Farewell friend.")
            break
          
          ## Add system prompt to respond only in user's language
          system_prompt = "You are a helpful assistant. Respond only in the user's language without providing translations."
          
          with console.status("[dim]Aulaf is thinking..."):
            response = ollama.chat(model=model, messages=[{"role": "system", "content": system_prompt},{"role": "user", "content": user_input}])
            
          answer = response['message']['content']
          console.print(f"[bold orange]Aulaf: {answer}")
          
        except KeyboardInterrupt:
          console.print("[bold red]Quitting Aulaf ... Farewell friend.")
          break
        except Exception as e:
          console.print(f"[bold red]An error occurred: {e}")
    else:
      #One Single message mode
      with console.status("[dim]Aulaf is thinking..."):
        response = ollama.chat(model=model, messages=[{"role": "user", "content": message}])
            
      answer = response['message']['content']
      console.print(f"[bold orange]Aulaf: {answer}")
      
if __name__ == "__main__":
  app()