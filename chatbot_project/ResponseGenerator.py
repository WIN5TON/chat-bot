import random


class ResponseGenerator:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base

    def generate_response(self, message, context):
        """Генерує відповідь на основі вхідного повідомлення."""
        if "інформація про замовлення" in message:
            return self.knowledge_base.get_order_info(context.get("order_id", "Невідомо"))

        elif "змінити адресу" in message:
            return self.knowledge_base.update_address(
                order_id=context.get("order_id"),
                new_address=context.get("new_address"),
                new_city=context.get("new_city"),
                new_point=context.get("new_point")
            )

        elif "пункти видачі" in message:
            city = context.get("city", "Невідомо")
            points = self.knowledge_base.get_delivery_points(city)
            return f"Доступні пункти видачі в {city}: {', '.join(points)}" if points else f"Немає доступних пунктів видачі для міста {city}."

        return random.choice([
            "Перепрошую, я не розумію вашого запиту. Спробуйте ще раз.",
            "Не зовсім зрозумів вас, будь ласка, уточніть.",
            "Ой, що-то я заплутався, давайте спробуємо ще раз!"
        ])