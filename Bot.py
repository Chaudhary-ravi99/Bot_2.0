import telebot
import os
from telebot import types
from telebot import util
import requests
from telebot.types import InputFile
import zipfile
from io import BytesIO
from jinxx.sticker_sticker_pack_cache import add_data_to_json, get_user_data, delete_data_from_json
from jinxx.others_jinxx import check_link, generate_random_string, resize_apng_jinxx, get_apng_size, apng_to_webm, gif_to_webm, check_image_type, png_to_webm, video_to_webm, get_video_size
from jinxx.jinxx_str import *
from telebot import apihelper

TOKEN = os.getenv('TELEGRAM_BOT_API_ID')
bot = telebot.TeleBot(TOKEN)
bot_info = bot.get_me()
bot_username = bot_info.username
user_states = {}
user_data = {}
saved_message_ids = []
saved_message_ids_v2 = []
HOME, STICKER_PACK_TITLE, APNG_TO_WEBM, ADD_STICKER, ADD_LINK_STICKER, DELPACK, STICKER_DOWNLOAD, DELSTICKER = range(8)
send_st_pack_link_text = telebot.types.ForceReply(input_field_placeholder="🔗 Pᴀsᴛᴇ Yᴏᴜʀ Sᴛɪᴄᴋᴇʀ Pᴀᴄᴋ Lɪɴᴋ Hᴇʀᴇ:")
command_back = telebot.types.InlineKeyboardMarkup(row_width=1)
b1 = telebot.types.InlineKeyboardButton(text="🔙 Bᴀᴄᴋ", callback_data='back')
command_back.add(b1)
command_list = telebot.types.InlineKeyboardMarkup(row_width=1)
b1 = telebot.types.InlineKeyboardButton(text="✨Cʀᴇᴀᴛᴇ A Nᴇᴡ Sᴛɪᴄᴋᴇʀ Pᴀᴄᴋ", callback_data='newpack')
b2 = telebot.types.InlineKeyboardButton(text="💟 Aᴅᴅ A Sᴛɪᴄᴋᴇʀ Tᴏ Aɴ Exɪsᴛɪɴɢ Pᴀᴄᴋ", callback_data='addsticker')
b3 = telebot.types.InlineKeyboardButton(text="🚮 Rᴇᴍᴏᴠᴇ Sᴛɪᴄᴋᴇʀ Fʀᴏᴍ Exɪsᴛɪɴɢ Pᴀᴄᴋ", callback_data='delsticker')
b4 = telebot.types.InlineKeyboardButton(text="🗑 Dᴇʟᴇᴛᴇ A Pᴀᴄᴋ", callback_data='delpack')
b5 = telebot.types.InlineKeyboardButton(text="🔁 Aᴘɴɢ, Pɴɢ, Gɪғ, Vɪᴅᴇᴏ Tᴏ Wᴇʙᴍ Cᴏɴᴠᴇʀᴛ", callback_data='apngtowebm')
b6 = telebot.types.InlineKeyboardButton(text="📥 Sᴛɪᴄᴋᴇʀ Dᴏᴡɴʟᴏᴀᴅᴇʀ", callback_data='stickerdownload')
command_list.add(b1, b2, b3, b4, b5, b6)
command_list_header_text = """
░░░░▒👾 𝗦𝗧𝗜𝗖𝗞𝗘𝗥 𝗕𝗢𝗧 0.1.8▒░░░░
▓▓▓▓Mᴀᴅᴇ Bʏ [⊏Jɪɴxx⊐](tg://user?id=6903011562) [⊏Jɪɴxx²⊐](tg://user?id=6693765228)▓▓▓▓
"""
@bot.message_handler(commands=['cancel', 'start'])
def start_fun(message):
    delete_all_saved_messages_v2(message.chat.id)
    bot.send_chat_action(message.chat.id, 'typing') 
    user_id = str(message.from_user.id)
    result_data = get_user_data(user_id)
    user_states[message.chat.id] = HOME
    if result_data:
        formatted_links = [f'[▒ 🖇 𝗦𝘁𝗶𝗰𝗸𝗲𝗿 𝗣𝗮𝗰𝗸 𝗟𝗶𝗻𝗸 ▒]({link})' for link in result_data]
        result = "\n".join(formatted_links)
        save = bot.send_message(message.chat.id, f"{command_list_header_text}\n⚡⃨ 𝗖⃨𝗥⃨𝗘⃨𝗔⃨𝗧⃨𝗘⃨𝗗⃨ 𝗦⃨𝗧⃨𝗜⃨𝗖⃨𝗞⃨𝗘⃨𝗥⃨ 𝗣⃨𝗔⃨𝗖⃨𝗞⃨ 𝗟⃨𝗜⃨𝗦⃨𝗧⃨\n{result}", reply_markup=command_list, parse_mode="Markdown")
        saved_message_ids_v2.append(save.message_id)
    else:
        save = bot.send_message(message.chat.id, command_list_header_text, reply_markup=command_list, parse_mode="Markdown")
        saved_message_ids_v2.append(save.message_id)
        
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == 'back')
def handle_call_back(call):
    user_id = str(call.from_user.id)
    result_data = get_user_data(user_id)
    user_states[call.message.chat.id] = HOME
    if result_data:
        formatted_links = [f'[▒ 🖇 𝗦𝘁𝗶𝗰𝗸𝗲𝗿 𝗣𝗮𝗰𝗸 𝗟𝗶𝗻𝗸 ▒]({link})' for link in result_data]
        result = "\n".join(formatted_links)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=f"{command_list_header_text}\n⚡⃨ 𝗖⃨𝗥⃨𝗘⃨𝗔⃨𝗧⃨𝗘⃨𝗗⃨ 𝗦⃨𝗧⃨𝗜⃨𝗖⃨𝗞⃨𝗘⃨𝗥⃨ 𝗣⃨𝗔⃨𝗖⃨𝗞⃨ 𝗟⃨𝗜⃨𝗦⃨𝗧⃨\n{result}", reply_markup=command_list, parse_mode="Markdown")
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=command_list_header_text, reply_markup=command_list, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == 'newpack')
def handle_call_newpack(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="📂 Sᴇɴᴅ Tʜᴇ Wᴇʙᴍ Sᴛɪᴄᴋᴇʀ Fɪʟᴇ Fᴏʀ Cʀᴇᴀᴛɪɴɢ A Nᴇᴡ Sᴛɪᴄᴋᴇʀ Pᴀᴄᴋ:", reply_markup=command_back)
    user_states[call.message.chat.id] = STICKER_PACK_TITLE


