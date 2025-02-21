import requests
import telebot
from telebot import types
import uuid
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import requests
import telebot
import os
from tempfile import NamedTemporaryFile
import os
import re
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# កំណត់ Token សម្រាប់ Telegram Bot របស់អ្នក
BOT_TOKEN = '7427603339:AAEJqyEyindaAVXeldrW4MBVAZ6wnWVi9js'
bot = telebot.TeleBot(BOT_TOKEN)

ADMIN_ID = 6248649930

# Function to download TikTok video and audio using an external API
def download_tiktok_media(url):
    api_url = f"https://tele-social.vercel.app/down?url={url}"
    try:
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status"):
                video_url = data["data"]["video"]
                audio_url = data["data"]["audio"]
                creator_name = data["creator"]["name"]
                profile_photo = data["creator"]["profile_photo"]
                total_views = data["details"]["total_views"]
                total_likes = data["details"]["total_likes"]
                video_duration = data["details"]["video_duration"]
                
                return {
                    "video_url": video_url,
                    "audio_url": audio_url,
                    "creator_name": creator_name,
                    "profile_photo": profile_photo,
                    "total_views": total_views,
                    "total_likes": total_likes,
                    "video_duration": video_duration
                }
            else:
                return {"error": "មិនអាចទាញយកទិន្នន័យពី TikTok បានទេ"}
        else:
            return {"error": "មានបញ្ហាក្នុងការទាញយកទិន្នន័យ"}
    except Exception as e:
        print(f"Error downloading TikTok media: {e}")
        return {"error": "មានបញ្ហាក្នុងការទាញយកទិន្នន័យ"}











CHANNEL_USERNAME = "MRX_STORE12"  # Channel username
USER_DATA_FILE = "user_data.json"  # ឯកសារ​សម្រាប់ផ្ទុក​ទិន្នន័យ​អ្នកប្រើ

# Function សម្រាប់អានទិន្នន័យពី user_data.json
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Function សម្រាប់រក្សាទុកទិន្នន័យ users
def save_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Function ពិនិត្យថា user បាន join channel ឬអត់
def is_member(user_id):
    try:
        chat_member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username if message.from_user.username else "No Username"
    
    # បើក user_data.json និងរក្សាទុក user ថ្មី
    user_data = load_user_data()
    if user_id not in user_data:
        user_data[user_id] = {"username": username, "balance": 0}
        save_user_data(user_data)

    # ផ្ញើសារ Welcome
    photo_url = "https://envs.sh/QSc.jpg"
    caption = "🔰 សូមស្វាគមន៍មកកាន់ Robot!\n\nទាញយកសំឡេង វីដេអូ និងរូបភាពពីវេទិកាពេញនិយមជាច្រើនតាមរយៈមនុស្សយន្តដ៏ងាយស្រួលនេះ!\n\nផ្ញើរ link 🔗 -----> បាន Video 🎬 🎥\n\nអរគុណសម្រាប់ការគាំទ្ររបស់អ្នក! 🙋‍♂️💞"

    markup = InlineKeyboardMarkup()
    btn_channel = InlineKeyboardButton("ចូលរួមជាមួយយើងឥឡូវនេះ! 🚀", url=f"https://t.me/{CHANNEL_USERNAME}")
    markup.add(btn_channel)

    bot.send_photo(message.chat.id, photo_url, caption=caption, reply_markup=markup)




# Handle message from the user (only for links starting with https://vt.tiktok.com/)
@bot.message_handler(func=lambda message: message.text.startswith(("https://vt.tiktok.com/", "https://www.tiktok.com/")))
def handle_message(message):
    url = message.text
    
    # Notify the user that the bot is processing the request
    bot.send_message(message.chat.id, "កំពុងទាញយកទិន្នន័យ...")
    
    # Directly pass the shortened TikTok link to the download function
    result = download_tiktok_media(url)
    if "error" in result:
        bot.reply_to(message, result["error"])
    else:
        # Create Caption for Video
        caption = (
            f"🎥 Creator: {result['creator_name']}\n"
            f"👁️ Views: {result['total_views']}\n"
            f"👍 Likes: {result['total_likes']}\n"
            f"⏳ Duration: {result['video_duration']} seconds\n"
        )
        
        # Send Video to the user
        bot.send_video(
            chat_id=message.chat.id,
            video=result["video_url"],
            caption=caption,
            parse_mode="HTML"
        )
        
        # Send Audio to the user
        bot.send_audio(
            chat_id=message.chat.id,
            audio=result["audio_url"],
            title=f"{result['creator_name']} - Audio",
            caption="🎵 អូឌីយ៉ូ TikTok"
        )
        
        


