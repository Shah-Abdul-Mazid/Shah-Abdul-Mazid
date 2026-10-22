import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_cute_developer_card(output_path="cute-ai-engineer.gif", num_frames=40):
    src_avatar_path = "ezgif.com-gif-maker.gif"
    if not os.path.exists(src_avatar_path):
        raise FileNotFoundError(f"{src_avatar_path} not found")

    avatar_raw = Image.open(src_avatar_path).convert("RGBA")

    width, height = 620, 185
    avatar_size = 114
    avatar_img = avatar_raw.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)

    # High quality supersampled circular mask
    mask_scale = 4
    mask = Image.new("L", (avatar_size * mask_scale, avatar_size * mask_scale), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, avatar_size * mask_scale, avatar_size * mask_scale), fill=255)
    mask = mask.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)

    avatar_circle = Image.new("RGBA", (avatar_size, avatar_size), (0, 0, 0, 0))
    avatar_circle.paste(avatar_img, (0, 0), mask=mask)

    # System fonts
    font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 25)
    font_sub_bold = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 15)
    font_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 14)
    font_badge = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 11)
    font_pill = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 11)

    titles = [
        "AI Engineer @ Neuroxyte",
        "LLMs & Multi-Agent Workflows",
        "Computer Vision & Deep Learning",
        "Researching Trustworthy AI"
    ]

    # Pre-calculated sparkle particles
    sparkles = [
        {"x": 22, "y": 28, "phase": 0.0, "size": 6},
        {"x": 158, "y": 22, "phase": 1.2, "size": 7},
        {"x": 162, "y": 142, "phase": 2.5, "size": 5},
        {"x": 26, "y": 146, "phase": 3.8, "size": 6},
        {"x": 580, "y": 26, "phase": 1.8, "size": 6},
        {"x": 595, "y": 152, "phase": 4.1, "size": 5},
    ]

    frames = []

    for f in range(num_frames):
        t = f / num_frames
        angle_rad = t * 2 * math.pi

        # 1. Background Canvas
        img = Image.new("RGBA", (width, height), (10, 15, 29, 255)) # Deep sleek slate-navy
        draw = ImageDraw.Draw(img)

        # Ambient colored glows (Glassmorphism look)
        glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        g_draw = ImageDraw.Draw(glow_layer)
        
        # Left cyan glow
        cyan_a = int(35 + 15 * math.sin(angle_rad))
        g_draw.ellipse((10, 10, 190, 175), fill=(6, 182, 212, cyan_a))
        
        # Right electric blue glow
        blue_a = int(30 + 12 * math.cos(angle_rad))
        g_draw.ellipse((420, 10, 600, 175), fill=(59, 130, 246, blue_a))

        # Center subtle purple accent
        purp_a = int(22 + 10 * math.sin(angle_rad + 1.5))
        g_draw.ellipse((220, 30, 420, 160), fill=(139, 92, 246, purp_a))

        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(32))
        img.alpha_composite(glow_layer)
        draw = ImageDraw.Draw(img)

        # Modern sleek border with glowing gradient effect
        draw.rounded_rectangle([2, 2, width - 3, height - 3], radius=16, outline=(30, 48, 82), width=1)
        draw.rounded_rectangle([3, 3, width - 4, height - 4], radius=15, outline=(15, 23, 42), width=1)

        # Avatar coordinates
        av_x = 36
        av_y = 35
        center_x = av_x + avatar_size // 2
        center_y = av_y + avatar_size // 2
        ring_radius = (avatar_size // 2) + 7

        # Dynamic rainbow-neon orbiting ring
        num_dots = 40
        for seg in range(num_dots):
            seg_angle = angle_rad + (seg / num_dots) * 2 * math.pi
            phase = (seg / num_dots + t) % 1.0
            
            # Smooth cyan -> blue -> purple gradient
            if phase < 0.5:
                p = phase / 0.5
                r_c = int(6 + p * (59 - 6))
                g_c = int(182 + p * (130 - 182))
                b_c = int(212 + p * (246 - 212))
            else:
                p = (phase - 0.5) / 0.5
                r_c = int(59 + p * (147 - 59))
                g_c = int(130 - p * (130 - 51))
                b_c = int(246 - p * (246 - 234))

            px = center_x + ring_radius * math.cos(seg_angle)
            py = center_y + ring_radius * math.sin(seg_angle)
            
            dot_rad = 2.4 + 0.8 * math.sin(seg_angle * 2 + angle_rad)
            draw.ellipse((px - dot_rad, py - dot_rad, px + dot_rad, py + dot_rad), fill=(r_c, g_c, b_c, 245))

        # Paste avatar circle
        img.alpha_composite(avatar_circle, (av_x, av_y))

        # Cute status indicator badge on bottom-right of avatar: [● ACTIVE]
        status_x = center_x + 24
        status_y = center_y + 36
        draw.rounded_rectangle([status_x - 3, status_y - 2, status_x + 38, status_y + 16], radius=8, fill=(15, 23, 42, 240), outline=(6, 182, 212), width=1)
        # Pulsing green dot
        green_pulse = int(190 + 65 * math.sin(angle_rad * 3))
        draw.ellipse((status_x + 2, status_y + 4, status_x + 8, status_y + 10), fill=(34, green_pulse, 94))
        draw.text((status_x + 12, status_y), "AI", fill=(224, 242, 254), font=font_badge)

        # Cute twinkling stars around the card
        for sp in sparkles:
            sp_alpha = (math.sin(angle_rad * 2 + sp["phase"]) + 1) / 2
            if sp_alpha > 0.15:
                s = sp["size"] * (0.6 + 0.5 * sp_alpha)
                sx, sy = sp["x"], sp["y"]
                star_col = (255, 255, 255, int(sp_alpha * 240))
                draw.line([(sx - s, sy), (sx + s, sy)], fill=star_col, width=1)
                draw.line([(sx, sy - s), (sx, sy + s)], fill=star_col, width=1)
                draw.ellipse((sx - 1.5, sy - 1.5, sx + 1.5, sy + 1.5), fill=(6, 182, 212, int(sp_alpha * 255)))

        # Right Side Information
        text_x = 188

        # Name
        draw.text((text_x, 26), "Shah Abdul Mazid", fill=(255, 255, 255), font=font_title)

        # Cute decorative star glyph
        sparkle_phase = (math.sin(angle_rad * 3) + 1) / 2
        star_color = (255, int(210 + 45 * sparkle_phase), 60)
        draw.text((text_x + 228, 28), "*", fill=star_color, font=font_title)

        # Cycling dynamic title with smooth animation
        title_idx = int(t * len(titles)) % len(titles)
        current_title = titles[title_idx]
        
        # Draw a cute small prefix bullet
        draw.ellipse((text_x, 69, text_x + 5, 74), fill=(6, 182, 212))
        draw.text((text_x + 12, 62), current_title, fill=(6, 182, 212), font=font_sub_bold)

        # Mission / Bio subtitle
        draw.text((text_x, 88), "Building scalable AI backends, RAG pipelines & vision models", fill=(148, 163, 184), font=font_sub)

        # 4 Cute Tech Pills
        pills = [
            ("LLMs & RAG", (37, 99, 235), (219, 234, 254)),       # Blue
            ("Computer Vision", (14, 165, 233), (224, 242, 254)),  # Cyan
            ("FastAPI & Cloud", (16, 185, 129), (209, 250, 229)),  # Emerald
            ("Research (IEEE)", (139, 92, 246), (243, 232, 255))  # Purple
        ]

        bx = text_x
        by = 124
        for p_label, p_border, p_txt in pills:
            bbox = font_pill.getbbox(p_label)
            bw = bbox[2] - bbox[0] + 16
            bh = 24
            # Pill capsule
            draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=12, fill=(15, 23, 42, 230), outline=p_border, width=1)
            draw.text((bx + 8, by + 4), p_label, fill=p_txt, font=font_pill)
            bx += bw + 8

        # Quantize frame cleanly
        rgb_frame = img.convert("RGB")
        p_frame = rgb_frame.quantize(colors=128, method=Image.Resampling.LANCZOS, dither=Image.Dither.FLOYDSTEINBERG)
        frames.append(p_frame)

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=65,
        loop=0,
        optimize=True
    )
    print(f"Generated {output_path}: {os.path.getsize(output_path)} bytes")

