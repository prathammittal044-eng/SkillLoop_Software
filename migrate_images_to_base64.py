import sqlite3
import os
import base64
from PIL import Image
import io

db_path = "skillloop.db"
base_dir = os.path.dirname(os.path.abspath(__file__))
uploads_dir = os.path.join(base_dir, "uploads", "profiles")

def file_to_data_url(filepath, max_dim=400, quality=85):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None
    try:
        with Image.open(filepath) as img:
            img = img.convert("RGB")
            img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=quality, optimize=True)
            b64 = base64.b64encode(buf.getvalue()).decode("ascii")
            return f"data:image/jpeg;base64,{b64}"
    except Exception as e:
        print(f"Error converting {filepath}: {e}")
        return None

def migrate():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    rows = c.execute("SELECT id, username, profile_picture, banner_image FROM users").fetchall()
    
    updated_count = 0
    for user_id, username, pic, banner in rows:
        new_pic = pic
        new_banner = banner
        
        # Check if profile_picture is a file path
        if pic and not pic.startswith("data:image/"):
            fname = os.path.basename(pic)
            fpath = os.path.join(uploads_dir, fname)
            converted = file_to_data_url(fpath, max_dim=400, quality=85)
            if converted:
                new_pic = converted
                print(f"User {username} (ID {user_id}) avatar converted ({len(converted)} chars)")
        
        # Check if banner_image is a file path
        if banner and not banner.startswith("data:image/"):
            fname = os.path.basename(banner)
            fpath = os.path.join(uploads_dir, fname)
            converted = file_to_data_url(fpath, max_dim=1200, quality=85)
            if converted:
                new_banner = converted
                print(f"User {username} (ID {user_id}) banner converted ({len(converted)} chars)")
                
        if new_pic != pic or new_banner != banner:
            c.execute("UPDATE users SET profile_picture = ?, banner_image = ? WHERE id = ?",
                      (new_pic, new_banner, user_id))
            updated_count += 1
            
    conn.commit()
    conn.close()
    print(f"Migration complete: {updated_count} users updated in database.")

if __name__ == "__main__":
    migrate()
