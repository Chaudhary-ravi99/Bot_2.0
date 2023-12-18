import string
import random
import imageio
import subprocess
import os
from PIL import Image
import numpy as np



def check_link(message):
    if "https://t.me/addstickers/" in message:
        hs72bsiqjb = True
    else:
        hs72bsiqjb = False
    return hs72bsiqjb
    
    
def is_apng(data):
    acTL = data.find(b"\x61\x63\x54\x4C")
    if acTL > 0:  # find returns -1 if it can't find anything
        iDAT = data.find(b"\x49\x44\x41\x54")
        if acTL < iDAT:
            return True
    return False

def check_image_type(file_path):
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
            return 'apng' if data.startswith(b'\x89PNG') and is_apng(data) else None
    except Exception as e:
        print(f"Error checking image type: {e}")
        return None





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

def get_video_size(video_path):
    vid = imageio.get_reader(video_path, 'ffmpeg')
    first_frame = vid.get_data(0)
    width, height = first_frame.shape[1], first_frame.shape[0]
    larger_value = max(width, height)
    ttttt = resize_apng_jinxx(larger_value, width, height)
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
    
    

def gif_to_webm(input_gif, output_webm, sticker_main_size):
    gif_frames = imageio.mimread(input_gif)
    original_height, original_width, _ = gif_frames[0].shape
    aspect_ratio = original_width / original_height
    new_width = int(sticker_main_size.split('x')[0])
    new_height = int(new_width / aspect_ratio)
    resized_frames = [Image.fromarray(frame).resize((new_width, new_height)) for frame in gif_frames]
    speed = 1.0
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', input_gif,
        '-c:v', 'libvpx-vp9',
        '-vf', f'split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse,setpts={1/speed}*PTS',
        '-b:v', '256K',
        '-auto-alt-ref', '0',
        '-pix_fmt', 'yuva420p',
        '-s', f'{new_width}x{new_height}',
        '-r', '60',
        '-crf', '10',
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
    

def png_to_webm(input_png, output_webm, sticker_main_size):
    # Extract width and height from sticker_main_size
    target_width, target_height = map(int, sticker_main_size.split('x'))

    # Resize the PNG image
    original_image = Image.open(input_png)
    resized_image = original_image.resize((target_width, target_height))
    resized_image.save('resized_input.png')

    ffmpeg_cmd = [
        'ffmpeg',
        '-i', 'resized_input.png',
        '-c:v', 'libvpx-vp9',
        '-b:v', '256k',
        '-vf', f'scale={target_width}:{target_height}',
        '-pix_fmt', 'yuva420p',
        output_webm
    ]
    subprocess.run(ffmpeg_cmd)

    # Clean up temporary resized image
    os.remove('resized_input.png')

    # Get the size of the created WebM file
    webm_size = os.path.getsize(output_webm)
    return webm_size, target_width, target_height
    
    
def video_to_webm(input_video, output_webm, sticker_main_size, target_duration=2.9):
    new_width = int(sticker_main_size.split('x')[0])
    
    ffmpeg_cmd = [
    'ffmpeg',
    '-i', input_video,
    '-vf', f'scale={new_width}:-1',
    '-c:v', 'libvpx-vp9',
    '-b:v', '512k',  # Adjust the bitrate as needed
    '-crf', '10',
    '-t', str(target_duration),
    '-pix_fmt', 'yuva420p',
    '-an',  # Remove audio
    output_webm
]
    subprocess.run(ffmpeg_cmd)

    # Get the size of the created WebM file
    webm_size = os.path.getsize(output_webm)
    return webm_size, new_width, int(new_width / 16 * 9)
