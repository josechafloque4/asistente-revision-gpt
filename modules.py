def check_access(clave_usuario):
    return clave_usuario == "1978"

def build_prompt(system_instructions, user_message):
    return [
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": user_message}
    ]