import os
import re
import yt_dlp
import telebot  # Import telebot from pytelegrambotapi




# 🛠️ Create download folder
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# 🔹 Path to cookies file
COOKIES_FILE = "cookies.txt"  # Ensure this file exists in the same directory as your script

# 🔹 Function to clean filenames
def clean_filename(filename):
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)  # Replace special characters
    filename = re.sub(r'[\U00010000-\U0010FFFF]', '', filename)  # Remove emojis
    filename = re.sub(r'\s+', '_', filename)  # Replace spaces with "_"
    return filename.strip()

# 🔹 Function to download media using yt-dlp with cookies
def download_media(url, format_type="audio"):
    try:
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'progress_hooks': [lambda d: print(f"\rDownloading {d['filename']}: {d.get('downloaded_bytes', 0)} bytes", end="") if d['status'] == 'downloading' else None],
            'cookiefile': COOKIES_FILE,  # Use cookies.txt for authentication
        }

        if format_type == "audio":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        elif format_type == "video":
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if format_type == "audio":
                filename = filename.replace('.webm', '.mp3').replace('.m4a', '.mp3')  # Adjust extension for audio
            return filename, info["title"]
    except Exception as e:
        print(f"Error downloading with yt-dlp: {e}")
        return None, None

# 🎯 Handle YouTube links
@bot.message_handler(func=lambda message: "youtube.com" in message.text or "youtu.be" in message.text)
def handle_youtube_link(message):
    url = message.text
    chat_id = message.chat.id

    bot.send_message(chat_id, "⏳ កំពុងទាញយកទិន្នន័យ... សូមរង់ចាំ!")

    # Check if cookies file exists
    if not os.path.exists(COOKIES_FILE):
        bot.send_message(chat_id, "❌ មិនអាចរកឃើញ cookies.txt! សូមផ្តល់ឯកសារនេះដើម្បីបន្ត។")
        return

    # Download audio
    audio_path, title = download_media(url, format_type="audio")
    if not audio_path or not title:
        bot.send_message(chat_id, "❌ មានបញ្ហា! មិនអាចទាញយកបានទេ។ សូមពិនិត្យ cookies.txt ឬ URL។")
        return

    safe_title = clean_filename(title)
    caption = (
        f"🎵 **ចំណងជើង:** {title}\n"
        f"🔗 **ប្រភព:** {url}\n"
    )

    # Send the audio file
    with open(audio_path, "rb") as audio:
        bot.send_document(chat_id, audio, caption=caption, parse_mode="Markdown")

    # Clean up
    os.remove(audio_path)
    bot.send_message(chat_id, "✅ បានទាញយក និងផ្ញើជូនអ្នករួចរាល់!")


        
# Function to download Pinterest media (video or image) using an external API
def download_pinterest_media(url):
    api_url = f"https://tele-social.vercel.app/down?url={url}"
    try:
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status"):
                platform = data.get("platform", "Unknown")
                
                if platform == "Pinterest":
                    # Handle Pinterest media (video or image)
                    media_url = data["url"]
                    filename = data["filename"]
                    credit = data["Credit"]
                    
                    return {
                        "platform": platform,
                        "media_url": media_url,
                        "filename": filename,
                        "credit": credit
                    }
                else:
                    return {"error": f"មិនគាំទ្របណ្តាញ {platform} នេះទេ"}
            else:
                return {"error": "មិនអាចទាញយកទិន្នន័យពី Pinterest បានទេ"}
        else:
            return {"error": "មានបញ្ហាក្នុងការទាញយកទិន្នន័យ"}
    except Exception as e:
        print(f"Error downloading Pinterest media: {e}")
        return {"error": "មានបញ្ហាក្នុងការទាញយកទិន្នន័យ"}