@bot.callback_query_handler(func=lambda call: call.data == 'addsticker')
def create_sticker_pack(call):
    user_states[call.message.chat.id] = ADD_LINK_STICKER
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="🔗 Sᴇɴᴅ Sᴛɪᴄᴋᴇʀ Pᴀᴄᴋ Lɪɴᴋ:", reply_markup=command_back)
    
    
@bot.callback_query_handler(func=lambda call: call.data == 'delsticker')
def create_sticker_pack(call):
    user_states[call.message.chat.id] = DELSTICKER
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="💟 Sᴇɴᴅ Sᴛɪᴄᴋᴇʀ:", reply_markup=command_back)
    
    

@bot.callback_query_handler(func=lambda call: call.data == 'apngtowebm')
def create_sticker_pack(call):
    user_states[call.message.chat.id] = APNG_TO_WEBM
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="📂 Sᴇɴᴅ Pɴɢ, Aᴘɴɢ, Gɪғ, Vɪᴅᴇᴏ Fɪʟᴇ:", reply_markup=command_back)
    
    
@bot.callback_query_handler(func=lambda call: call.data == 'stickerdownload')
def create_sticker_pack(call):
    user_states[call.message.chat.id] = STICKER_DOWNLOAD
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="💟 Sᴇɴᴅ Sᴛɪᴄᴋᴇʀ:", reply_markup=command_back)



