import random
import time
import os

class KnowledgeBase:
    def __init__(self):
        self.orders = {
            "123": {"status": "доставляється", "delivery_time": "15:00", "address": "Вул. Головна 123"},
            "456": {"status": "готується", "delivery_time": "Немає", "address": "Вул. Соснова 456"},
            "789": {"status": "відправлено", "delivery_time": "18:30", "address": "Вул. Дубова 789"},
        }
        self.delivery_points = {
            "Київ": ["Пункт A", "Пункт B", "Пункт C"],
            "Львів": ["Пункт D", "Пункт E", "Пункт F"]
        }

    def get_order_info(self, order_id):
        order_id = self.normalize_order_id(order_id)
        if order_id in self.orders:
            order = self.orders[order_id]
            return (f"Замовлення {order_id}:\n"
                    f"Статус: {order['status']}\n"
                    f"Час доставки: {order['delivery_time']}\n"
                    f"Адреса: {order['address']}")
        else:
            return "Замовлення не знайдено."

    def update_address(self, order_id, new_address):
        order_id = self.normalize_order_id(order_id)
        if order_id in self.orders:
            current_address = self.orders[order_id]["address"]
            self.orders[order_id]["address"] = self.normalize_address(new_address)
            return f"Адреса успішно змінена з {current_address} на {self.orders[order_id]['address']}."
        else:
            return "Замовлення не знайдено."

    def normalize_address(self, address):
        if "Вул." in address and not address.startswith("Вул. "):
            address = address.replace("Вул.", "Вул. ")
        return address.strip()

    def normalize_order_id(self, order_id):
        return order_id.strip()

    def get_delivery_points(self, city):
        if city in self.delivery_points:
            return self.delivery_points[city]
        else:
            return None


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


class Chatbot:
    def __init__(self, response_generator):
        self.response_generator = response_generator
        self.context = {}

    def process_message(self, message):
        if "замовлення" in message:
            order_id = self.extract_order_id(message)
            if order_id:
                self.context["order_id"] = order_id

        if "змінити адресу" in message:
            new_address = self.extract_address(message)
            if new_address:
                self.context["new_address"] = new_address

        if "пункти видачі" in message:
            city = self.extract_city(message)
            if city:
                self.context["city"] = city

        response = self.response_generator.generate_response(message, self.context)
        self.send_response(response, message)

    def send_response(self, response, user_message):
        # Вивести команду користувача
        print(f"\033[1;34m[Користувач]:\033[0m {user_message}")
        
        # Чекати перед відповіддю
        time.sleep(1)

        # Очищення екрану перед виведенням відповіді
        os.system('cls' if os.name == 'nt' else 'clear')  # Очищення екрану

        # Вивести основне меню (повторно після кожного кроку)
        self.show_main_menu()

        # Вивести відповідь бота
        print(f"\033[1;32m[Бот]:\033[0m {response}")
    
    def user_input(self):
        print("\033[1;36m[Користувач]:\033[0m ", end="")
        user_message = input().strip()
        return user_message

    def show_main_menu(self):
        print("\n\033[1;33mОсь доступні команди:\033[0m")
        print("I - Інформація про замовлення")
        print("A - Змінити адресу")
        print("P - Пункти видачі")
        print("Q - Вийти з чату")
        print("-" * 40)

    def extract_order_id(self, message):
        numbers = ''.join([c for c in message if c.isdigit()])
        return numbers if numbers else None

    def extract_address(self, message):
        if "Вул." in message:
            return message.split("Вул.")[1].strip()
        return None

    def extract_city(self, message):
        if "Київ" in message:
            return "Київ"
        elif "Львів" in message:
            return "Львів"
        else:
            return None

    def run(self):
        print("\033[1;36mПривіт! Як я можу допомогти?\033[0m")
        self.show_main_menu()

        while True:
            command = self.user_input().strip().upper()

            if command == "I":
                order_id = input("Введіть номер замовлення: ").strip()
                self.context["order_id"] = order_id
                self.process_message(f"інформація про замовлення {order_id}")
            elif command == "A":
                order_id = input("Введіть номер замовлення: ").strip()
                new_address = input("Введіть нову адресу: ").strip()
                self.context["order_id"] = order_id
                self.context["new_address"] = new_address
                self.process_message(f"змінити адресу на {new_address}")
            elif command == "P":
                city = input("Введіть місто: ").strip()
                self.context["city"] = city
                self.process_message(f"пункти видачі в {city}")
            elif command == "Q":
                print("\033[1;36mДо побачення! Сподіваюся, допоміг!\033[0m")
                break
            else:
                print("\033[1;31mНевідома команда. Спробуйте ще раз.\033[0m")

if __name__ == "__main__":
    knowledge_base = KnowledgeBase()
    response_generator = ResponseGenerator(knowledge_base)
    chatbot = Chatbot(response_generator)

    chatbot.run()
