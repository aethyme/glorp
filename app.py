from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from supabase import create_client, Client
import uuid
import re

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

# For Vercel deployment, use a different upload folder path
if os.getenv('VERCEL'):
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
else:
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8MB max upload size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_to_supabase_storage(file, username):
    """Upload file to Supabase Storage"""
    try:
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{username}/{uuid.uuid4()}.{file_extension}"
        print(f"Uploading {unique_filename} to Supabase Storage...")

        # Upload to Supabase Storage
        file.stream.seek(0)  # Ensure pointer is at start
        response = supabase.storage.from_('upload').upload(
            path=unique_filename,
            file=file.read(),
            file_options={"content-type": file.content_type}
        )
        print(f"Upload response: {response}")

        # Get public URL
        public_url = supabase.storage.from_('upload').get_public_url(unique_filename)
        print(f"Public URL: {public_url}")
        return public_url
    except Exception as e:
        print(f"Error uploading to Supabase Storage: {e}")
        return None

def delete_from_supabase_storage(file_url):
    """Delete file from Supabase Storage"""
    try:
        # Extract filename from URL
        filename = file_url.split('/')[-1]
        supabase.storage.from_('uploads').remove([filename])
    except Exception as e:
        print(f"Error deleting from Supabase Storage: {e}")

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

def get_champ_icons():
    """Get list of champion icons - works both locally and on Vercel"""
    champ_icons = [
        'Aatrox.png', 'Ahri.png', 'Akali.png', 'Akshan.png', 'Alistar.png', 'Ambessa.png',
        'Amumu.png', 'Anivia.png', 'Annie.png', 'Aphelios.png', 'Ashe.png', 'Aurelion_Sol.png',
        'Aurora.png', 'Azir.png', 'Bard.png', "Bel'Veth.png", 'Blitzcrank.png', 'Brand.png',
        'Braum.png', 'Briar.png', 'Caitlyn.png', 'Camille.png', 'Cassiopeia.png', "Cho'Gath.png",
        'Corki.png', 'Darius.png', 'Diana.png', 'Draven.png', 'Dr_Mundo.png', 'Ekko.png',
        'Elise.png', 'Evelynn.png', 'Ezreal.png', 'Fiddlesticks.png', 'Fiora.png', 'Fizz.png',
        'Galio.png', 'Gangplank.png', 'Garen.png', 'Gnar.png', 'Gragas.png', 'Graves.png',
        'Gwen.png', 'Hecarim.png', 'Heimerdinger.png', 'Hwei.png', 'Illaoi.png', 'Irelia.png',
        'Ivern.png', 'Janna.png', 'Jarvan_IV.png', 'Jax.png', 'Jayce.png', 'Jhin.png',
        'Jinx.png', "K'Sante.png", "Kai'Sa.png", 'Kalista.png', 'Karma.png', 'Karthus.png',
        'Kassadin.png', 'Katarina.png', 'Kayle.png', 'Kayn.png', 'Kennen.png', "Kha'Zix.png",
        'Kindred.png', 'Kled.png', "Kog'Maw.png", 'Leblanc.png', 'Lee_Sin.png', 'Leona.png',
        'Lillia.png', 'Lissandra.png', 'Lucian.png', 'Lulu.png', 'Lux.png', 'Malphite.png',
        'Malzahar.png', 'Maokai.png', 'Master_Yi.png', 'Mel.png', 'Milio.png', 'Miss_Fortune.png',
        'Mordekaiser.png', 'Morgana.png', 'Naafiri.png', 'Nami.png', 'Nasus.png', 'Nautilus.png',
        'Neeko.png', 'Nidalee.png', 'Nilah.png', 'Nocturne.png', 'Nunu.png', 'Olaf.png',
        'Orianna.png', 'Ornn.png', 'Pantheon.png', 'Poppy.png', 'Pyke.png', 'Qiyana.png',
        'Quinn.png', 'Rakan.png', 'Rammus.png', "Rek'Sai.png", 'Rell.png', 'Renata.png',
        'Renekton.png', 'Rengar.png', 'Riven.png', 'Rumble.png', 'Ryze.png', 'Samira.png',
        'Sejuani.png', 'Senna.png', 'Seraphine.png', 'Sett.png', 'Shaco.png', 'Shen.png',
        'Shyvana.png', 'Singed.png', 'Sion.png', 'Sivir.png', 'Skarner.png', 'Smolder.png',
        'Sona.png', 'Soraka.png', 'Swain.png', 'Sylas.png', 'Syndra.png', 'Tahm_Kench.png',
        'Taliyah.png', 'Talon.png', 'Taric.png', 'Teemo.png', 'Thresh.png', 'Tristana.png',
        'Trundle.png', 'Tryndamere.png', 'Twisted_Fate.png', 'Twitch.png', 'Udyr.png',
        'Urgot.png', 'Varus.png', 'Vayne.png', 'Veigar.png', "Vel'Koz.png", 'Vex.png',
        'Vi.png', 'Viego.png', 'Viktor.png', 'Vladimir.png', 'Volibear.png', 'Warwick.png',
        'Wukong.png', 'Xayah.png', 'Xerath.png', 'Xin_Zhao.png', 'Yasuo.png', 'Yone.png',
        'Yorick.png', 'Yunara.png', 'Yuumi.png', 'Zac.png', 'Zed.png', 'Zeri.png',
        'Ziggs.png', 'Zilean.png', 'Zoe.png', 'Zyra.png'
    ]
    return champ_icons

