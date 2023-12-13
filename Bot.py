import imageio
import subprocess
import numpy as np
import telebot
import os
from PIL import Image
from telebot import types

TOKEN = os.getenv('TELEGRAM_BOT_API_ID')
bot = telebot.TeleBot(TOKEN)

user_states = {}
HOME, SET_SIZE = range(2)

def resize_apng_jinxx(larger_value, Num, Num2):
    if larger_value == Num:
        new_width = 512
        new_height = int(Num2 * (512 / Num))
        jinxx = f"{new_width}x{new_height}"
    elif larger_value == Num2:
        new_height = 512
        new_width = int(Num * (512 / Num2))
        jinxx = f"{new_width}x{new_height}"
    return jinxx


def get_apng_size(apng_path):
    apng_frames = imageio.mimread(apng_path)
    first_frame_size = apng_frames[0].shape[:2]

    Num = first_frame_size[1]
    Num2 = first_frame_size[0]

    larger_value = max(Num, Num2)
    ttttt = resize_apng_jinxx(larger_value, Num, Num2)
    apng_jinxx_size = ttttt
    return ttttt


def apng_to_webm(input_apng, output_webm, sticker_main_size):
    apng_frames = imageio.mimread(input_apng)

    original_height, original_width, _ = apng_frames[0].shape
    aspect_ratio = original_width / original_height

    new_width = int(sticker_main_size.split('x')[0])
    new_height = int(new_width / aspect_ratio)

    resized_frames = [Image.fromarray(frame).resize((new_width, new_height)) for frame in apng_frames]

    ffmpeg_cmd = [
        'ffmpeg',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-s', f'{new_width}x{new_height}',
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
            process.stdin.write(np.array(frame).tobytes())

    except BrokenPipeError:
        pass

    finally:
        process.stdin.close()
        process.wait()

    # Get the size of the created WebM file
    webm_size = os.path.getsize(output_webm)

    return webm_size, new_width, new_height


@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        bot.reply_to(message, f"🍥 Pʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ APNG ғɪʟᴇ...")

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        f72hs = message.from_user.id

        with open(f"{f72hs}.apng", "wb") as file:
            file.write(downloaded_file)

    except Exception as e:
        bot.send_message(message.chat.id, e)

    try:
        sticker_main_size = get_apng_size(f"{f72hs}.apng")
        webm_size, new_width, new_height = apng_to_webm(f"{f72hs}.apng", f"{f72hs}.webm", sticker_main_size)

        # Send the WebM file
        with open(f"{f72hs}.webm", 'rb') as sticker_file:
            sent_message = bot.send_document(message.chat.id, sticker_file)
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
            
            # Send the size information
            size_info = f"WebM Size: {webm_size} bytes\nResized Dimensions: {new_width}x{new_height}"
            bot.send_message(message.chat.id, size_info, reply_to_message_id=sent_message.message_id)

    except Exception as e:
        bot.send_message(message.chat.id, e)

    try:
        os.remove(f"{f72hs}.apng")
        os.remove(f"{f72hs}.webm")
    except Exception as e:
        bot.send_message(message.chat.id, e)


bot.polling()