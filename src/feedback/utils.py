async def generate_feedback_message(feedback: dict):
    return (
        f"📝 <b>Тема обращения:</b> {feedback.get('title')}\n"
        f"📄 <b>Текст обращения:</b> {feedback.get('text')}\n\n"
        f"👨‍💼 <b>Дата отправления:</b> {feedback.get('created_at')}"
    )