# Handle message from the user (for Pinterest links)
@bot.message_handler(func=lambda message: message.text.startswith(("https://pin.it/", "https://www.pinterest.com/")))
def handle_message(message):
    url = message.text
    
    # Notify the user that the bot is processing the request
    bot.send_message(message.chat.id, "កំពុងទាញយកទិន្នន័យ...")
    
    # Pass the link to the download function
    result = download_pinterest_media(url)
    if "error" in result:
        bot.reply_to(message, result["error"])
    else:
        # Handle Pinterest media (video or image)
        media_url = result["media_url"]
        filename = result["filename"]
        credit = result["credit"]
        
        if filename.endswith(".mp4"):
            # Send Video for Pinterest
            bot.send_video(
                chat_id=message.chat.id,
                video=media_url,
                caption=f"🎥 Pinterest Video\ncredit: @MRX_MEDIA_BOT",
                parse_mode="HTML"
            )
        elif filename.endswith(".jpg") or filename.endswith(".png"):
            # Send Image for Pinterest
            bot.send_photo(
                chat_id=message.chat.id,
                photo=media_url,
                caption=f"🖼️ Pinterest Image\ncredit: @MRX_MEDIA_BOT",
                parse_mode="HTML"
            )
            
            
            
            







# Function to download Instagram media (video or image) using an external API
def download_instagram_media(url):
    api_url = f"https://tele-social.vercel.app/down?url={url}"
    try:
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status"):
                platform = data.get("platform", "Unknown")
                
                if platform == "Instagram":
                    # Handle Instagram media (video or image)
                    media_data_list = data["data"]
                    
                    return {
                        "platform": platform,
                        "media_data": media_data_list
                    }
                else:
                    return {"error": f"មិនគាំទ្របណ្តាញ {platform} នេះទេ"}
            else:
                return {"error": "មិនអាចទាញយកទិន្នន័យពី Instagram បានទេ"}
        else:
            return {"error": "មានបញ្ហាក្នុងការទាញយកទិន្នន័យ"}
    except Exception as e:
        print(f"Error downloading Instagram media: {e}")
        return {"error": "មានបញ្ហាក្នុងការទាញយកទិន្នន័យ"}



# Handle message from the user (for Instagram links)
@bot.message_handler(func=lambda message: message.text.startswith(("https://www.instagram.com/p/", "https://www.instagram.com/reel/")))
def handle_message(message):
    url = message.text
    
    # Notify the user that the bot is processing the request
    bot.send_message(message.chat.id, "កំពុងទាញយកទិន្នន័យ...")
    
    # Determine if the link is for an image or video
    if url.startswith("https://www.instagram.com/p/"):
        media_type = "image"
    elif url.startswith("https://www.instagram.com/reel/"):
        media_type = "video"
    
    # Pass the link to the download function
    result = download_instagram_media(url)
    if "error" in result:
        bot.reply_to(message, result["error"])
    else:
        # Handle Instagram media (video or image)
        media_data_list = result["media_data"]
        
        for media_data in media_data_list:
            thumbnail = media_data.get("thumbnail")
            media_url = media_data.get("url")
            
            if media_type == "video":
                # Download the video file to a temporary location
                try:
                    video_response = requests.get(media_url, stream=True)
                    if video_response.status_code == 200:
                        # Save the video to a temporary file
                        with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                            temp_file.write(video_response.content)
                            temp_file_path = temp_file.name
                        
                        # Send the video directly to the user
                        with open(temp_file_path, 'rb') as video_file:
                            bot.send_video(
                                chat_id=message.chat.id,
                                video=video_file,
                                caption="🎥 វីដេអូ Instagram",
                                parse_mode="HTML"
                            )
                        
                        # Delete the temporary video file after sending
                        os.remove(temp_file_path)
                    else:
                        bot.reply_to(message, "មិនអាចទាញយកវីដេអូបានទេ។")
                except Exception as e:
                    print(f"Error sending video: {e}")
                    bot.reply_to(message, "មានបញ្ហាក្នុងការផ្ញើវីដេអូ។")
            elif media_type == "image":
                # Send Image for Instagram
                bot.send_photo(
                    chat_id=message.chat.id,
                    photo=media_url,
                    caption="🖼️ រូបភាព Instagram",
                    parse_mode="HTML"
                )











