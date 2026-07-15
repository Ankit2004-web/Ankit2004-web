from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
WIDTH, HEIGHT = 1600, 400
PRIMARY = (10, 42, 102)
ACCENT = (30, 167, 255)
WHITE = (255, 255, 255)
MUTED = (184, 199, 220)
LIGHT = (232, 238, 247)
AVATAR_SIZE = 184
AVATAR_X = 1188
AVATAR_Y = 108
AVATAR_CENTER_X = AVATAR_X + AVATAR_SIZE // 2
AVATAR_CENTER_Y = AVATAR_Y + AVATAR_SIZE // 2


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_background(draw: ImageDraw.ImageDraw) -> None:
    for x in range(WIDTH):
        ratio = x / WIDTH
        r = int(PRIMARY[0] + (13 - PRIMARY[0]) * ratio * 0.4)
        g = int(PRIMARY[1] + (52 - PRIMARY[1]) * ratio * 0.4)
        b = int(PRIMARY[2] + (120 - PRIMARY[2]) * ratio * 0.4)
        draw.line([(x, 0), (x, HEIGHT)], fill=(r, g, b))


def draw_avatar_accents(draw: ImageDraw.ImageDraw) -> None:
    glow_radius = 132
    draw.ellipse(
        (
            AVATAR_CENTER_X - glow_radius,
            AVATAR_CENTER_Y - glow_radius,
            AVATAR_CENTER_X + glow_radius,
            AVATAR_CENTER_Y + glow_radius,
        ),
        fill=(ACCENT[0], ACCENT[1], ACCENT[2], 42),
    )

    inner_radius = 108
    draw.ellipse(
        (
            AVATAR_CENTER_X - inner_radius,
            AVATAR_CENTER_Y - inner_radius,
            AVATAR_CENTER_X + inner_radius,
            AVATAR_CENTER_Y + inner_radius,
        ),
        fill=(ACCENT[0], ACCENT[1], ACCENT[2], 28),
    )

    draw.ellipse((1410, 285, 1540, 415), fill=(255, 255, 255, 18))
    draw.rounded_rectangle((1040, 255, 1145, 360), radius=24, fill=(255, 255, 255, 12))


def circular_avatar(source: Path, size: int) -> Image.Image:
    image = Image.open(source).convert("RGBA")
    image = image.resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    image.putalpha(mask)
    return image


def circular_avatar_with_ring(source: Path, size: int, ring_width: int = 4) -> Image.Image:
    avatar = circular_avatar(source, size)
    canvas_size = size + ring_width * 2 + 8
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    ring_draw = ImageDraw.Draw(canvas)
    ring_draw.ellipse((0, 0, canvas_size, canvas_size), outline=ACCENT + (230,), width=ring_width)
    canvas.paste(avatar, (ring_width + 4, ring_width + 4), avatar)
    return canvas


def main() -> None:
    profile_path = ASSETS / "profile.png"
    if not profile_path.exists():
        raise FileNotFoundError(f"Missing profile image: {profile_path}")

    banner = Image.new("RGBA", (WIDTH, HEIGHT), PRIMARY)
    draw = ImageDraw.Draw(banner, "RGBA")
    draw_background(draw)
    draw_avatar_accents(draw)

    title_font = load_font(54, bold=True)
    subtitle_font = load_font(28, bold=True)
    body_font = load_font(22)
    small_font = load_font(17)

    draw.text((120, 70), "Ankit Biswas", font=title_font, fill=WHITE)
    draw.text((120, 140), "Full-Stack Developer", font=subtitle_font, fill=ACCENT)
    draw.text((120, 190), "Building Scalable Enterprise Applications", font=body_font, fill=LIGHT)
    draw.text(
        (120, 236),
        "ASP.NET Core • React • SQL Server • Azure DevOps",
        font=small_font,
        fill=MUTED,
    )
    draw.rectangle((120, 300, 340, 304), fill=ACCENT)

    avatar_size = AVATAR_SIZE
    avatar = circular_avatar(profile_path, avatar_size)
    ring_size = avatar_size + 16
    ring = Image.new("RGBA", (ring_size, ring_size), (0, 0, 0, 0))
    ring_draw = ImageDraw.Draw(ring)
    ring_draw.ellipse((0, 0, ring_size, ring_size), outline=ACCENT + (220,), width=4)
    ring_x = AVATAR_CENTER_X - ring_size // 2
    ring_y = AVATAR_CENTER_Y - ring_size // 2
    banner.paste(ring, (ring_x, ring_y), ring)
    banner.paste(avatar, (AVATAR_X, AVATAR_Y), avatar)

    output = ASSETS / "banner.png"
    banner.convert("RGB").save(output, format="PNG", optimize=True)
    print(f"Generated {output}")

    profile_circle = circular_avatar_with_ring(profile_path, 220)
    profile_output = ASSETS / "profile-circle.png"
    profile_circle.save(profile_output, format="PNG", optimize=True)
    print(f"Generated {profile_output}")


if __name__ == "__main__":
    main()
