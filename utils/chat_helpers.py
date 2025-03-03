def format_conversation(conversation_history):
    return "\n".join(
        [f"{msg['role'].capitalize()}:{msg['content']}" for msg in conversation_history]
    )