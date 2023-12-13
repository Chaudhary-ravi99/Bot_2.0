import imageio
import subprocess
import numpy as np
import telebot
import os
from telebot import types


TOKEN = os.getenv('TELEGRAM_BOT_API_ID')
bot = telebot.TeleBot(TOKEN)

user_states = {}
HOME, SET_SIZE = range(2)

def get_apng_size(apng_path):
    apng_frames = imageio.mimread(apng_path)
    first_frame_size = apng_frames[0].shape[:2]  # Get the size of the first frame
    return f"{first_frame_size[1]}x{first_frame_size[0]}"  # Swap width and height for correct format

def apng_to_webm(input_apng, output_webm, sticker_main_size):
    apng_frames = imageio.mimread(input_apng)
    resized_frames = [frame[:int(sticker_main_size.split('x')[1]), :int(sticker_main_size.split('x')[0]), :] for frame in apng_frames]

    ffmpeg_cmd = [
        'ffmpeg',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-s', sticker_main_size,
        '-pix_fmt', 'rgba',
        '-r', '60',
        '-i', '-',
        '-c:v', 'libvpx-vp9',
        '-b:v', '256k',
        '-crf', '10',
        '-auto-alt-ref', '0',
        '-pix_fmt', 'yuva420p',
        output_webm
    ]

    process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    try:
        for frame in resized_frames:
            process.stdin.write(frame.tobytes())

    except BrokenPipeError:
        pass

    finally:
        process.stdin.close()
        process.wait()

@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        bot.reply_to(message, "🍥 Pʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ APNG ғɪʟᴇ...")
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        f72hs = message.from_user.id
        with open(f"{f72hs}.apng", "wb") as file:
            file.write(downloaded_file)
            
    except Exception as e:
        bot.send_message(message.chat.id, e)
    
    global sticker_main_size
    sticker_main_size = get_apng_size(f"{f72hs}.apng")
    apng_to_webm(f"{f72hs}.apng", f"{f72hs}.webm", sticker_main_size)
        
    
        
    try:
        with open(f"{f72hs}.webm", 'rb') as sticker_file:
            sent_message = bot.send_document(message.chat.id, open(f"{f72hs}.webm", 'rb'))
            file_id = sent_message.document.file_id
            file_path = bot.get_file(file_id).file_path
            base_url = 'https://api.telegram.org/file/bot' + TOKEN
            full_raw_link = base_url + '/' + file_path
            preju83 = f"https://jinix6.github.io/Webm_preview?video={full_raw_link}"
            
            markup = types.InlineKeyboardMarkup()
            webApp = types.WebAppInfo(preju83)
            button = types.InlineKeyboardButton(text="👁️Pʀᴇᴠɪᴇᴡ", web_app=webApp)
            markup.add(button)
            bot.send_message(message.chat.id, "🔘 Cʟɪᴄᴋ Tʜᴇ Bᴜᴛᴛᴏɴ Tᴏ Vɪsɪᴛ Tʜᴇ Pʀᴇᴠɪᴇᴡ Pᴀɢᴇ:", reply_markup=markup)
           
    except Exception as e:
        bot.send_message(message.chat.id, e)
        
    try:
        os.remove(f"{f72hs}.apng")
        os.remove(f"{f72hs}.webm")
    except Exception as e:
        bot.send_message(message.chat.id, e)


bot.polling()