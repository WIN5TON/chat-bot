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
        """Повертає інформацію про замовлення за його ID."""
        order_id = self.normalize_order_id(order_id)
        order = self.orders.get(order_id)

        if order:
            return (f"Замовлення {order_id}:\n"
                    f"Статус: {order['status']}\n"
                    f"Час доставки: {order['delivery_time']}\n"
                    f"Місто: {order['місто']}\n"
                    f"Адреса: {order['address']}\n"
                    f"Пункт видачі: {order['пункт']}")
        return "Замовлення не знайдено."

    def update_address(self, order_id, new_address=None, new_city=None, new_point=None):
        """Оновлює адресу, місто та пункт видачі для замовлення."""
        order = self.orders.get(order_id)
        if not order:
            return f"Замовлення з ID {order_id} не знайдено."

        # Оновлення адреси
        if new_address:
            order["address"] = self.normalize_address(new_address)

        # Оновлення міста і пункту видачі
        if new_city:
            result = self._update_city_and_point(order, new_city, new_point)
            if result:
                return result

        # Оновлення пункту видачі (без зміни міста)
        if new_point and not new_city:
            result = self._update_point_only(order, new_point)
            if result:
                return result

        return self._build_update_message(order_id, new_address, new_city, new_point)

    def _update_city_and_point(self, order, new_city, new_point):
        order["місто"] = new_city
        if new_point and new_point not in self.delivery_points.get(new_city, []):
            return f"Пункт видачі '{new_point}' недоступний у місті {new_city}."
        order["пункт"] = new_point or self._get_default_point(new_city)
        return None

    def _update_point_only(self, order, new_point):
        """Оновлює лише пункт видачі, якщо місто не змінювалось."""
        city_points = self.delivery_points.get(order["місто"], [])
        if new_point not in city_points:
            return f"Пункт видачі '{new_point}' недоступний у місті {order['місто']}."
        order["пункт"] = new_point
        return None

    def _build_update_message(self, order_id, new_address, new_city, new_point):
        """Формує повідомлення про успішне оновлення."""
        changes = []
        if new_address:
            changes.append(f"- Адреса: {self.orders[order_id]['address']}")
        if new_city:
            changes.append(f"- Місто: {self.orders[order_id]['місто']}")
        if new_point or new_city:
            changes.append(f"- Пункт видачі: {self.orders[order_id]['пункт']}")
        return f"Зміни успішно внесено для замовлення {order_id}:\n" + "\n".join(changes)

    def normalize_address(self, address):
        """Нормалізує формат адреси."""
        if "Вул." in address and not address.startswith("Вул. "):
            address = address.replace("Вул.", "Вул. ")
        return address.strip()

    def normalize_order_id(self, order_id):
        """Нормалізує формат ID замовлення."""
        return order_id.strip()

    def get_delivery_points(self, city):
        """Повертає доступні пункти видачі для заданого міста."""
        return self.delivery_points.get(city)

    def _get_default_point(self, city):
        """Повертає перший доступний пункт видачі для міста."""
        points = self.get_delivery_points(city)
        return points[0] if points else "Немає доступних пунктів"