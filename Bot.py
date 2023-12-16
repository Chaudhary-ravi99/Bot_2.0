import imageio
import subprocess
import numpy as np
import telebot
import os
from PIL import Image
from telebot import types
from telebot import util
import requests
from telebot.types import InputFile
import zipfile
from io import BytesIO
import random
import string
from sticker_sticker_pack_cache import add_data_to_json, get_user_data, delete_data_from_json

TOKEN = os.getenv('TELEGRAM_BOT_API_ID')
bot = telebot.TeleBot(TOKEN)
bot_info = bot.get_me()
bot_username = bot_info.username

user_states = {}
user_data = {}
HOME, STICKER_PACK_TITLE, APNG_TO_WEBM, ADD_STICKER, ADD_LINK_STICKER, DELPACK, STICKER_DOWNLOAD, DELSTICKER = range(8)
send_st_pack_link_text = telebot.types.ForceReply(input_field_placeholder="🔗 Pᴀsᴛᴇ Yᴏᴜʀ Sᴛɪᴄᴋᴇʀ Pᴀᴄᴋ Lɪɴᴋ Hᴇʀᴇ:")
sticker_pack_cre_mess = "🔥 Sᴛɪᴄᴋᴇʀ Pᴀᴄᴋ Cʀᴇᴀᴛᴇᴅ."
jinxx_mess_start = """
𝗔𝗣𝗡𝗚 𝗧𝗢 𝗪𝗘𝗕𝗠 𝗕𝗢𝗧 𝗕𝗬 👾𝗝𝗜𝗡𝗫𝗫


✨ Cʀᴇᴀᴛᴇ A Nᴇᴡ Sᴛɪᴄᴋᴇʀ Pᴀᴄᴋ: /newpack

🗑 Dᴇʟᴇᴛᴇ A Pᴀᴄᴋ: /delpack

💟 Aᴅᴅ A Sᴛɪᴄᴋᴇʀ Tᴏ Aɴ Exɪsᴛɪɴɢ Pᴀᴄᴋ: /addsticker

🚮 Rᴇᴍᴏᴠᴇ A Sᴛɪᴄᴋᴇʀ Fʀᴏᴍ Aɴ Exɪsᴛɪɴɢ Pᴀᴄᴋ: /delsticker

🔁 Aᴘɴɢ Tᴏ Wᴇʙᴍ Cᴏɴᴠᴇʀᴛ: /apngtowebm

📥 Sᴛɪᴄᴋᴇʀ Dᴏᴡɴʟᴏᴀᴅᴇʀ: /stickerdownload

❌ Cᴀɴᴄᴇʟ Tʜᴇ Cᴜʀʀᴇɴᴛ Oᴘᴇʀᴀᴛɪᴏɴ: /cancel
"""




def check_link(message):
    if "https://t.me/addstickers/" in message:
        hs72bsiqjb = True
    else:
        hs72bsiqjb = False
    return hs72bsiqjb

def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

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

@bot.message_handler(content_types=['document'], func=lambda message: user_states.get(message.chat.id) == APNG_TO_WEBM)
def handle_document(message):
    if message.document.mime_type == 'video/webm':
        try:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message, f"🍥 Pʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ APNG ғɪʟᴇ...")
            file_info = bot.get_file(message.document.file_id)
            bot.send_chat_action(message.chat.id, 'upload_document')
            downloaded_file = bot.download_file(file_info.file_path)
            f72hs = message.from_user.id
            with open(f"{f72hs}.apng", "wb") as file:
                file.write(downloaded_file)
        except Exception as e:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, e)
        try:
            sticker_main_size = get_apng_size(f"{f72hs}.apng")
            webm_size, new_width, new_height = apng_to_webm(f"{f72hs}.apng", f"{f72hs}.webm", sticker_main_size)
        # Send the WebM file
            with open(f"{f72hs}.webm", 'rb') as sticker_file:
                bot.send_chat_action(message.chat.id, 'upload_document')
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
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, "🔘 Cʟɪᴄᴋ Tʜᴇ Bᴜᴛᴛᴏɴ Tᴏ Vɪsɪᴛ Tʜᴇ Pʀᴇᴠɪᴇᴡ Pᴀɢᴇ:", reply_markup=markup)
            # Send the size information
                size_info = f"📏 WᴇʙM Sɪᴢᴇ: {webm_size} bytes\n📏 Rᴇsɪᴢᴇᴅ Dɪᴍᴇɴsɪᴏɴs: {new_width}x{new_height}"
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, size_info, reply_to_message_id=sent_message.message_id)

        except Exception as e:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, e)

        try:
            os.remove(f"{f72hs}.apng")
            os.remove(f"{f72hs}.webm")
        except Exception as e:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, e)

    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, "❌ Oɴʟʏ Sᴜᴘᴘᴏʀᴛ Wᴇʙᴍ Fɪʟᴇs. Pʟᴇᴀsᴇ Uᴘʟᴏᴀᴅ A Vᴀʟɪᴅ Wᴇʙᴍ Fɪʟᴇ.", parse_mode="Markdown")


