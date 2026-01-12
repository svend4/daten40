/**
 * Тестовый JavaScript модуль
 * @module TestUtilities
 * @version 1.0.0
 * @created 2026-01-12
 */

// Класс для работы с тестовыми данными
class TestDataManager {
    constructor() {
        this.data = [];
        this.config = {
            autoSave: true,
            validateData: true,
            maxItems: 1000
        };
    }

    /**
     * Добавляет элемент в хранилище
     * @param {Object} item - Объект для добавления
     * @returns {boolean} - Успешность операции
     */
    addItem(item) {
        if (this.config.validateData && !this.validateItem(item)) {
            console.error('Неверный формат данных:', item);
            return false;
        }

        if (this.data.length >= this.config.maxItems) {
            console.warn('Достигнут максимум элементов');
            return false;
        }

        this.data.push({
            ...item,
            id: this.generateId(),
            timestamp: Date.now()
        });

        if (this.config.autoSave) {
            this.save();
        }

        return true;
    }

    /**
     * Получает элемент по ID
     * @param {string} id - Идентификатор
     * @returns {Object|null} - Найденный элемент или null
     */
    getItem(id) {
        return this.data.find(item => item.id === id) || null;
    }

    /**
     * Фильтрует данные по критериям
     * @param {Function} predicate - Функция фильтрации
     * @returns {Array} - Отфильтрованные данные
     */
    filter(predicate) {
        return this.data.filter(predicate);
    }

    /**
     * Удаляет элемент по ID
     * @param {string} id - Идентификатор
     * @returns {boolean} - Успешность операции
     */
    removeItem(id) {
        const initialLength = this.data.length;
        this.data = this.data.filter(item => item.id !== id);
        
        if (this.data.length < initialLength) {
            if (this.config.autoSave) this.save();
            return true;
        }
        
        return false;
    }

    /**
     * Обновляет элемент
     * @param {string} id - Идентификатор
     * @param {Object} updates - Обновления
     * @returns {boolean} - Успешность операции
     */
    updateItem(id, updates) {
        const index = this.data.findIndex(item => item.id === id);
        
        if (index === -1) return false;
        
        this.data[index] = {
            ...this.data[index],
            ...updates,
            updatedAt: Date.now()
        };
        
        if (this.config.autoSave) this.save();
        
        return true;
    }

    /**
     * Проверяет корректность элемента
     */
    validateItem(item) {
        return item && typeof item === 'object' && !Array.isArray(item);
    }

    /**
     * Генерирует уникальный ID
     */
    generateId() {
        return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Сохраняет данные
     */
    save() {
        try {
            localStorage.setItem('testData', JSON.stringify(this.data));
            console.log('Данные сохранены');
        } catch (error) {
            console.error('Ошибка сохранения:', error);
        }
    }

    /**
     * Загружает данные
     */
    load() {
        try {
            const saved = localStorage.getItem('testData');
            if (saved) {
                this.data = JSON.parse(saved);
                console.log('Данные загружены');
            }
        } catch (error) {
            console.error('Ошибка загрузки:', error);
        }
    }

    /**
     * Очищает все данные
     */
    clear() {
        this.data = [];
        if (this.config.autoSave) this.save();
        console.log('Данные очищены');
    }

    /**
     * Возвращает статистику
     */
    getStats() {
        return {
            total: this.data.length,
            maxItems: this.config.maxItems,
            percentage: (this.data.length / this.config.maxItems * 100).toFixed(2) + '%'
        };
    }
}

// Вспомогательные функции
const utils = {
    /**
     * Форматирует дату
     */
    formatDate(timestamp) {
        return new Date(timestamp).toLocaleString('ru-RU');
    },

    /**
     * Генерирует случайное число
     */
    randomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    },

    /**
     * Задержка выполнения
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },

    /**
     * Debounce функция
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { TestDataManager, utils };
}

// Пример использования
if (typeof window !== 'undefined') {
    window.TestDataManager = TestDataManager;
    window.testUtils = utils;
    
    console.log('✅ Test utilities загружены');
}