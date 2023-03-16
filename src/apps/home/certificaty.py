from PIL import Image, ImageDraw, ImageFont
import time


def certificaty(name, course):
    cert_template = Image.open("/home/nurmuhammad/uic/ayoluchun.uz/static/shablon/1.jpg")
    font = ImageFont.load_default()
    font_style = ImageFont.truetype("/home/nurmuhammad/uic/ayoluchun.uz/static/fonts/Roboto/Roboto-BoldItalic.ttf", 40)

    draw = ImageDraw.Draw(cert_template)

    date = f'Data: {time.strftime("%d/%m/%Y")}'

    congart = "Congratulations!"

    name_pos = (300, 350)
    course_pos = (300, 450)
    date_pos = (300, 550)
    congart_pos = (300, 250)

    draw.text(name_pos, name, font=font_style, fill='black')
    draw.text(course_pos, course, font=font_style, fill='black')
    draw.text(date_pos, date, font=font_style, fill='black')
    draw.text(congart_pos, congart, font=font_style, fill='black')

    cert_template.save(f"/home/nurmuhammad/uic/ayoluchun.uz/static/certicats/{name}-{course}.jpg")

    return f"/home/nurmuhammad/uic/ayoluchun.uz/static/certicats/{name}-{course}.jpg"
