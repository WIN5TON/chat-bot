import random

class ResponseGenerator:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base

    def generate_response(self, message, context):
        if "інформація про замовлення" in message:
            order_id = context.get("order_id", "Невідомо")
            return self.knowledge_base.get_order_info(order_id)

        elif "змінити адресу" in message:
            new_address = context.get("new_address", "Невідомо")
            order_id = context.get("order_id", "Невідомо")
            return self.knowledge_base.update_address(order_id, new_address)

        elif "пункти видачі" in message:
            city = context.get("city", "Невідомо")
            points = self.knowledge_base.get_delivery_points(city)
            if points:
                return f"Доступні пункти видачі в {city}: {', '.join(points)}"
            else:
                return f"Немає доступних пунктів видачі для міста {city}."

        else:
            return random.choice([
                "Перепрошую, я не розумію вашого запиту. Спробуйте ще раз.",
                "Не зовсім зрозумів вас, будь ласка, уточніте.",
                "Ой, що-то я заплутався, давайте спробуємо ще раз!"
            ])
