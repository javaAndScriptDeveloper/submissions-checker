-- Migration: 009_create_lecture_knowledge_table
-- Description: Create lecture_knowledge table for RAG-based AI reviews
CREATE TABLE lecture_knowledge (
    id SERIAL PRIMARY KEY,
    lab_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX ix_lecture_knowledge_lab_id ON lecture_knowledge(lab_id);

CREATE TRIGGER update_lecture_knowledge_updated_at
    BEFORE UPDATE ON lecture_knowledge
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