# Function to download Facebook media (video or image) using an external API
def download_facebook_media(url):
    api_url = f"https://tele-social.vercel.app/down?url={url}"
    try:
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status"):
                platform = data.get("platform", "Unknown")
                
                if platform == "Facebook":
                    # Handle Facebook media (video or image)
                    media_data_list = data["data"]
                    
                    return {
                        "platform": platform,
                        "media_data": media_data_list
                    }
                else:
                    return {"error": f"មិនគាំទ្របណ្តាញ {platform} នេះទេ"}
            else:
                return {"error": "មិនអាចទាញយកទិន្នន័យពី Facebook បានទេ"}
        else:
            return {"error": "មានបញ្ហាក្នុងការទាញយកទិន្នន័យ"}
    except Exception as e:
        print(f"Error downloading Facebook media: {e}")
        return {"error": "មានបញ្ហាក្នុងការទាញយកទិន្នន័យ"}



# Handle message from the user (for Facebook links)
@bot.message_handler(func=lambda message: message.text.startswith("https://www.facebook.com/"))
def handle_message(message):
    url = message.text
    
    # Notify the user that the bot is processing the request
    bot.send_message(message.chat.id, "កំពុងទាញយកទិន្នន័យ...")
    
    # Pass the link to the download function
    result = download_facebook_media(url)
    if "error" in result:
        bot.reply_to(message, result["error"])
    else:
        # Handle Facebook media (video or image)
        media_data_list = result["media_data"]
        
        # Select the highest resolution video (HD if available)
        selected_media = None
        for media_data in media_data_list:
            resolution = media_data.get("resolution", "").lower()
            if "720p" in resolution or "hd" in resolution:
                selected_media = media_data
                break
        
        # If no HD video is found, select the first video
        if not selected_media and media_data_list:
            selected_media = media_data_list[0]
        
        if selected_media:
            thumbnail = selected_media.get("thumbnail")
            media_url = selected_media.get("url")
            resolution = selected_media.get("resolution", "Unknown")
            
            # Prepare caption
            caption = (
                f"<b>🎥 វីដេអូ Facebook ({resolution})</b>\n\n"
                f'<a href="{media_url}">ចុចទីនេះដើម្បីទាញយក</a>\n\n'
                f"⚠️ មូលហេតុ: ទំហំឯកសារធំ ដូច្នេះ bot មិនអាចផ្ញើវីដេអូដោយផ្ទាល់បានទេ។"
            )
            
            # Check if caption exceeds Telegram's limit (1024 characters)
            if len(caption) <= 1024:
                try:
                    bot.send_photo(
                        chat_id=message.chat.id,
                        photo=thumbnail,
                        caption=caption,
                        parse_mode="HTML"
                    )
                except Exception as e:
                    bot.reply_to(message, f"មានបញ្ហាក្នុងការផ្ញើរូបថត: {e}")
            else:
                # Create a temporary text file with the download link
                try:
                    with NamedTemporaryFile(delete=False, mode='w', suffix=".txt") as temp_file:
                        temp_file.write(f"Download Link: {media_url}")
                        temp_file_path = temp_file.name
                    
                    # Send the thumbnail
                    bot.send_photo(
                        chat_id=message.chat.id,
                        photo=thumbnail,
                        caption="⚠️ អត្ថបទវែងពេក។ សូមមើលឯកសារដើម្បីទាញយកវីដេអូ។",
                        parse_mode="HTML"
                    )
                    
                    # Send the text file with the download link
                    with open(temp_file_path, 'rb') as file:
                        bot.send_document(
                            chat_id=message.chat.id,
                            document=file,
                            caption="ឯកសារដែលមានតំណភ្ជាប់ទាញយក"
                        )
                    
                    # Delete the temporary file after sending
                    os.remove(temp_file_path)
                except Exception as e:
                    bot.reply_to(message, f"មានបញ្ហាក្នុងការផ្ញើឯកសារ: {e}")
        else:
            bot.reply_to(message, "មិនមានវីដេអូដែលអាចទាញយកបានទេ។")








