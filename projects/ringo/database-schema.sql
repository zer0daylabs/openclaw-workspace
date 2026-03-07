-- Ringo - Database Schema
-- PostgreSQL/Supabase

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (link to Supabase Auth)
CREATE TABLE public.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Projects table
CREATE TABLE public.projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'active', -- active, archived
    color TEXT,
    created_by UUID REFERENCES public.users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tasks table
CREATE TABLE public.tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES public.projects(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'todo', -- todo, in_progress, review, done
    priority TEXT DEFAULT 'medium', -- low, medium, high, critical
    due_date TIMESTAMPTZ,
    created_by UUID REFERENCES public.users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Task Assignments (many-to-many)
CREATE TABLE public.task_assignments (
    task_id UUID REFERENCES public.tasks(id) ON DELETE CASCADE,
    user_id UUID REFERENCES public.users(id),
    assigned_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (task_id, user_id)
);

-- Audit trail
CREATE TABLE public.audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name TEXT NOT NULL,
    record_id UUID NOT NULL,
    action TEXT NOT NULL, -- created, updated, deleted
    changed_by UUID REFERENCES public.users(id),
    changed_at TIMESTAMPTZ DEFAULT NOW(),
    old_values JSONB,
    new_values JSONB
);

-- Indexes for performance
CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_task_assignments_user ON task_assignments(user_id);

-- Row Level Security (RLS)
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.task_assignments ENABLE ROW LEVEL SECURITY;

-- RLS Policies - Users can see their own data and public data
CREATE POLICY "Users can view own profile"
    ON public.users FOR SELECT
    USING (auth.uid()::text = email OR id = auth.uid());

CREATE POLICY "Users can update own profile"
    ON public.users FOR UPDATE
    USING (auth.uid()::text = email);

CREATE POLICY "Users can view projects"
    ON public.projects FOR SELECT
    USING (true); -- Public projects

CREATE POLICY "Users can create projects"
    ON public.projects FOR INSERT
    WITH CHECK (auth.uid()::text = created_by::text OR true);

CREATE POLICY "Users can view tasks"
    ON public.tasks FOR SELECT
    USING (true); -- Public tasks

CREATE POLICY "Users can create tasks"
    ON public.tasks FOR INSERT
    WITH CHECK (auth.uid()::text = created_by::text OR true);

CREATE POLICY "Users can view own assignments"
    ON public.task_assignments FOR SELECT
    USING (auth.uid()::text = user_id::text OR true);

CREATE POLICY "Users can create assignments"
    ON public.task_assignments FOR INSERT
    WITH CHECK (auth.uid()::text = user_id::text OR true);

-- Seed data
INSERT INTO users (email, full_name) VALUES
    ('lauro@zeroday.com', 'Lauro - Founder'),
    ('test@zeroday.com', 'Test User');

INSERT INTO projects (name, description, color) VALUES
    ('Internal Development', 'Zer0Day Labs internal projects', '#3b82f6'),
    ('Client Work', 'External client deliverables', '#10b981'),
    ('Research', 'Research and development', '#f59e0b');

INSERT INTO tasks (project_id, title, description, priority, status) VALUES
    (1, 'Initial Setup', 'Complete Ringo project scaffolding', 'critical', 'todo'),
    (1, 'Database Schema', 'Define and implement core schema', 'high', 'todo'),
    (1, 'Authentication', 'Implement email and OAuth login', 'high', 'todo');

-- Update timestamps on changes
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON public.users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON public.projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON public.tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
