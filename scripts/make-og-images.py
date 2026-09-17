#!/usr/bin/env python3
"""Dựng ảnh xem trước khi chia sẻ link (Open Graph) 1200x630 cho các trang tĩnh.

    pip install Pillow
    python3 scripts/make-og-images.py       # chạy từ thư mục html/

Chạy lại khi nào: đổi tiêu đề/ảnh nền của 1 trang trong danh sách JOBS bên dưới. KHÔNG nằm
trong CI (ảnh gần như không bao giờ đổi, và CI không cần Pillow).

Bài viết do trang quản trị đăng KHÔNG dùng script này — chúng lấy thẳng ảnh bìa người viết tải
lên làm ảnh xem trước.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
BASE = "assets/images"
OUT = "assets/og"
os.makedirs(OUT, exist_ok=True)

BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
REG  = "/System/Library/Fonts/Supplemental/Arial.ttf"

def cover(src, w=W, h=H):
    im = Image.open(src).convert("RGB")
    sw, sh = im.size
    scale = max(w / sw, h / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    im = im.resize((nw, nh), Image.LANCZOS)
    return im.crop(((nw - w) // 2, (nh - h) // 2, (nw - w) // 2 + w, (nh - h) // 2 + h))

def scrim(im, top=0.20, bottom=0.94):
    """Dark gradient from bottom so text stays readable."""
    grad = Image.new("L", (1, H))
    for y in range(H):
        t = y / (H - 1)
        grad.putpixel((0, y), int(255 * (top + (bottom - top) * (t ** 2.2))))
    mask = grad.resize((W, H))
    overlay = Image.new("RGB", (W, H), (10, 12, 18))
    return Image.composite(overlay, im, mask.point(lambda v: v))

def fit(draw, text, font_path, max_w, start):
    size = start
    while size > 20:
        f = ImageFont.truetype(font_path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(font_path, 20)

def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def build(src, headline, sub, out_name):
    im = scrim(cover(os.path.join(BASE, src)))
    d = ImageDraw.Draw(im, "RGBA")

    # brand bar
    d.rectangle([0, H - 12, W, H], fill=(204, 30, 44, 255))

    # logo
    logo = Image.open(os.path.join(BASE, "logo-white.png")).convert("RGBA")
    lh = 96
    logo = logo.resize((int(logo.width * lh / logo.height), lh), Image.LANCZOS)
    im.paste(logo, (72, 64), logo)

    pad = 72
    maxw = W - pad * 2

    hf = fit(d, headline, BOLD, maxw, 66)
    lines = wrap(d, headline, hf, maxw)
    if len(lines) > 3:
        hf = ImageFont.truetype(BOLD, 52)
        lines = wrap(d, headline, hf, maxw)[:3]

    sf = ImageFont.truetype(REG, 30)
    slines = wrap(d, sub, sf, maxw)[:2] if sub else []

    lh_h = hf.size + 14
    lh_s = sf.size + 10
    block = len(lines) * lh_h + (18 + len(slines) * lh_s if slines else 0)
    y = H - 84 - block

    for ln in lines:
        d.text((pad, y), ln, font=hf, fill=(255, 255, 255))
        y += lh_h
    if slines:
        y += 18
        for ln in slines:
            d.text((pad, y), ln, font=sf, fill=(232, 232, 236))
            y += lh_s

    # hotline pill top-right
    pill = "0386 263 287"
    pf = ImageFont.truetype(BOLD, 30)
    tw = d.textlength(pill, font=pf)
    x0, y0 = W - pad - tw - 44, 72
    d.rounded_rectangle([x0, y0, x0 + tw + 44, y0 + 58], radius=29, fill=(204, 30, 44, 255))
    d.text((x0 + 22, y0 + 13), pill, font=pf, fill=(255, 255, 255))

    im.save(os.path.join(OUT, out_name), "JPEG", quality=86, optimize=True, progressive=True)
    print("wrote", out_name, im.size)

JOBS = [
    ("bg-banner.webp", "TAXI GÒ CÔNG", "Đặt xe nhanh 24/7 — Gò Công · Tiền Giang · Đồng Tháp", "og-default.jpg"),
    ("car.webp", "Taxi nội thành Gò Công", "Đón đúng giờ, giá rẻ, phục vụ 24/7", "og-taxi-noi-thanh.jpg"),
    ("service-intercity.webp", "Taxi liên tỉnh Tiền Giang — Đồng Tháp", "Đón tận nơi, xe đời mới 4–16 chỗ", "og-lien-tinh.jpg"),
    ("article-noibai-tarmac.jpg", "Xe đưa đón sân bay Tân Sơn Nhất", "Giá niêm yết, đón tận nhà, không lo trễ chuyến", "og-san-bay-tsn.jpg"),
    ("service-airport.webp", "Xe đưa đón sân bay Cần Thơ", "Giá niêm yết, đón tận nhà, hỗ trợ 24/7", "og-san-bay-can-tho.jpg"),
    ("service-tour.webp", "Xe du lịch, tham quan", "Trọn gói theo lịch trình, xe 4–16 chỗ", "og-du-lich.jpg"),
    ("service-contract.webp", "Xe hợp đồng & sự kiện", "Công ty, đám cưới, hội nghị, đưa đón nhân viên", "og-hop-dong.jpg"),
    ("blog-dalat.jpg", "Xe đường dài theo yêu cầu", "Tài xế kinh nghiệm, giá thoả thuận rõ ràng", "og-duong-dai.jpg"),
    ("car.webp", "Cho thuê xe tự lái", "Thủ tục nhanh gọn, giao nhận xe tận nơi", "og-tu-lai.jpg"),
    ("pricing-promo-banner.jpg", "Bảng giá Taxi Gò Công", "Giá niêm yết rõ ràng, không phát sinh chi phí ẩn", "og-bang-gia.jpg"),
    ("coverage-mytho.webp", "Tuyến đường phục vụ", "Nội thành, liên tỉnh, sân bay và đường dài", "og-tuyen-duong.jpg"),
    ("coverage-gocong.webp", "Giới thiệu Taxi Gò Công", "Đơn vị vận tải hành khách uy tín tại Tiền Giang", "og-gioi-thieu.jpg"),
    ("car.webp", "Liên hệ Taxi Gò Công", "Hotline 24/7 · taxigocong@gmail.com", "og-lien-he.jpg"),
    ("coverage-lapvo.webp", "Blog Taxi Gò Công", "Kinh nghiệm đi lại & cẩm nang du lịch miền Tây", "og-blog.jpg"),
    ("coverage-gocong.webp", "Cẩm nang du lịch Gò Công", "Những điểm đến không thể bỏ lỡ", "og-blog-gocong.jpg"),
    ("coverage-caolanh.webp", "Du lịch Đồng Tháp mùa nước nổi", "Tràm Chim, Gáo Giồng, làng hoa Sa Đéc", "og-blog-dongthap.jpg"),
    ("article-noibai-tarmac.jpg", "Kinh nghiệm đặt xe sân bay Tân Sơn Nhất", "Bảng giá tham khảo & checklist chọn nhà xe uy tín", "og-blog-tsn.jpg"),
    ("service-airport.webp", "Kinh nghiệm đặt xe sân bay Cần Thơ", "Thời gian di chuyển, bảng giá và lưu ý quan trọng", "og-blog-cantho.jpg"),
    ("blog-nhatrang.jpg", "Cẩm nang du lịch", "Chuyên mục trên blog Taxi Gò Công", "og-dm-cam-nang.jpg"),
    ("blog-sapa.jpg", "Kinh nghiệm đi lại", "Chuyên mục trên blog Taxi Gò Công", "og-dm-kinh-nghiem.jpg"),
]

for src, h, s, out in JOBS:
    build(src, h, s, out)
