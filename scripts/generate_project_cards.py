from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "projects"
WIDTH, HEIGHT = 980, 520
RADIUS = 36

PROJECTS = [
    {
        "file": "01-wfims.png",
        "index": "01",
        "title": "Workforce Intelligence",
        "body": "Employees, attendance, and leave in one place. Role-based access, live analytics, and reports for day-to-day operations at Newmark.",
        "tags": ["React", "TypeScript", ".NET 8", "SQL Server"],
        "accent": (30, 167, 255),
    },
    {
        "file": "02-velune.png",
        "index": "02",
        "title": "Velune",
        "body": "A private birthday in one link. Photos, a letter, cake, and music open as a cinematic page. No app and no account.",
        "tags": ["Next.js", "Prisma", "PostgreSQL", "Tailwind"],
        "accent": (244, 114, 182),
    },
    {
        "file": "03-railyatra.png",
        "index": "03",
        "title": "Railyatra",
        "body": "Search trains, book tickets, and manage reservations. Each account is protected, and staff oversee bookings from an admin dashboard.",
        "tags": ["Node.js", "Express", "MongoDB", "JWT"],
        "accent": (45, 212, 191),
    },
    {
        "file": "04-anti-sleep.png",
        "index": "04",
        "title": "Anti Sleep Alarm",
        "body": "An Arduino device that notices when a driver stops blinking and sounds an alarm, with a site that explains the hardware.",
        "tags": ["Arduino", "C++", "IR Sensor", "Vercel"],
        "accent": (251, 191, 36),
    },
    {
        "file": "05-cipherlink.png",
        "index": "05",
        "title": "CipherLink",
        "body": "Group chat, photos, and voice notes. Every message is stored as ciphertext, so the conversation stays private in the database.",
        "tags": ["Python", "Flask", "PostgreSQL", "AES-256-GCM"],
        "accent": (167, 139, 250),
    },
    {
        "file": "06-portfolio.png",
        "index": "06",
        "title": "Portfolio",
        "body": "The live site for these projects, certifications, skills, and contact. Built with React, TypeScript, and Tailwind.",
        "tags": ["React", "TypeScript", "Vite", "Tailwind"],
        "accent": (125, 211, 252),
    },
]


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        current = ""
        for word in words:
            trial = word if not current else f"{current} {word}"
            if draw.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def rounded_gradient(accent: tuple[int, int, int]) -> Image.Image:
    gradient = Image.new("RGBA", (WIDTH, HEIGHT))
    pixels = gradient.load()
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        r = int(8 + (16 - 8) * t)
        g = int(18 + (36 - 18) * t)
        b = int(40 + (78 - 40) * t)
        for x in range(WIDTH):
            glow = max(0, 1 - ((x - WIDTH * 0.82) ** 2 + (y - HEIGHT * 0.2) ** 2) ** 0.5 / 420)
            pixels[x, y] = (
                min(255, int(r + accent[0] * glow * 0.22)),
                min(255, int(g + accent[1] * glow * 0.18)),
                min(255, int(b + accent[2] * glow * 0.28)),
                255,
            )

    mask = Image.new("L", (WIDTH, HEIGHT), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, WIDTH - 1, HEIGHT - 1), radius=RADIUS, fill=255)
    gradient.putalpha(mask)
    return gradient


def draw_card(project: dict) -> Image.Image:
    accent = project["accent"]
    card = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    card.alpha_composite(rounded_gradient(accent))
    draw = ImageDraw.Draw(card)

    index_font = load_font(22, bold=True)
    title_font = load_font(48, bold=True)
    body_font = load_font(26)
    tag_font = load_font(20, bold=True)
    watermark_font = load_font(210, bold=True)

    watermark = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ImageDraw.Draw(watermark).text((620, 210), project["index"], font=watermark_font, fill=accent + (28,))
    card.alpha_composite(watermark)
    draw = ImageDraw.Draw(card)

    pill = (48, 42, 118, 86)
    draw.rounded_rectangle(pill, radius=22, fill=accent)
    index_box = draw.textbbox((0, 0), project["index"], font=index_font)
    index_w = index_box[2] - index_box[0]
    index_h = index_box[3] - index_box[1]
    draw.text(
        (pill[0] + (pill[2] - pill[0] - index_w) / 2, pill[1] + (pill[3] - pill[1] - index_h) / 2 - 2),
        project["index"],
        font=index_font,
        fill=(7, 17, 32),
    )

    title_lines = wrap_text(draw, project["title"], title_font, WIDTH - 120)
    y = 118
    for line in title_lines[:2]:
        draw.text((48, y), line, font=title_font, fill=(255, 255, 255))
        y += 58

    body_top = y + 8
    for line in wrap_text(draw, project["body"], body_font, WIDTH - 120)[:3]:
        draw.text((48, body_top), line, font=body_font, fill=(198, 214, 232))
        body_top += 38

    x = 48
    tag_y = HEIGHT - 92
    for tag in project["tags"]:
        text_w = draw.textlength(tag, font=tag_font)
        box = (x, tag_y, x + text_w + 36, tag_y + 44)
        draw.rounded_rectangle(box, radius=16, outline=accent, width=2)
        draw.text((x + 18, tag_y + 8), tag, font=tag_font, fill=accent)
        x = box[2] + 12

    return card


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for project in PROJECTS:
        image = draw_card(project)
        path = OUT / project["file"]
        image.save(path, format="PNG", optimize=True)
        print(f"Generated {path}")


if __name__ == "__main__":
    main()
