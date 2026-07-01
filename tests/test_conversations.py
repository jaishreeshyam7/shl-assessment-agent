from app.core.conversation_manager import ConversationManager

manager = ConversationManager()

history = [
    {
        "role": "user",
        "content": "Need assessment"
    }
]

print(manager.analyze(history))