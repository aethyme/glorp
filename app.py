from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Supabase configuration
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

# Debug: Print environment variables
print(f"SUPABASE_URL: {supabase_url}")
print(f"SUPABASE_KEY: {supabase_key[:20] if supabase_key else 'None'}...")

if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

supabase: Client = create_client(supabase_url, supabase_key)

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8MB max upload size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_rank_and_lp():
    # Get all posts from Supabase
    response = supabase.table('posts').select('*').execute()
    posts = response.data
    
    total_lp = sum(post.get('lp', 0) for post in posts)
    # Determine rank and icon image
    if total_lp >= 500:
        rank = 'Challenger'
        icon = 'challenger.png'
    elif total_lp >= 250:
        rank = 'Grandmaster'
        icon = 'grandmaster.png'
    else:
        rank = 'Master'
        icon = 'master.png'
    # Calculate win/loss statistics
    wins = len([post for post in posts if post.get('color') == 'blue'])
    losses = len([post for post in posts if post.get('color') == 'red'])
    total_games = wins + losses
    win_rate = (wins / total_games * 100) if total_games > 0 else 0
    return {
        'rank': rank,
        'icon': icon,
        'lp': total_lp,
        'wins': wins,
        'losses': losses,
        'win_rate': round(win_rate)
    }

def get_post_counts():
    # Get all posts from Supabase
    response = supabase.table('posts').select('*').execute()
    posts = response.data
    
    # Count posts per username
    username_counts = {}
    for post in posts:
        username = post.get('username', '')
        username_counts[username] = username_counts.get(username, 0) + 1
    
    # Sort by count (descending)
    sorted_counts = sorted(username_counts.items(), key=lambda x: x[1], reverse=True)
    return [{'username': username, 'count': count} for username, count in sorted_counts]

def is_logged_in():
    return 'username' in session

def is_cidez():
    return session.get('username', '').lower() == 'cidez'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if not username:
            flash('Username is required.')
            return redirect(url_for('login'))
        # Allow login if username is already in session or in database
        response = supabase.table('users').select('*').eq('username', username).execute()
        existing = response.data
        
        if not existing:
            # Register new user
            supabase.table('users').insert({'username': username}).execute()
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.')
    return redirect(url_for('login'))

@app.route('/')
def home():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    # Get posts from Supabase, ordered by created_at desc
    response = supabase.table('posts').select('*').order('created_at', desc=True).execute()
    posts = response.data
    
    rank_info = get_rank_and_lp()
    post_counts = get_post_counts()
    show_confetti = is_cidez()
    champ_icons = os.listdir(os.path.join('static', 'champ_icons'))
    return render_template(
        'index.html',
        posts=posts,
        rank_info=rank_info,
        post_counts=post_counts,
        show_confetti=show_confetti,
        username=session['username'],
        champ_icons=champ_icons
    )

@app.route('/post', methods=['POST'])
def create_post():
    if not is_logged_in():
        return redirect(url_for('login'))
    content = request.form.get('content', '')
    username = session['username']
    color = request.form.get('color', 'blue')
    image_filename = None
    profile_picture = request.form.get('profile_picture', '')

    # Handle image upload
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{datetime.utcnow().timestamp()}_{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_filename = filename
    
    if not content:
        flash('Content is required.')
        return redirect(url_for('home'))
    
    # Set LP based on color. Since 'red' is the only other option, this works.
    lp = 25 if color == 'blue' else -25
    
    # Create post in Supabase
    post_data = {
        'content': content,
        'username': username,
        'color': color,
        'lp': lp,
        'image_filename': image_filename,
        'profile_picture': profile_picture,
        'created_at': datetime.utcnow().isoformat()
    }
    
    supabase.table('posts').insert(post_data).execute()
    
    return redirect(url_for('home'))

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if not is_logged_in():
        return redirect(url_for('login'))
    
    # Get post from Supabase
    response = supabase.table('posts').select('*').eq('id', post_id).execute()
    posts = response.data
    
    if not posts:
        flash('Post not found.')
        return redirect(url_for('home'))
    
    post = posts[0]
    if post['username'] != session['username']:
        flash('You can only delete your own posts.')
        return redirect(url_for('home'))
    
    # Remove image file if exists
    if post.get('image_filename'):
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post['image_filename']))
        except Exception:
            pass
    
    # Delete post from Supabase
    supabase.table('posts').delete().eq('id', post_id).execute()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True) 