def create_cute_avatar_badge(output_path="cute-avatar.gif", num_frames=36):
    src_avatar_path = "ezgif.com-gif-maker.gif"
    avatar_raw = Image.open(src_avatar_path).convert("RGBA")

    size = 170
    avatar_size = 130
    avatar_img = avatar_raw.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)

    # High quality supersampled mask
    mask_scale = 4
    mask = Image.new("L", (avatar_size * mask_scale, avatar_size * mask_scale), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, avatar_size * mask_scale, avatar_size * mask_scale), fill=255)
    mask = mask.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)

    avatar_circle = Image.new("RGBA", (avatar_size, avatar_size), (0, 0, 0, 0))
    avatar_circle.paste(avatar_img, (0, 0), mask=mask)

    font_badge = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 10)

    frames = []
    center = size // 2
    ring_radius = (avatar_size // 2) + 7
    av_offset = (size - avatar_size) // 2

    sparkles = [
        {"x": 20, "y": 24, "phase": 0.0},
        {"x": 150, "y": 28, "phase": 1.5},
        {"x": 18, "y": 140, "phase": 3.0},
        {"x": 152, "y": 136, "phase": 4.5},
    ]

    for f in range(num_frames):
        t = f / num_frames
        angle_rad = t * 2 * math.pi

        # Transparent/dark background
        img = Image.new("RGBA", (size, size), (11, 17, 33, 255))
        draw = ImageDraw.Draw(img)

        # Ambient glow
        glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        g_draw = ImageDraw.Draw(glow)
        glow_a = int(50 + 20 * math.sin(angle_rad))
        g_draw.ellipse((10, 10, size - 10, size - 10), fill=(6, 182, 212, glow_a))
        glow = glow.filter(ImageFilter.GaussianBlur(18))
        img.alpha_composite(glow)
        draw = ImageDraw.Draw(img)

        # Outer rounded boundary
        draw.rounded_rectangle([1, 1, size - 2, size - 2], radius=24, outline=(30, 48, 80), width=1)

        # Neon orbiting ring
        num_dots = 32
        for seg in range(num_dots):
            seg_angle = angle_rad + (seg / num_dots) * 2 * math.pi
            phase = (seg / num_dots + t) % 1.0
            
            # Cyan -> Blue -> Purple
            if phase < 0.5:
                p = phase / 0.5
                r_c = int(6 + p * (59 - 6))
                g_c = int(182 + p * (130 - 182))
                b_c = int(212 + p * (246 - 212))
            else:
                p = (phase - 0.5) / 0.5
                r_c = int(59 + p * (147 - 59))
                g_c = int(130 - p * (130 - 51))
                b_c = int(246 - p * (246 - 234))

            px = center + ring_radius * math.cos(seg_angle)
            py = center + ring_radius * math.sin(seg_angle)
            dot_rad = 2.2 + 0.7 * math.sin(seg_angle * 2 + angle_rad)
            draw.ellipse((px - dot_rad, py - dot_rad, px + dot_rad, py + dot_rad), fill=(r_c, g_c, b_c, 245))

        # Avatar
        img.alpha_composite(avatar_circle, (av_offset, av_offset))

        # Cute status pill at bottom center
        pill_w, pill_h = 70, 18
        px1 = center - pill_w // 2
        py1 = size - 22
        draw.rounded_rectangle([px1, py1, px1 + pill_w, py1 + pill_h], radius=9, fill=(15, 23, 42, 245), outline=(6, 182, 212), width=1)
        
        green_pulse = int(190 + 65 * math.sin(angle_rad * 3))
        draw.ellipse((px1 + 6, py1 + 5, px1 + 12, py1 + 11), fill=(34, green_pulse, 94))
        draw.text((px1 + 18, py1 + 2), "AI ENG", fill=(224, 242, 254), font=font_badge)

        # Sparkles
        for sp in sparkles:
            sp_alpha = (math.sin(angle_rad * 2 + sp["phase"]) + 1) / 2
            if sp_alpha > 0.2:
                s = 4.5 * (0.6 + 0.5 * sp_alpha)
                sx, sy = sp["x"], sp["y"]
                star_col = (255, 255, 255, int(sp_alpha * 240))
                draw.line([(sx - s, sy), (sx + s, sy)], fill=star_col, width=1)
                draw.line([(sx, sy - s), (sx, sy + s)], fill=star_col, width=1)

        # Convert to P mode
        rgb_frame = img.convert("RGB")
        p_frame = rgb_frame.quantize(colors=96, method=Image.Resampling.LANCZOS, dither=Image.Dither.FLOYDSTEINBERG)
        frames.append(p_frame)

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=65,
        loop=0,
        optimize=True
    )
    print(f"Generated {output_path}: {os.path.getsize(output_path)} bytes")

if __name__ == "__main__":
    create_cute_developer_card()
    create_cute_avatar_badge()