# Function to fetch data from the API
def fetch_account_info(id_ff):
    api_url = f"https://wlx-demon-info.vercel.app/profile_info?uid={id_ff}&region=sg&key=wlx_demon"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to convert Unix timestamp to readable date
def convert_unix_to_date(unix_time):
    try:
        # Convert Unix timestamp to a readable date format
        return datetime.utcfromtimestamp(int(unix_time)).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        return "❌ មិនអាចបំប្លែងពេលវេលាបាន"

# Handle messages that contain only numbers (9-10 digits)
@bot.message_handler(regexp=r'^\d{9,11}$')
def handle_id(message):
    id_ff = message.text.strip()
    
    # Fetch account info from the API
    account_info = fetch_account_info(id_ff)
    
    if account_info:
        # Extract relevant data and format it in Khmer with emojis
        account_name = account_info.get("AccountInfo", {}).get("AccountName", "❌ មិនមានពត៌មាន")
        account_level = account_info.get("AccountInfo", {}).get("AccountLevel", "❌ មិនមានពត៌មាន")
        guild_name = account_info.get("GuildInfo", {}).get("GuildName", "❌ មិនមានពត៌មាន")
        credit_score = account_info.get("creditScoreInfo", {}).get("creditScore", "❌ មិនមានពត៌មាន")
        account_likes = account_info.get("AccountInfo", {}).get("AccountLikes", "❌ មិនមានពត៌មាន")
        account_region = account_info.get("AccountInfo", {}).get("AccountRegion", "❌ មិនមានពត៌មាន")
        account_signature = account_info.get("socialinfo", {}).get("AccountSignature", "❌ មិនមានពត៌មាន")
        
        # Extract additional information: Level, Last Login, Create Time
        level = account_info.get("captainBasicInfo", {}).get("level", "❌ មិនមានពត៌មាន")
        last_login_at = account_info.get("captainBasicInfo", {}).get("lastLoginAt", "❌ មិនមានពត៌មាន")
        create_at = account_info.get("captainBasicInfo", {}).get("createAt", "❌ មិនមានពត៌មាន")
        
        # Convert Unix timestamps to readable dates
        last_login_date = convert_unix_to_date(last_login_at)
        create_date = convert_unix_to_date(create_at)
        
        # Prepare the response message in Khmer with emojis
        response_message = (
            f"👤 ឈ្មោះគណនី: {account_name} 🏆\n"
            f"📊 កម្រិតគណនី: {account_level} ⭐️\n"
            f"👥 ឈ្មោះសហគមន៍: {guild_name} 🏰\n"
            f"💯 ពិន្ទុឥណទាន: {credit_score} 💳\n"
            f"👍 ចំនួនចូលចិត្ត: {account_likes} ❤️\n"
            f"📍 តំបន់: {account_region} 🌍\n"
            f"📝 ហត្ថលេខា: {account_signature} ✒️\n"
            f"🌟 កម្រិតរបស់ Caption: {level} ⭐️\n"
            f"📅 ចុងក្រោយបាន Login: {last_login_date} 🕒\n"
            f"⏰ បង្កើតគណនីនៅ: {create_date} 📅\n"
        )
        
        # Create inline buttons
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        
        # Add a button to redirect to the channel
        channel_button = InlineKeyboardButton("ទៅ Channel @a", url="https://t.me/a")
        
        # Add a "More" button to show full JSON data
        more_button = InlineKeyboardButton("More", callback_data=f"more_{id_ff}")
        
        markup.add(channel_button, more_button)
        
        # Send the response back to the user with inline buttons
        bot.reply_to(message, response_message, reply_markup=markup)
    else:
        response_message = "❌ មិនអាចទទួលពត៌មានគណនីបានទេ។ សូមព្យាយាមម្តងទៀត!"
        bot.reply_to(message, response_message)

