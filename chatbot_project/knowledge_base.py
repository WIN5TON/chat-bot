class KnowledgeBase:
    def __init__(self):
        self.orders = {
            "123": {"status": "доставляється", "delivery_time": "15:00", "address": "Вул. Головна 123", "місто": "Київ", "пункт": "Пункт A"},
            "456": {"status": "готується", "delivery_time": "Немає", "address": "Вул. Соснова 456", "місто": "Львів", "пункт": "Пункт D"},
            "789": {"status": "відправлено", "delivery_time": "18:30", "address": "Вул. Дубова 789", "місто": "Київ", "пункт": "Пункт B"},
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
                    f"Місто: {order['місто']}\n"
                    f"Адреса: {order['address']}\n"
                    f"Пункт видачі: {order['пункт']}")
        else:
            return "Замовлення не знайдено."


    def update_address(self, order_id, new_address=None, new_city=None, new_point=None):
        if order_id not in self.orders:
            return f"Замовлення з ID {order_id} не знайдено."

        # Оновлення адреси
        if new_address:
            self.orders[order_id]["address"] = self.normalize_address(new_address)

        # Оновлення міста
        if new_city:
            self.orders[order_id]["місто"] = new_city
            # Перевірка пункту видачі, чи він існує в новому місті
            if new_point and new_point not in self.delivery_points.get(new_city, []):
                return f"Пункт видачі '{new_point}' недоступний у місті {new_city}."
            elif not new_point:
                # Якщо пункт видачі не вказаний, вибрати перший доступний пункт
                available_points = self.get_delivery_points(new_city)
                if available_points:
                    self.orders[order_id]["пункт"] = available_points[0]
                else:
                    self.orders[order_id]["пункт"] = "Немає доступних пунктів"

        # Оновлення пункту видачі (тільки якщо місто не змінювалось)
        if new_point and not new_city:
            if new_point in self.delivery_points.get(self.orders[order_id]["місто"], []):
                self.orders[order_id]["пункт"] = new_point
            else:
                return f"Пункт видачі '{new_point}' недоступний у місті {self.orders[order_id]['місто']}."

        # Формування повідомлення про успішне оновлення
        updated_info = f"Зміни успішно внесено для замовлення {order_id}:\n"
        if new_address:
            updated_info += f"- Адреса: {self.orders[order_id]['address']}\n"
        if new_city:
            updated_info += f"- Місто: {self.orders[order_id]['місто']}\n"
        if new_point or new_city:
            updated_info += f"- Пункт видачі: {self.orders[order_id]['пункт']}\n"

        return updated_info

 
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