@bot.callback_query_handler(func=lambda call: call.data == 'delpack')
def create_sticker_pack(call):
    user_states[call.message.chat.id] = DELPACK
    user_id = str(call.from_user.id)
    result_data = get_user_data(user_id)
    if result_data:
        formatted_links = [f'[▒ 🖇 𝗦𝘁𝗶𝗰𝗸𝗲𝗿 𝗣𝗮𝗰𝗸 𝗟𝗶𝗻𝗸 ▒]({link})' for link in result_data]
        result = "\n".join(formatted_links)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=f"🔗 Sᴇɴᴅ Sᴛɪᴄᴋᴇʀ Pᴀᴄᴋ Lɪɴᴋ:\n\n⚡⃨ 𝗖⃨𝗥⃨𝗘⃨𝗔⃨𝗧⃨𝗘⃨𝗗⃨ 𝗦⃨𝗧⃨𝗜⃨𝗖⃨𝗞⃨𝗘⃨𝗥⃨ 𝗣⃨𝗔⃨𝗖⃨𝗞⃨ 𝗟⃨𝗜⃨𝗦⃨𝗧⃨\n{result}", reply_markup=command_back, parse_mode="Markdown")
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=f"🔗 Sᴇɴᴅ Sᴛɪᴄᴋᴇʀ Pᴀᴄᴋ Lɪɴᴋ:", reply_markup=command_back, parse_mode="Markdown")
    
@bot.message_handler(content_types=['document'], func=lambda message: user_states.get(message.chat.id) == APNG_TO_WEBM)
def handle_document(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        save = bot.reply_to(message, f"🍥 Pʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ `{message.document.mime_type}` ғɪʟᴇ...", parse_mode="Markdown")
        saved_message_ids.append(save.message_id)
        saved_message_ids.append(message.message_id)
        
        file_info = bot.get_file(message.document.file_id)
        bot.send_chat_action(message.chat.id, 'upload_document')
        downloaded_file = bot.download_file(file_info.file_path)
        f72hs = message.from_user.id
        file_path = file_info.file_path
        content_type = file_info.file_path.split('.')[-1]
        document_file_name_jinxx = f"{f72hs}.{content_type}"
        with open(document_file_name_jinxx, "wb") as file:
            file.write(downloaded_file)
    except Exception as e:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, e)
    if content_type == "png":
        file1_type = check_image_type(document_file_name_jinxx)
        if file1_type == "apng":
            try:
                sticker_main_size = get_apng_size(document_file_name_jinxx)
                webm_size, new_width, new_height = apng_to_webm(document_file_name_jinxx, f"{f72hs}.webm", sticker_main_size)
            except Exception as e:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, e)       
        else:
            try:
                sticker_main_size = get_apng_size(document_file_name_jinxx)
                webm_size, new_width, new_height = png_to_webm(document_file_name_jinxx, f"{f72hs}.webm", sticker_main_size)
            except Exception as e:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, e)       
                
    elif content_type == "gif":
        print("2")
        try:
            sticker_main_size = get_apng_size(document_file_name_jinxx)
            webm_size, new_width, new_height = gif_to_webm(document_file_name_jinxx, f"{f72hs}.webm", sticker_main_size)
        except Exception as e:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, e)
            
    elif content_type == "mp4":
        try:
            print("82727")
            sticker_main_size = get_video_size(document_file_name_jinxx)
            webm_size, new_width, new_height = video_to_webm(document_file_name_jinxx, f"{f72hs}.webm", sticker_main_size)
        except Exception as e:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, e)
            
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, f"``{content_type}`` Unsupported MIME type", parse_mode="Markdown")
    if os.path.exists(f"{f72hs}.webm"):
        with open(f"{f72hs}.webm", 'rb') as sticker_file:
            delete_all_saved_messages(message.chat.id)
            bot.send_chat_action(message.chat.id, 'upload_document')
            size_info = f"📏 Sɪᴢᴇ: {webm_size} bytes\n📏 Sɪᴢᴇ: {new_width}x{new_height}"
            sent_message = bot.send_document(message.chat.id, sticker_file, caption=size_info)
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
            bot.edit_message_reply_markup(chat_id=message.chat.id,
                                  message_id=sent_message.message_id,
                                  reply_markup=markup)
                           

            
            #bot.send_message(message.chat.id, size_info, reply_markup=markup)
    try:
        os.remove(document_file_name_jinxx)
        os.remove(f"{f72hs}.webm")
    except Exception as e:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, e)
            
            
            

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
        
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)