# Handle callback queries for the "More" button
@bot.callback_query_handler(func=lambda call: call.data.startswith("more_"))
def handle_more_callback(call):
    # Extract the ID from the callback data
    id_ff = call.data.split("_")[1]
    
    # Fetch account info from the API again
    account_info = fetch_account_info(id_ff)
    
    if account_info:
        # Convert the entire JSON data into a formatted string
        formatted_data = json.dumps(account_info, indent=4, ensure_ascii=False)
        
        # Prepare the response message
        response_message = (
            f"ទិន្នន័យពេញលេងរបស់ ID {id_ff}:\n\n"
            f"```json\n{formatted_data}\n```"
        )
    else:
        response_message = "❌ មិនអាចទទួលពត៌មានគណនីបានទេ។ សូមព្យាយាមម្តងទៀត!"
    
    # Send the response back to the user
    bot.send_message(call.message.chat.id, response_message, parse_mode='Markdown')
    


# Dictionary to store pending messages for confirmation
pending_messages = {}


# Handle "Send Message" action
@bot.message_handler(func=lambda message: message.text == "📩 ផ្ញើសារ" and message.from_user.id == ADMIN_ID)
def send_message_prompt(message):
    msg = bot.send_message(message.chat.id, "សូមបញ្ចូលអត្ថបទសារដែលអ្នកចង់ផ្ញើ (អាចបន្ថែមអ៊ីមូជិចបាន):")
    bot.register_next_step_handler(msg, preview_message)

# Preview message before sending
def preview_message(message):
    try:
        # Store the message for confirmation
        msg_id = str(uuid.uuid4())
        pending_messages[msg_id] = message  # Store full message object

        # Ask if admin wants to add inline buttons
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("បន្ថែម Inline Button", "បញ្ចូលសារដោយគ្មាន Button")
        bot.send_message(message.chat.id, "តើអ្នកចង់បន្ថែម inline button ទេ?", reply_markup=markup)
        bot.register_next_step_handler(message, lambda m: handle_button_decision(m, msg_id))
    except Exception as e:
        bot.send_message(message.chat.id, f"កំហុស: {str(e)}")

# Handle button decision
def handle_button_decision(message, msg_id):
    if message.text == "បន្ថែម Inline Button":
        msg = bot.send_message(message.chat.id, "សូមបញ្ចូល URL (ឧទាហរណ៍៖ link គ្រប់ប្រភេទ):")
        bot.register_next_step_handler(msg, lambda m: add_inline_button(m, msg_id))
    else:
        # Proceed without adding buttons
        ask_for_confirmation(message, msg_id)

# Add inline button to the message
def add_inline_button(message, msg_id):
    try:
        # Check if the input is a valid URL
        if message.text.startswith("https://"):
            button_url = message.text.strip()
            button_text = "ចុចដើម្បីមើល"  # Default button text
        else:
            # If the input is not a valid URL, ask for a valid URL
            bot.send_message(message.chat.id, "សូមបញ្ចូលតែ URL ត្រឹមត្រូវ (ឧទាហរណ៍៖ https://t.me/tupup)។")
            return

        # Create inline button
        inline_markup = types.InlineKeyboardMarkup()
        inline_markup.add(types.InlineKeyboardButton(text=button_text, url=button_url))

        # Store the inline markup with the message
        pending_messages[msg_id].reply_markup = inline_markup

        # Ask for confirmation
        ask_for_confirmation(message, msg_id)
    except Exception as e:
        bot.send_message(message.chat.id, f"កំហុស: {str(e)}")