@bot.message_handler(commands=['cancel', 'start'])
def start_fun(message):
    bot.send_chat_action(message.chat.id, 'typing') 
    user_id = str(message.from_user.id)
    result_data = get_user_data(user_id)
    user_states[message.chat.id] = HOME
    if result_data:
        formatted_links = [f'[▒ 🖇 𝗦𝘁𝗶𝗰𝗸𝗲𝗿 𝗣𝗮𝗰𝗸 𝗟𝗶𝗻𝗸 ▒]({link})' for link in result_data]
        result = "\n".join(formatted_links)
        bot.send_message(message.chat.id, f"{jinxx_mess_start}\n⚡⃨ 𝗖⃨𝗥⃨𝗘⃨𝗔⃨𝗧⃨𝗘⃨𝗗⃨ 𝗦⃨𝗧⃨𝗜⃨𝗖⃨𝗞⃨𝗘⃨𝗥⃨ 𝗣⃨𝗔⃨𝗖⃨𝗞⃨ 𝗟⃨𝗜⃨𝗦⃨𝗧⃨\n{result}", parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, f"{jinxx_mess_start}", parse_mode="Markdown")

    
@bot.message_handler(commands=['newpack'])
def create_sticker_pack(message):
    user_states[message.chat.id] = STICKER_PACK_TITLE
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "📂 Sᴇɴᴅ Wᴇʙᴍ Sᴛɪᴄᴋᴇʀ Fɪʟᴇ")
        
@bot.message_handler(commands=['apngtowebm'])
def create_sticker_pack(message):
    user_states[message.chat.id] = APNG_TO_WEBM
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "📂 Sᴇɴᴅ APNG Fɪʟᴇ")



@bot.message_handler(commands=['delsticker'])
def create_sticker_pack(message):
    user_states[message.chat.id] = DELSTICKER
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "💟 Sᴇɴᴅ Sᴛɪᴄᴋᴇʀ")

@bot.message_handler(content_types=['sticker'], func=lambda message: user_states.get(message.chat.id) == DELSTICKER)
def handle_sticker(message):
    sticker_id = message.sticker.file_id
    try:
        bot.delete_sticker_from_set(sticker_id)
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, "👍 I Hᴀᴠᴇ Dᴇʟᴇᴛᴇᴅ Tʜᴀᴛ Sᴛɪᴄᴋᴇʀ Fᴏʀ Yᴏᴜ, Iᴛ Wɪʟʟ Sᴛᴏᴘ Bᴇɪɴɢ Aᴠᴀɪʟᴀʙʟᴇ Tᴏ Tᴇʟᴇɢʀᴀᴍ Usᴇʀs Wɪᴛʜɪɴ Aɴ Hᴏᴜʀ.")
    except telebot.apihelper.ApiException as e:
        if "STICKERSET_INVALID" in str(e):
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, f"😢 Tʜɪs Mᴇᴛʜᴏᴅ Tᴏ Dᴇʟᴇᴛᴇ A Sᴛɪᴄᴋᴇʀ Fʀᴏᴍ A Sᴇᴛ Cʀᴇᴀᴛᴇᴅ Bʏ Tʜᴇ Bᴏᴛ.", parse_mode="Markdown")
        elif "STICKERSET_NOT_MODIFIED" in str(e):
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, "👍 I Hᴀᴠᴇ Dᴇʟᴇᴛᴇᴅ Tʜᴀᴛ Sᴛɪᴄᴋᴇʀ Fᴏʀ Yᴏᴜ, Iᴛ Wɪʟʟ Sᴛᴏᴘ Bᴇɪɴɢ Aᴠᴀɪʟᴀʙʟᴇ Tᴏ Tᴇʟᴇɢʀᴀᴍ Usᴇʀs Wɪᴛʜɪɴ Aɴ Hᴏᴜʀ.")
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, f"```ERROR {e}```", parse_mode="Markdown")
    



    
@bot.message_handler(commands=['stickerdownload'])
def create_sticker_pack(message):
    user_states[message.chat.id] = STICKER_DOWNLOAD
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "💟 Sᴇɴᴅ Sᴛɪᴄᴋᴇʀ")
    
@bot.message_handler(content_types=['sticker'], func=lambda message: user_states.get(message.chat.id) == STICKER_DOWNLOAD)
def handle_sticker(message):
    sticker_id = message.sticker.file_id
    user_id_jinxx = message.from_user.id
    # Get sticker file details
    file_info = bot.get_file(sticker_id)
    file_path = file_info.file_path
    content_type = file_info.file_path.split('.')[-1]
    webm_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    response = requests.get(webm_url)
    stucker_don_file_name = f"{user_id_jinxx}sticker.{content_type}"
    with open(stucker_don_file_name, "wb") as webm_file:
        webm_file.write(response.content)
    if content_type == "tgs":
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.write(stucker_don_file_name)
        zip_buffer.seek(0)
        random_file_name = generate_random_string()
        bot.send_chat_action(message.chat.id, 'upload_document')
        bot.send_document(message.chat.id, zip_buffer, caption='Sticker in Zip', visible_file_name=f'{random_file_name}.zip')
    
    with open(stucker_don_file_name, 'rb') as sticker_file:
        bot.send_chat_action(message.chat.id, 'upload_document')
        bot.send_video(message.chat.id, sticker_file, caption=stucker_don_file_name)
    try:
        os.remove(stucker_don_file_name)
    except Exception as e:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, e)