@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == DELPACK)
def handle_document4(message):
    sticker_pack_link = message.text
    user_id = str(message.from_user.id)
    if check_link(sticker_pack_link):
        sticker_pack_name = sticker_pack_link.split("/")[-1]
        try:
            bot.delete_sticker_set(sticker_pack_name)
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, "✅ Dᴏɴᴇ! Tʜᴇ Sᴛɪᴄᴋᴇʀ Sᴇᴛ Is Gᴏɴᴇ.", parse_mode="Markdown")
            data_to_delete = [message.text]
            delete_data_from_json(user_id, data_to_delete)
            result_data = get_user_data(user_id)
            if result_data:
                formatted_links = [f'[▒ 🖇 𝗦𝘁𝗶𝗰𝗸𝗲𝗿 𝗣𝗮𝗰𝗸 𝗟𝗶𝗻𝗸 ▒]({link})' for link in result_data]
                result = "\n".join(formatted_links)
                bot.send_message(message.chat.id, f"{command_list_header_text}\n⚡⃨ 𝗖⃨𝗥⃨𝗘⃨𝗔⃨𝗧⃨𝗘⃨𝗗⃨ 𝗦⃨𝗧⃨𝗜⃨𝗖⃨𝗞⃨𝗘⃨𝗥⃨ 𝗣⃨𝗔⃨𝗖⃨𝗞⃨ 𝗟⃨𝗜⃨𝗦⃨𝗧⃨\n{result}", reply_markup=command_list, parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, command_list_header_text, reply_markup=command_list, parse_mode="Markdown")
            user_states[message.chat.id] = HOME
        except telebot.apihelper.ApiException as e:
            if "STICKERSET_INVALID" in str(e):
                data_to_delete = [message.text]
                delete_data_from_json(user_id, data_to_delete)
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, f"😢 Tʜɪs Mᴇᴛʜᴏᴅ Tᴏ Dᴇʟᴇᴛᴇ A Sᴛɪᴄᴋᴇʀ Pᴀᴄᴋ Fʀᴏᴍ A Sᴇᴛ Cʀᴇᴀᴛᴇᴅ Bʏ Tʜᴇ Bᴏᴛ.", parse_mode="Markdown")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, f"```ERROR {e}```", parse_mode="Markdown")
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, f"❌ Tʜᴇ Mᴇssᴀɢᴇ Is Nᴏᴛ A Vᴀʟɪᴅ URL.\n\n```🔗Exᴀᴍᴘʟᴇ: https://t.me/addstickers/STICKER_NAME```", parse_mode="Markdown", reply_markup=send_st_pack_link_text)








@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == ADD_LINK_STICKER)
def handle_document3(message):
    sticker_pack_link = message.text
    user_id = str(message.from_user.id)
    if check_link(sticker_pack_link):
        if user_id not in user_data:
            user_data[user_id] = {}
        user_data[user_id]['add_link_sticker'] = message.text
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, "📂 Sᴇɴᴅ Wᴇʙᴍ Sᴛɪᴄᴋᴇʀ Fɪʟᴇ")
        user_states[message.chat.id] = ADD_STICKER
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, f"❌ Tʜᴇ Mᴇssᴀɢᴇ Is Nᴏᴛ A Vᴀʟɪᴅ URL.\n\n```🔗Exᴀᴍᴘʟᴇ: https://t.me/addstickers/STICKER_NAME```", parse_mode="Markdown", reply_markup=send_st_pack_link_text)





@bot.message_handler(content_types=['document'], func=lambda message: user_states.get(message.chat.id) == ADD_STICKER)
def handle_document2(message):
    if message.document.mime_type == 'video/webm':
        user_id = str(message.from_user.id)
        if user_id not in user_data:
            user_data[user_id] = {}
        sticker_pack_link = user_data[user_id]['add_link_sticker']
        sticker_pack_name = sticker_pack_link.split("/")[-1]
        bot.add_sticker_to_set(user_id, sticker_pack_name, emojis="⭐", webm_sticker=message.document.file_id)
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, f"Sticker Added {sticker_pack_link}")
        bot.send_message(message.chat.id, "📂 Sᴇɴᴅ Wᴇʙᴍ Sᴛɪᴄᴋᴇʀ Fɪʟᴇ")
    else:
        bot.send_chat_action(message.chat.id, 'typing')
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