# Ask for confirmation before sending
def ask_for_confirmation(message, msg_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("✅ ផ្ញើសារ", "❌ បោះបង់")
    bot.send_message(message.chat.id, "តើអ្នកចង់ផ្ញើសារនេះដែរឬទេ?", reply_markup=markup)
    bot.register_next_step_handler(message, lambda m: handle_send_confirmation(m, msg_id))

# Handle message confirmation or cancellation
def handle_send_confirmation(message, msg_id):
    if message.text == "✅ ផ្ញើសារ":
        # Get the last pending message ID
        msg = pending_messages[msg_id]

        # Ask if the admin wants to pin the message
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📌 Pin សារ", "🚫 កុំ Pin")
        bot.send_message(message.chat.id, "តើអ្នកចង់ pin សារនេះជាមួយអ្នកប្រើទេ?", reply_markup=markup)
        bot.register_next_step_handler(message, lambda m: handle_pin_decision(m, msg_id, msg))
    elif message.text == "❌ បោះបង់":
        # Cancel the message sending
        bot.send_message(message.chat.id, "ការផ្ញើសារត្រូវបានបោះបង់។")
        send_welcome(message)

# Handle pin decision
def handle_pin_decision(message, msg_id, msg):
    if message.text == "📌 Pin សារ":
        pin_message = True
    else:
        pin_message = False

    # Start sending the message to all users
    bot.send_message(message.chat.id, "ផ្ញើសារទៅកាន់អ្នកប្រើប្រាស់ទាំងអស់...")
    send_message_to_all_users(message, msg, pin_message)

    # Remove the message from pending messages after sending
    del pending_messages[msg_id]

# Function to create ASCII bar chart
def create_ascii_bar_chart(success_percentage, failed_percentage):
    # Define the length of the bar (e.g., 20 characters)
    bar_length = 20

    # Calculate the number of blocks for each percentage
    success_blocks = int((success_percentage / 100) * bar_length)
    failed_blocks = int((failed_percentage / 100) * bar_length)

    # Create the bar using ASCII characters
    success_bar = '█' * success_blocks
    failed_bar = '░' * failed_blocks

    # Combine the bars with labels
    bar_chart = (
        f"ជោគជ័យ: {success_bar} {success_percentage:.2f}%\n"
        f"បរាជ័យ: {failed_bar} {failed_percentage:.2f}%"
    )

    return bar_chart

# Send message to all users (supports text, voice, video, photo, document)
def send_message_to_all_users(admin_message, msg, pin_message=False):
    try:
        # Load user data from the file
        with open('user_data.json', 'r') as f:
            users = json.load(f)

        total_users = len(users)
        successful = 0
        failed = 0

        # Detect content type (text, voice, video, photo, document)
        content_type = msg.content_type
        caption = msg.caption if hasattr(msg, 'caption') else None

        # Send the appropriate message based on content type
        for user_id, user_data in users.items():
            try:
                if content_type == 'text':
                    sent_message = bot.send_message(user_id, msg.text, reply_markup=msg.reply_markup)
                elif content_type == 'voice':
                    sent_message = bot.send_voice(user_id, msg.voice.file_id, caption=caption, reply_markup=msg.reply_markup)
                elif content_type == 'video':
                    sent_message = bot.send_video(user_id, msg.video.file_id, caption=caption, reply_markup=msg.reply_markup)
                elif content_type == 'photo':
                    sent_message = bot.send_photo(user_id, msg.photo[-1].file_id, caption=caption, reply_markup=msg.reply_markup)
                elif content_type == 'document':
                    sent_message = bot.send_document(user_id, msg.document.file_id, caption=caption, reply_markup=msg.reply_markup)

                # Pin the message if requested
                if pin_message:
                    bot.pin_chat_message(user_id, sent_message.message_id)

                successful += 1
            except telebot.apihelper.ApiException:
                failed += 1

        # Calculate percentages
        success_percentage = (successful / total_users) * 100
        failed_percentage = (failed / total_users) * 100

        # Create ASCII bar chart
        bar_chart = create_ascii_bar_chart(success_percentage, failed_percentage)

        # Send the summary with ASCII bar chart to the admin
        summary_message = (
            f"សារបានផ្ញើទៅ {successful}/{total_users} អ្នកប្រើប្រាស់។\n"
            f"ភាគរយជោគជ័យ: {success_percentage:.2f}% | ភាគរយបរាជ័យ: {failed_percentage:.2f}%\n\n"
            f"សសរភាគរយ:\n{bar_chart}"
        )
        bot.send_message(admin_message.chat.id, summary_message)

        # Run start_command after sending the summary
        send_welcome(admin_message)

    except Exception as e:
        bot.send_message(admin_message.chat.id, f"កំហុស: {str(e)}")
        # Run start_command even if there's an error
        send_welcome(admin_message)

                
                
        

# Run the bot
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling()
