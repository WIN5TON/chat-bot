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
