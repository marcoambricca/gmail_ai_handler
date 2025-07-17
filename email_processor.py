from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from email_sender import send_email
from db_functions import available_functions, function_specs

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

load_dotenv()

def process_email(email_text, email_sender, email_subject):
    try:
        initial_response = client.chat.completions.create(model="gpt-4o",
        messages=[
            {"role": "system", "content": "Sos un asistente por email de atención al cliente para una tienda online."},
            {"role": "user", "content": email_text}
        ],
        functions=function_specs,
        function_call="auto")

        choice = initial_response.choices[0].message

        if choice.function_call:
            func_name = choice.function_call.name
            func_args = json.loads(choice.function_call.arguments)

            if func_name in available_functions:
                result = available_functions[func_name](**func_args)

                final_response = client.chat.completions.create(model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Sos un asistente por email de atención al cliente."},
                    {"role": "user", "content": email_text},
                    {"role": "function", "name": func_name, "content": json.dumps(result)}
                ])
                reply_text = final_response.choices[0].message.content
            else:
                reply_text = "Disculpas, no pude acceder a la información solicitada."
        else:
            reply_text = choice.content

        # Email final
        formatted_reply = f"""
Hola,

{reply_text}

Saludos,
SumoTech
"""
        send_email(to=email_sender, subject=email_subject, body=formatted_reply)

    except Exception as e:
        print(f"Error al procesar el email: {e}")

