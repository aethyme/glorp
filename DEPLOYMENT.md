# Deploying Flask App on Vercel with Supabase

This guide will help you deploy your Flask birthday app on Vercel with a Supabase database.

## Prerequisites

1. **Supabase Project**: Make sure your Supabase project is set up and running
2. **GitHub Account**: You'll need a GitHub account to connect to Vercel
3. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)

## Step 1: Prepare Your Supabase Environment Variables

1. Go to your Supabase dashboard → Settings → API
2. Copy your **Project URL** and **anon public key**
3. Create a strong **SECRET_KEY** for Flask sessions

## Step 2: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard (Recommended)

1. **Push your code to GitHub**:

   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Connect to Vercel**:

   - Go to [vercel.com](https://vercel.com) and sign in
   - Click "New Project"
   - Import your GitHub repository
   - Select the repository containing your Flask app

3. **Configure Environment Variables**:

   - In the Vercel project settings, go to "Environment Variables"
   - Add the following variables:
     ```
     SUPABASE_URL=https://your-project-id.supabase.co
     SUPABASE_KEY=your_anon_public_key_here
     SECRET_KEY=your-secret-key-here
     ```

4. **Deploy**:
   - Click "Deploy"
   - Vercel will automatically build and deploy your app

### Option B: Deploy via Vercel CLI

1. **Install Vercel CLI**:

   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:

   ```bash
   vercel login
   ```

3. **Deploy**:

   ```bash
   vercel
   ```

4. **Set Environment Variables**:
   ```bash
   vercel env add SUPABASE_URL
   vercel env add SUPABASE_KEY
   vercel env add SECRET_KEY
   ```

## Step 3: Configure Custom Domain (Optional)

1. In your Vercel dashboard, go to your project settings
2. Click "Domains"
3. Add your custom domain and follow the DNS configuration instructions

## Step 4: Test Your Deployment

1. Visit your deployed URL (e.g., `https://your-app.vercel.app`)
2. Test the login functionality
3. Create a test post to verify Supabase connection
4. Test image uploads (note: these will be temporary on Vercel)

## Important Notes for Vercel Deployment

### File Uploads

- **Temporary Storage**: File uploads on Vercel are stored in `/tmp` and are **temporary**
- **Alternative Solutions**: Consider using:
  - Supabase Storage for file uploads
  - Cloudinary or AWS S3 for image storage
  - Remove file upload functionality for serverless deployment

### Static Files

- Static files (images, CSS, JS) should be in the `static/` folder
- Vercel will serve them automatically
- For champion icons, consider using a CDN or external storage

### Environment Variables

- Never commit `.env` files to your repository
- Set all environment variables in Vercel dashboard
- Use different values for development and production

## Troubleshooting

### Common Issues:

1. **"Module not found" errors**:

   - Make sure all dependencies are in `requirements.txt`
   - Check that `gunicorn` is included

2. **Environment variables not working**:

   - Verify variables are set in Vercel dashboard
   - Check variable names match your code exactly

3. **Database connection errors**:

   - Verify Supabase URL and key are correct
   - Check that your Supabase project is active
   - Ensure Row Level Security (RLS) policies are configured

4. **File upload issues**:
   - Remember that `/tmp` storage is temporary on Vercel
   - Consider implementing Supabase Storage for permanent file storage

### Getting Help:

- [Vercel Documentation](https://vercel.com/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

## Security Best Practices

1. **Environment Variables**: Never expose sensitive keys in your code
2. **CORS**: Configure CORS properly if needed
3. **HTTPS**: Vercel provides HTTPS by default
4. **Rate Limiting**: Consider implementing rate limiting for your API endpoints

## Monitoring and Analytics

1. **Vercel Analytics**: Enable in your project settings
2. **Supabase Dashboard**: Monitor database usage and performance
3. **Error Tracking**: Consider adding error tracking services

## Cost Considerations

- **Vercel**: Free tier includes 100GB bandwidth and 100GB storage
- **Supabase**: Free tier includes 500MB database and 1GB file storage
- **Scaling**: Both services auto-scale based on usage
