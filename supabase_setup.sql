-- Create posts table
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    username VARCHAR(80) NOT NULL,
    color VARCHAR(20) DEFAULT 'blue',
    lp INTEGER DEFAULT 0,
    image_filename VARCHAR(256),
    profile_picture VARCHAR(256)
);

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_posts_username ON posts(username);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Enable Row Level Security (RLS)
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create policies for posts table
-- Allow all users to read posts
CREATE POLICY "Allow public read access to posts" ON posts
    FOR SELECT USING (true);

-- Allow authenticated users to insert their own posts
CREATE POLICY "Allow users to insert their own posts" ON posts
    FOR INSERT WITH CHECK (true);

-- Allow users to update their own posts
CREATE POLICY "Allow users to update their own posts" ON posts
    FOR UPDATE USING (auth.uid()::text = username);

-- Allow users to delete their own posts
CREATE POLICY "Allow users to delete their own posts" ON posts
    FOR DELETE USING (auth.uid()::text = username);

-- Create policies for users table
-- Allow all users to read users
CREATE POLICY "Allow public read access to users" ON users
    FOR SELECT USING (true);

-- Allow users to insert new users
CREATE POLICY "Allow users to insert new users" ON users
    FOR INSERT WITH CHECK (true); 