@app.template_filter('split_camel')
def split_camel(s):
    # Remove file extension if present
    s = s.rsplit('.', 1)[0]
    # Replace underscores with spaces
    return s.replace('_', ' ')

@app.template_filter('pretty_date')
def pretty_date(s):
    try:
        dt = datetime.fromisoformat(s.replace('Z', '+00:00'))
        return dt.strftime('%b %d')
    except Exception:
        return s

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
    
    # Get champion icons list
    champ_icons = get_champ_icons()
    
    # Get posts from Supabase, ordered by created_at desc
    response = supabase.table('posts').select('*').order('created_at', desc=True).execute()
    posts = response.data
    
    rank_info = get_rank_and_lp()
    post_counts = get_post_counts()
    show_confetti = is_cidez()
    
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
    image_url = None
    profile_picture = request.form.get('profile_picture', '')

    # Handle image upload - try Supabase Storage first, then local storage
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            # Try Supabase Storage first
            image_url = upload_to_supabase_storage(file, username)
            # If Supabase Storage fails, fall back to local storage
            if not image_url:
                file.stream.seek(0)
                filename = secure_filename(f"{datetime.utcnow().timestamp()}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename

    # Only require content if no image is uploaded
    if not content and not image_url and not image_filename:
        flash('Content or an image is required.')
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
        'image_url': image_url,
        'profile_picture': profile_picture,
        'created_at': datetime.utcnow().isoformat()
    }
    supabase.table('posts').insert(post_data).execute()
    return redirect(url_for('home'))

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if not is_logged_in():
        print('User not logged in')
        return redirect(url_for('login'))
    print(f'Trying to delete post with id: {post_id}')
    # Get post from Supabase
    response = supabase.table('posts').select('*').eq('id', post_id).execute()
    posts = response.data
    print(f'Posts found: {posts}')
    if not posts:
        flash('Post not found.')
        print('Post not found')
        return redirect(url_for('home'))
    post = posts[0]
    if post['username'] != session['username']:
        flash('You can only delete your own posts.')
        print('User does not own post')
        return redirect(url_for('home'))
    # Delete image from Supabase Storage if exists
    if post.get('image_url'):
        print(f'Deleting image from Supabase Storage: {post["image_url"]}')
        delete_from_supabase_storage(post['image_url'])
    # Remove local image file if exists
    if post.get('image_filename'):
        try:
            print(f'Removing local image file: {post["image_filename"]}')
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post['image_filename']))
        except Exception as e:
            print(f'Error removing local image file: {e}')
    # Delete post from Supabase
    try:
        print(f'Deleting post from Supabase with id: {post_id}')
        del_response = supabase.table('posts').delete().eq('id', post_id).execute()
        print(f'Delete response: {del_response}')
    except Exception as e:
        print(f'Error deleting post from Supabase: {e}')
        flash('Error deleting post.')
    return redirect(url_for('home'))

# WSGI application for Vercel
app.debug = True

if __name__ == '__main__':
    app.run(debug=True) 