@bot.message_handler(commands=['delpack'])
def create_sticker_pack(message):
    user_states[message.chat.id] = DELPACK
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "🔗 Sᴇɴᴅ Sᴛɪᴄᴋᴇʀ Pᴀᴄᴋ Lɪɴᴋ", reply_markup=send_st_pack_link_text)
    
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == DELPACK)
def handle_document4(message):
    sticker_pack_link = message.text
    if check_link(sticker_pack_link):
        sticker_pack_name = sticker_pack_link.split("/")[-1]
        try:
            bot.delete_sticker_set(sticker_pack_name)
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message( message.chat.id, jinxx_mess_start, parse_mode="Markdown")
            user_states[message.chat.id] = HOME
        except telebot.apihelper.ApiException as e:
            if "STICKERSET_INVALID" in str(e):
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, f"😢 Tʜɪs Mᴇᴛʜᴏᴅ Tᴏ Dᴇʟᴇᴛᴇ A Sᴛɪᴄᴋᴇʀ Pᴀᴄᴋ Fʀᴏᴍ A Sᴇᴛ Cʀᴇᴀᴛᴇᴅ Bʏ Tʜᴇ Bᴏᴛ.", parse_mode="Markdown")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, f"```ERROR {e}```", parse_mode="Markdown")
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, f"❌ Tʜᴇ Mᴇssᴀɢᴇ Is Nᴏᴛ A Vᴀʟɪᴅ URL.\n\n```🔗Exᴀᴍᴘʟᴇ: https://t.me/addstickers/STICKER_NAME```", parse_mode="Markdown", reply_markup=send_st_pack_link_text)






@bot.message_handler(commands=['addsticker'])
def create_sticker_pack(message):
    user_states[message.chat.id] = ADD_LINK_STICKER
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "🔗 Sᴇɴᴅ Sᴛɪᴄᴋᴇʀ Pᴀᴄᴋ Lɪɴᴋ", reply_markup=send_st_pack_link_text)

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == ADD_LINK_STICKER)
def handle_document3(message):
    user_id = str(message.from_user.id)
    if user_id not in user_data:
        user_data[user_id] = {}

    user_data[user_id]['add_link_sticker'] = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "📂 Sᴇɴᴅ Wᴇʙᴍ Sᴛɪᴄᴋᴇʀ Fɪʟᴇ")
    user_states[message.chat.id] = ADD_STICKER
    

    
@bot.message_handler(content_types=['document'], func=lambda message: user_states.get(message.chat.id) == ADD_STICKER)
def handle_document2(message):
    user_id = str(message.from_user.id)
    
    if user_id not in user_data:
        user_data[user_id] = {}
        
    sticker_pack_link = user_data[user_id]['add_link_sticker']
    
    sticker_pack_name = sticker_pack_link.split("/")[-1]
    bot.add_sticker_to_set(user_id, sticker_pack_name, emojis="⭐", webm_sticker=message.document.file_id)
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, f"Sticker Added {sticker_pack_link}")
    bot.send_message(message.chat.id, "📂 Sᴇɴᴅ Wᴇʙᴍ Sᴛɪᴄᴋᴇʀ Fɪʟᴇ")
    
    
    
@bot.message_handler(content_types=['document'], func=lambda message: user_states.get(message.chat.id) == STICKER_PACK_TITLE)
def handle_document2(message):
    if message.document.mime_type == 'video/webm':
        try:
            user_id = str(message.from_user.id)
            random_result = generate_random_string()
            sticker_pack_name = f'{random_result}_by_{bot_username}'
            print(sticker_pack_name)
            sticker_pack_title = '👩🏻‍💻 Sᴛɪᴄᴋᴇʀ Pᴀᴄᴋ Cʀᴇᴀᴛᴇᴅ Bʏ @ApngTowebm_Bot'
            pack_info = bot.create_new_sticker_set(
            user_id=user_id,
            name=sticker_pack_name,
            title=sticker_pack_title,
            emojis=['⭐'],
            webm_sticker=message.document.file_id
            )
            bot.send_chat_action(message.chat.id, 'typing')
            sticker_pack_link = f"https://t.me/addstickers/{sticker_pack_name}"
            bot.send_message(message.chat.id, f"{sticker_pack_cre_mess} {sticker_pack_link}")
            add_data_to_json(user_id, sticker_pack_link)
            user_states[message.chat.id] = HOME
        except telebot.apihelper.ApiException as e:
            if "invalid sticker set name is specified" in str(e):
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, "Network Error Send Again")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, e)
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, "📂 Sᴇɴᴅ Wᴇʙᴍ Sᴛɪᴄᴋᴇʀ Fɪʟᴇ")
    
    
if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)
