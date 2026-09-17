#!/usr/bin/env python3
"""Scrape 4 bài viết tay đã có sẵn -> data/legacy-posts.json.

Bài cũ KHÔNG migrate vào CMS (xem static-site-build.md mục 3): trang chi tiết của chúng giữ
nguyên y hệt, `build.py` chỉ liệt kê thêm ở trang danh sách + sitemap. CMS không bao giờ đụng
vào file này.

Chạy lại khi nào: sửa tay tiêu đề/mô tả/ảnh của 1 trong 4 bài cũ. Bình thường không cần chạy.

    python3 scripts/scrape-legacy-posts.py
"""
import glob
import json
import os
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
HTML = os.path.join(ROOT, "html")
DATA = os.path.join(ROOT, "data")

# Danh mục của từng bài cũ - chốt tay theo đúng chuyên mục các bài đang thuộc về, KHÔNG đoán
# từ slug (đoán sai là bài nhảy sang chuyên mục khác mà không ai để ý).
LEGACY_CATEGORY = {
    "cam-nang-du-lich-go-cong": "Cẩm nang du lịch",
    "kinh-nghiem-du-lich-dong-thap-mua-nuoc-noi": "Cẩm nang du lịch",
    "kinh-nghiem-don-xe-san-bay-can-tho": "Kinh nghiệm đi lại",
    "kinh-nghiem-don-xe-san-bay-tan-son-nhat": "Kinh nghiệm đi lại",
}

# Ngày đăng của 4 bài cũ: lấy từ commit đầu tiên đưa chúng vào repo (không có ngày nào hiển
# thị trên trang để đọc ra).
LEGACY_DATE = "2026-09-16"

# 4 bài cũ CÙNG một ngày đăng nên sắp theo ngày sẽ ra thứ tự tuỳ ý. Chốt cứng đúng thứ tự
# chúng đang hiển thị trên /blog/ trước khi có pipeline, để build lại không xáo trộn trang.
LEGACY_ORDER = [
    "kinh-nghiem-don-xe-san-bay-tan-son-nhat",
    "kinh-nghiem-du-lich-dong-thap-mua-nuoc-noi",
    "cam-nang-du-lich-go-cong",
    "kinh-nghiem-don-xe-san-bay-can-tho",
]


def squash(text):
    return re.sub(r"\s+", " ", text).strip()


def main():
    blog = open(os.path.join(HTML, "blog", "index.html"), encoding="utf-8").read()
    # Ảnh thẻ bài lấy từ chính trang /blog/ (thumb thật đang dùng), không tự đặt.
    thumb_pat = re.compile(
        r'href="/blog/([a-z0-9-]+)"\s*[^>]*class="blog-card-thumb"\s*>\s*'
        r'<img\s+src="([^"]+)"\s+alt="([^"]*)"',
        re.S,
    )
    thumbs = {m.group(1): (m.group(2), m.group(3)) for m in thumb_pat.finditer(blog)}

    out = []
    for path in sorted(glob.glob(os.path.join(HTML, "blog", "*", "index.html"))):
        slug = os.path.basename(os.path.dirname(path))
        if slug == "danh-muc":
            continue
        s = open(path, encoding="utf-8").read()
        head = re.search(r"<head>.*?</head>", s, re.S).group(0)
        body = re.sub(r"<head>.*?</head>", "", s, flags=re.S)

        desc = re.search(r'name="description" content="(.*?)"', head, re.S)
        h1 = re.search(r"<h1>(.*?)</h1>", body, re.S)
        crumb = re.search(r'<nav class="breadcrumb".*?<span>([^<]+)</span>\s*</nav>', body, re.S)
        cover, cover_alt = thumbs.get(slug, ("", ""))

        if not cover:
            raise SystemExit(
                "Không tìm thấy ảnh thẻ bài của '%s' trên trang /blog/ - kiểm tra lại markup "
                "blog-card-thumb trước khi tin file sinh ra là đúng." % slug
            )
        if slug not in LEGACY_CATEGORY:
            raise SystemExit(
                "Bài cũ '%s' chưa được khai danh mục trong LEGACY_CATEGORY - bổ sung rồi chạy lại."
                % slug
            )

        if slug not in LEGACY_ORDER:
            raise SystemExit(
                "Bài cũ '%s' chưa có trong LEGACY_ORDER - bổ sung rồi chạy lại." % slug
            )

        out.append({
            "slug": slug,
            "order": LEGACY_ORDER.index(slug),
            "title": squash(h1.group(1)) if h1 else slug,
            "description": squash(desc.group(1)) if desc else "",
            "category": LEGACY_CATEGORY[slug],
            "date": LEGACY_DATE,
            "cover": cover,
            "cover_alt": cover_alt,
            "breadcrumb": squash(crumb.group(1)) if crumb else "",
            "legacy": True,
        })

    out.sort(key=lambda p: p["order"])

    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "legacy-posts.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    posts_path = os.path.join(DATA, "posts.json")
    if not os.path.exists(posts_path):
        with open(posts_path, "w", encoding="utf-8") as fh:
            fh.write("[]\n")

    print("data/legacy-posts.json: %d bài" % len(out))
    for p in out:
        print("  -", p["slug"], "|", p["category"], "|", p["cover"])


if __name__ == "__main__":
    main()
