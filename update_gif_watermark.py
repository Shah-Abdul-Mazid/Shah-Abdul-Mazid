import os
import time
from PIL import Image, ImageSequence, ImageDraw, ImageFont

def apply_badge(im_rgba, font_bold):
    draw = ImageDraw.Draw(im_rgba)
    pill_box = [8, 240, 196, 268]
    draw.rounded_rectangle(pill_box, radius=8, fill=(10, 15, 28, 255), outline=(6, 182, 212, 255), width=1)
    
    cx, cy, s = 22, 254, 6
    diamond = [(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy)]
    draw.polygon(diamond, fill=(255, 255, 255))
    s_in = 2.5
    diamond_in = [(cx, cy - s_in), (cx + s_in, cy), (cx, cy + s_in), (cx - s_in, cy)]
    draw.polygon(diamond_in, fill=(10, 15, 28))
    
    draw.text((34, 247), 'shah abdul mazid ai', fill=(255, 255, 255), font=font_bold)
    return im_rgba

def process_gif(input_path, output_path):
    print(f"Processing {input_path}...")
    t0 = time.time()
    im = Image.open(input_path)
    durations = []
    processed_frames = []
    
    font_bold = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 12)
    
    for i, frame in enumerate(ImageSequence.Iterator(im)):
        durations.append(frame.info.get('duration', 30))
        rgba = frame.convert("RGBA")
        apply_badge(rgba, font_bold)
        
        # Quantize to P mode (using RGB to avoid alpha dithering issues in GIF)
        rgb = rgba.convert("RGB")
        p_frame = rgb.quantize(colors=128, method=Image.Resampling.LANCZOS, dither=Image.Dither.FLOYDSTEINBERG)
        processed_frames.append(p_frame)
    
    print(f"Processed {len(processed_frames)} frames in {time.time()-t0:.2f}s. Saving...")
    t1 = time.time()
    
    processed_frames[0].save(
        output_path,
        save_all=True,
        append_images=processed_frames[1:],
        duration=durations,
        loop=0,
        optimize=True
    )
    print(f"Saved {output_path} ({os.path.getsize(output_path)} bytes) in {time.time()-t1:.2f}s.")

if __name__ == "__main__":
    for gif_name in ["Talking Artificial Intelligence GIF by Krater.ai.gif", "Working Artificial Intelligence GIF by Krater.ai.gif"]:
        temp_out = "temp_" + gif_name
        process_gif(gif_name, temp_out)
        # Replace original with temp
        if os.path.exists(temp_out) and os.path.getsize(temp_out) > 1000:
            os.replace(temp_out, gif_name)
            print(f"Successfully replaced {gif_name}!")
