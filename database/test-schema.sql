-- Тестовая база данных
-- Создана: 2026-01-12

-- Создание таблицы пользователей
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    role VARCHAR(20) DEFAULT 'user'
);

-- Создание таблицы продуктов
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы заказов
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Вставка тестовых пользователей
INSERT INTO users (username, email, password_hash, role) VALUES
('admin', 'admin@test.com', 'hash123', 'admin'),
('testuser1', 'user1@test.com', 'hash456', 'user'),
('testuser2', 'user2@test.com', 'hash789', 'user'),
('manager', 'manager@test.com', 'hash101', 'manager'),
('guest', 'guest@test.com', 'hash202', 'guest');

-- Вставка тестовых продуктов
INSERT INTO products (name, description, price, stock_quantity, category) VALUES
('Ноутбук', 'Мощный ноутбук для работы', 75000.00, 15, 'electronics'),
('Клавиатура', 'Механическая клавиатура', 5500.00, 30, 'accessories'),
('Мышь', 'Беспроводная мышь', 1200.00, 50, 'accessories'),
('Монитор', '27" 4K монитор', 35000.00, 8, 'electronics'),
('Наушники', 'Беспроводные наушники', 8900.00, 25, 'audio');

-- Вставка тестовых заказов
INSERT INTO orders (user_id, total_amount, status) VALUES
(2, 75000.00, 'completed'),
(3, 6700.00, 'pending'),
(2, 43900.00, 'shipped'),
(4, 35000.00, 'processing');

-- Примеры запросов

-- Получить всех активных пользователей
SELECT * FROM users WHERE is_active = true;

-- Получить продукты в категории electronics
SELECT * FROM products WHERE category = 'electronics' ORDER BY price DESC;

-- Получить заказы с информацией о пользователях
SELECT 
    o.id,
    o.total_amount,
    o.status,
    u.username,
    u.email
FROM orders o
JOIN users u ON o.user_id = u.id
ORDER BY o.created_at DESC;

-- Подсчитать общую стоимость заказов по пользователям
SELECT 
    u.username,
    COUNT(o.id) as order_count,
    SUM(o.total_amount) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.username
ORDER BY total_spent DESC NULLS LAST;

-- Найти продукты с низким запасом
SELECT name, stock_quantity 
FROM products 
WHERE stock_quantity < 10
ORDER BY stock_quantity ASC;