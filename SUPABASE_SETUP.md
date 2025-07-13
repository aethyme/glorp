# Supabase Setup Guide

This guide will help you connect your birthday posts project to Supabase.

## Step 1: Create a Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign up/sign in
2. Click "New Project"
3. Choose your organization
4. Enter a project name (e.g., "birthday-posts")
5. Enter a database password (save this!)
6. Choose a region close to you
7. Click "Create new project"

## Step 2: Get Your Supabase Credentials

1. In your Supabase dashboard, go to Settings → API
2. Copy the following values:
   - **Project URL** (looks like: `https://your-project-id.supabase.co`)
   - **anon public key** (starts with `eyJ...`)

## Step 3: Set Up Your Database Tables

1. In your Supabase dashboard, go to the SQL Editor
2. Copy and paste the contents of `supabase_setup.sql` into the editor
3. Click "Run" to create the tables and policies

## Step 4: Configure Your Environment Variables

1. Open the `.env` file in your project
2. Replace the placeholder values with your actual Supabase credentials:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_anon_public_key_here
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-ID].supabase.co:5432/postgres

# Flask Configuration
SECRET_KEY=your-secret-key-here
```

**Note:** For the `DATABASE_URL`, you can find the connection string in your Supabase dashboard under Settings → Database → Connection string → URI.

## Step 5: Install Dependencies

Run the following command to install the required packages:

```bash
pip install -r requirements.txt
```

## Step 6: Test Your Connection

1. Start your Flask app:

   ```bash
   python app.py
   ```

2. Visit `http://localhost:5000` in your browser
3. Try creating a post to test the connection

## Troubleshooting

### Common Issues:

1. **"Invalid API key" error**: Make sure you're using the `anon public` key, not the `service_role` key
2. **"Connection refused" error**: Check that your `SUPABASE_URL` is correct
3. **"Table doesn't exist" error**: Make sure you ran the SQL setup script in Step 3

### Getting Help:

- Check the Supabase documentation: [supabase.com/docs](https://supabase.com/docs)
- Check the Flask-Supabase integration: [github.com/supabase-community/supabase-py](https://github.com/supabase-community/supabase-py)

## Security Notes

- Never commit your `.env` file to version control
- The `anon public` key is safe to use in client-side code
- Row Level Security (RLS) is enabled on your tables for additional security
