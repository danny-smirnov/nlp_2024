#!/bin/bash

# Настройки подключения к базе данных
DB_NAME="wikisearch"
DB_USER="postgres"
DB_HOST="localhost"
DB_PORT="5432"
DB_PASSWORD="postgres"

# Название таблицы и индекса
TABLE_NAME="wiki_headers"
INDEX_NAME="idx_wiki_headers_embedding"
COLUMN_NAME="embedding"

# Установить пароль для psql (можно использовать PGPASSWORD для автоматической аутентификации)
export PGPASSWORD=$DB_PASSWORD

echo "Добавление индекса для таблицы $TABLE_NAME на колонку $COLUMN_NAME"

# Подключение к базе данных и выполнение SQL команд
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME <<EOF

-- Удаляем старый индекс, если существует
DO \$\$ 
BEGIN
    IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = '$INDEX_NAME') THEN
        EXECUTE 'DROP INDEX ' || quote_ident('$INDEX_NAME');
        RAISE NOTICE 'Старый индекс $INDEX_NAME удален';
    END IF;
END \$\$;

-- Создаем новый индекс
CREATE INDEX $INDEX_NAME 
ON $TABLE_NAME USING hnsw ($COLUMN_NAME vector_cosine_ops);

-- Анализируем таблицу для оптимизации запроса
ANALYZE $TABLE_NAME;

EOF

echo "Индекс $INDEX_NAME успешно создан!"