#AUTOMATIC DELETE UNNECESSARY MESSAGE V1{
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == HOME, content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
def handle_sba72sbticker(message):
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except telebot.apihelper.ApiException as e:
        bot.send_message(message.chat.id, f"😅 Dᴏɴ'ᴛ Wᴏʀʀʏ, Jᴜsᴛ Iɢɴᴏʀᴇ Iᴛ.\n\n```{e}", parse_mode="Markdown")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == STICKER_PACK_TITLE, content_types=['audio', 'photo', 'voice', 'video', 'text', 'location', 'contact', 'sticker'])
def handle_sba72sbticker(message):
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except telebot.apihelper.ApiException as e:
        bot.send_message(message.chat.id, f"😅 Dᴏɴ'ᴛ Wᴏʀʀʏ, Jᴜsᴛ Iɢɴᴏʀᴇ Iᴛ.\n\n```{e}", parse_mode="Markdown")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == ADD_LINK_STICKER, content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
def handle_sba72sbticker(message):
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except telebot.apihelper.ApiException as e:
        bot.send_message(message.chat.id, f"😅 Dᴏɴ'ᴛ Wᴏʀʀʏ, Jᴜsᴛ Iɢɴᴏʀᴇ Iᴛ.\n\n```{e}", parse_mode="Markdown")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == ADD_STICKER, content_types=['audio', 'photo', 'voice', 'video', 'text', 'location', 'contact', 'sticker'])
def handle_sba72sbticker(message):
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except telebot.apihelper.ApiException as e:
        bot.send_message(message.chat.id, f"😅 Dᴏɴ'ᴛ Wᴏʀʀʏ, Jᴜsᴛ Iɢɴᴏʀᴇ Iᴛ.\n\n```{e}", parse_mode="Markdown")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == DELSTICKER, content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact'])
def handle_sba72sbticker(message):
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except telebot.apihelper.ApiException as e:
        bot.send_message(message.chat.id, f"😅 Dᴏɴ'ᴛ Wᴏʀʀʏ, Jᴜsᴛ Iɢɴᴏʀᴇ Iᴛ.\n\n```{e}", parse_mode="Markdown")
        
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == DELPACK, content_types=['audio', 'photo', 'voice', 'video', 'document', 'location', 'contact', 'sticker'])
def handle_sba72sbticker(message):
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except telebot.apihelper.ApiException as e:
        bot.send_message(message.chat.id, f"😅 Dᴏɴ'ᴛ Wᴏʀʀʏ, Jᴜsᴛ Iɢɴᴏʀᴇ Iᴛ.\n\n```{e}", parse_mode="Markdown")
        
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == APNG_TO_WEBM, content_types=['audio', 'voice', 'text', 'location', 'contact', 'sticker', 'video', 'photo'])
def handle_sba72sbticker(message):
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except telebot.apihelper.ApiException as e:
        bot.send_message(message.chat.id, f"😅 Dᴏɴ'ᴛ Wᴏʀʀʏ, Jᴜsᴛ Iɢɴᴏʀᴇ Iᴛ.\n\n```{e}", parse_mode="Markdown")
        
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == STICKER_DOWNLOAD, content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact'])
def handle_sba72sbticker(message):
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except telebot.apihelper.ApiException as e:
        bot.send_message(message.chat.id, f"😅 Dᴏɴ'ᴛ Wᴏʀʀʏ, Jᴜsᴛ Iɢɴᴏʀᴇ Iᴛ.\n\n```{e}", parse_mode="Markdown")
#}AUTOMATIC DELETE UNNECESSARY MESSAGE V1



def delete_all_saved_messages(chat_id):
    for msg_id in saved_message_ids:
        try:
            bot.delete_message(chat_id, msg_id)
            
        except Exception as e:
            print(f"Error deleting message ID {msg_id}: {e}")
    saved_message_ids.clear()
    
    
def delete_all_saved_messages_v2(chat_id):
    for msg_id in saved_message_ids_v2:
        try:
            bot.delete_message(chat_id, msg_id)
            
        except Exception as e:
            print(f"Error deleting message ID {msg_id}: {e}")
    saved_message_ids_v2.clear()



if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)