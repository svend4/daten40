#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый скрипт для проверки функциональности
Создан: 2026-01-12
"""

import json
import datetime
from typing import List, Dict, Optional


class TestDataGenerator:
    """Класс для генерации тестовых данных"""
    
    def __init__(self, seed: Optional[int] = None):
        self.seed = seed
        self.data = []
    
    def generate_user(self, user_id: int) -> Dict:
        """Генерирует тестового пользователя"""
        return {
            "id": user_id,
            "username": f"test_user_{user_id}",
            "email": f"user{user_id}@test.com",
            "created_at": datetime.datetime.now().isoformat(),
            "active": user_id % 3 != 0,
            "role": "admin" if user_id % 5 == 0 else "user"
        }
    
    def generate_batch(self, count: int = 10) -> List[Dict]:
        """Генерирует пакет тестовых данных"""
        return [self.generate_user(i) for i in range(1, count + 1)]
    
    def save_to_json(self, filename: str, data: List[Dict]) -> None:
        """Сохраняет данные в JSON файл"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Данные сохранены в {filename}")


def run_tests():
    """Запускает тесты"""
    print("Запуск тестов...")
    
    generator = TestDataGenerator(seed=42)
    test_data = generator.generate_batch(count=5)
    
    print(f"Сгенерировано {len(test_data)} тестовых записей")
    
    for user in test_data:
        print(f"  - {user['username']}: {user['email']} [{user['role']}]")
    
    return test_data


if __name__ == "__main__":
    print("="*50)
    print("Тестовый скрипт генерации данных")
    print("="*50)
    
    data = run_tests()
    
    print("\nТесты завершены успешно! ✅")