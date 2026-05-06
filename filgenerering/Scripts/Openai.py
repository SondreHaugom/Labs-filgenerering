import json
import openai
from dotenv import load_dotenv
import os
from Scripts.powerpont import create_presentation

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conversation_ID = None

tools = [
    {
        "type": "function",
        "name": "generate_presentation",
        "description": "Genererer en PowerPoint-presentasjon basert på brukerens input. Brukes når brukeren ønsker å lage en presentasjon. når funksjonen kalles kan bruker legge inn tittel og innhold selv, og presentasjonen vil bli lagret som en .pptx fil.",
        "parameters": {
            "type": "object",
            "properties": {
                "presentation_file": {
                    "type": "string",
                    "description": "Navnet på den genererte PowerPoint-filen."
                }
            },
        }
    }
]

# funksjon for å generere en presentasjon ved å kalle create_presentation fra powerpont.py
def generate_presentation():
    presentation_file = create_presentation()
    if presentation_file is None:
        return {"presentation_file": "Ingen presentasjon generert."}
    return {"presentation_file": presentation_file}


# funksjon for å holde en samtale med openai gpt-5.4
def chat_with_gpt():
    # Vi starter med ingen tidligere respons, så response_id er None
    response_id = None

    # kjører samtalen i en løkke som kjrøer fram til bruker skriver "exit", "quit" eller "q"
    while True:
        # henter bruker input
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit", "q"]: # sjekker om bruker vil avslutte samtalen
            print("Exiting chat.")
            break
        # Oppretter respons fra openai med responses api
        response = client.responses.create(
            model="gpt-5.4",
            instructions="Du er en hjelpsom assistent, om bruker sprør som du kan lage en presentasjon skal du bruke funksjonskall for å opprette fila ikke noe mer.", 
            input=user_input,
            previous_response_id=response_id,
            tools= tools
        )
        # oppdaterer response_id for neste iterasjon av løkken
        response_id = response.id
        # skriver ut responsen fra gpt
        print(f"GPT: {response.output_text}")

        while any(item.type == "function_call" for item in response.output):
            
            input_list = []

            for item in response.output:
                if item.type == "function_call":
                    print(f"Kaller funksjonen ---> {item.name}")

                if item.name == "generate_presentation":
                    result = generate_presentation()

                    input_list.append({
                        "type": "function_call_output", 
                        "call_id": item.call_id, 
                        "output": json.dumps(result)    
                    })

                    response = client.responses.create(
                        model="gpt-5.4",
                        input=input_list,
                        previous_response_id=response_id,
                        tools= tools
                    )
                    response_id = response.id
                    print(f"GPT: {response.output_text}")

# starter chatten når scriptet kjøres direkte
if __name__ == "__main__":
    print("Starting chat with GPT. Type 'exit', 'quit', or 'q' to end the chat.")
    chat_with_gpt()