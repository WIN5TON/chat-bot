import os
import time

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
        print(f"\033[1;34m[Користувач]:\033[0m {user_message}")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.show_main_menu()
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
