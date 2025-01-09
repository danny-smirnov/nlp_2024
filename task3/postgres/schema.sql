-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create sample table
CREATE TABLE wiki_headers (
    id SERIAL PRIMARY KEY,
    url text NOT NULL,
    title text NOT NULL,
    embedding vector(768) NOT NULL
);
