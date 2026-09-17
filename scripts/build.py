#!/usr/bin/env python3
"""Build trang tĩnh từ data/ + templates/.

    python3 scripts/build.py

Sinh ra:
  html/blog/<slug>/index.html            trang chi tiết của bài do CMS tạo
  html/blog/index.html                   danh sách tất cả bài (CMS + bài viết tay cũ)
  html/blog/danh-muc/<slug>/index.html   trang chuyên mục (chỉ chuyên mục CÓ bài)

KHÔNG đụng tới trang chi tiết của 4 bài viết tay cũ (`legacy: true` trong
data/legacy-posts.json) — chúng giữ nguyên y hệt, chỉ được liệt kê thêm ở danh sách.
Xem static-site-build.md mục 3.

`<head>` của mọi trang do scripts/build-seo.py sinh — CHẠY SAU script này:

    python3 scripts/build.py && python3 scripts/build-seo.py
"""
import html as html_mod
import json
import os
import re
import shutil

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
HTML = os.path.join(ROOT, "html")
DATA = os.path.join(ROOT, "data")
TEMPLATES = os.path.join(ROOT, "templates")

# PHẢI KHỚP y hệt hằng POST_CATEGORIES trong gas/Code.js. gas/ không nằm trong git nên 2 chỗ
# này KHÔNG tự đồng bộ được — sửa 1 bên thì sửa luôn bên kia (GAS.md mục II.5).
POST_CATEGORIES = [
    "Cẩm nang du lịch",
    "Kinh nghiệm đi lại",
    "Bảng giá",
    "Tin tức",
]

CATEGORY_SLUGS = {
    "Cẩm nang du lịch": "cam-nang-du-lich",
    "Kinh nghiệm đi lại": "kinh-nghiem-di-lai",
    "Bảng giá": "bang-gia",
    "Tin tức": "tin-tuc",
}

BLOG_IMAGE_PUBLIC = "/assets/images/blog/"


def esc(s):
    return html_mod.escape(str(s if s is not None else ""), quote=True)


def load_json(name, default):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def read_template(name):
    with open(os.path.join(TEMPLATES, name), encoding="utf-8") as fh:
        return fh.read()


def cover_url(post):
    """Bài CMS lưu `cover` là TÊN FILE trần ("<slug>-cover.jpg"); bài cũ lưu sẵn đường dẫn
    tuyệt đối. Phân biệt bằng dấu "/" ở đầu, đừng ghép tiền tố 2 lần."""
    c = str(post.get("cover") or "")
    if not c:
        return ""
    return c if c.startswith("/") else BLOG_IMAGE_PUBLIC + c


def all_posts():
    """CMS + bài cũ, mới nhất trước. CMS ghi đè nếu trùng slug."""
    legacy = load_json("legacy-posts.json", [])
    cms = load_json("posts.json", [])
    by_slug = {p["slug"]: p for p in legacy}
    for p in cms:
        p = dict(p)
        p["legacy"] = False
        by_slug[p["slug"]] = p
    posts = list(by_slug.values())
    # Ngày giảm dần; CÙNG ngày thì theo "order" tăng dần (bài cũ có sẵn thứ tự chốt cứng, bài
    # CMS không có nên xếp sau). Nếu chỉ sắp theo ngày, 4 bài cũ cùng ngày sẽ đảo lộn mỗi lần
    # build ra thứ tự khác với trang đang chạy.
    posts.sort(key=lambda p: (
        str(p.get("date", "")),
        -int(p.get("order", 9999)),
    ), reverse=True)
    return posts


def used_categories(posts):
    """Chỉ chuyên mục THẬT SỰ có bài mới sinh trang — tránh đẻ ra trang rỗng cho 4 chuyên mục
    cố định trong khi chỉ 2 cái có nội dung. Giữ đúng thứ tự của POST_CATEGORIES."""
    have = {str(p.get("category") or "") for p in posts}
    return [c for c in POST_CATEGORIES if c in have]


# ----------------------------------------------------------------- render nhỏ

def render_card(post):
    url = "/blog/" + post["slug"]
    return (
        '              <article class="blog-card">\n'
        '                <a href="%s" class="blog-card-thumb">\n'
        '                  <img src="%s" alt="%s" loading="lazy" />\n'
        '                </a>\n'
        '                <div class="blog-card-body">\n'
        '                  <h2><a href="%s">%s</a></h2>\n'
        '                  <p>%s</p>\n'
        '                </div>\n'
        '              </article>'
        % (esc(url), esc(cover_url(post)), esc(post.get("cover_alt") or post["title"]),
           esc(url), esc(post["title"]), esc(post.get("description", "")))
    )


def render_category_list(posts, active=None):
    out = []
    for cat in used_categories(posts):
        slug = CATEGORY_SLUGS[cat]
        cls = ' class="active"' if cat == active else ""
        out.append('                  <li><a href="/blog/danh-muc/%s"%s>%s</a></li>'
                   % (esc(slug), cls, esc(cat)))
    return "\n".join(out)


def render_related(posts, current_slug, limit=3):
    """3 bài khác mới nhất. Không lọc theo chuyên mục: số bài còn ít, lọc thêm dễ ra khối rỗng."""
    out = []
    for p in posts:
        if p["slug"] == current_slug:
            continue
        url = "/blog/" + p["slug"]
        out.append(
            '              <li>\n'
            '                <a href="%s" class="related-article-item">\n'
            '                  <span class="related-article-thumb">\n'
            '                    <img src="%s" alt="%s" loading="lazy" />\n'
            '                  </span>\n'
            '                  <span class="related-article-text">%s</span>\n'
            '                </a>\n'
            '              </li>'
            % (esc(url), esc(cover_url(p)), esc(p.get("cover_alt") or p["title"]), esc(p["title"]))
        )
        if len(out) >= limit:
            break
    return "\n".join(out)


def render_breadcrumb(items):
    """items: [(nhãn, href hoặc None)]. Phần tử cuối không có link (trang hiện tại)."""
    parts = ['            <a href="/">Trang chủ</a>']
    for label, href in items:
        parts.append("            <span>/</span>")
        if href:
            parts.append('            <a href="%s">%s</a>' % (esc(href), esc(label)))
        else:
            parts.append("            <span>%s</span>" % esc(label))
    return "\n".join(parts)


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


# ------------------------------------------------------------------ build lớn

def build_posts(posts):
    """Chỉ render bài CMS. Bài cũ giữ nguyên trang chi tiết viết tay."""
    tpl = read_template("blog-post.html")
    cms = [p for p in posts if not p.get("legacy")]
    for post in cms:
        detail = load_json(os.path.join("blog", post["slug"] + ".json"), None)
        if detail is None:
            raise SystemExit(
                "Thiếu data/blog/%s.json (có trong danh sách nhưng không có nội dung) - "
                "kiểm tra lại thao tác Lưu gần nhất." % post["slug"]
            )
        page = (tpl
                .replace("{{TITLE}}", esc(detail.get("title", post["title"])))
                .replace("{{BREADCRUMB}}", esc(detail.get("breadcrumb") or detail.get("title", "")))
                # content_html là HTML do trình soạn thảo sinh -> KHÔNG escape.
                .replace("{{CONTENT}}", detail.get("content_html", ""))
                .replace("{{RELATED}}", render_related(posts, post["slug"]))
                .replace("{{CATEGORIES}}", render_category_list(posts, active=post.get("category"))))
        write(os.path.join(HTML, "blog", post["slug"], "index.html"), page)
    return cms


def build_blog_list(posts):
    tpl = read_template("blog-list.html")
    page = (tpl
            .replace("{{HEADING}}", "BLOG")
            .replace("{{BREADCRUMB}}", render_breadcrumb([("Blog", None)]))
            .replace("{{CARDS}}", "\n\n".join(render_card(p) for p in posts))
            .replace("{{CATEGORIES}}", render_category_list(posts)))
    write(os.path.join(HTML, "blog", "index.html"), page)


def build_categories(posts):
    tpl = read_template("blog-list.html")
    built = []
    for cat in used_categories(posts):
        slug = CATEGORY_SLUGS[cat]
        subset = [p for p in posts if p.get("category") == cat]
        page = (tpl
                .replace("{{HEADING}}", esc(cat.upper()))
                .replace("{{BREADCRUMB}}", render_breadcrumb([("Blog", "/blog"), (cat, None)]))
                .replace("{{CARDS}}", "\n\n".join(render_card(p) for p in subset))
                .replace("{{CATEGORIES}}", render_category_list(posts, active=cat)))
        write(os.path.join(HTML, "blog", "danh-muc", slug, "index.html"), page)
        built.append(slug)
    return built


def prune_orphans(posts, built_categories):
    """Xoá thư mục bài/chuyên mục không còn trong data/.

    Build script chỉ TẠO/GHI ĐÈ thì trang đã xoá qua CMS vẫn truy cập được vô thời hạn trên
    site thật và Google vẫn tiếp tục lập chỉ mục (gotcha #19 của skill).
    ⚠️ Chỉ đụng thư mục bài CMS — thư mục bài viết tay cũ (legacy) TUYỆT ĐỐI không xoá.
    """
    legacy_slugs = {p["slug"] for p in load_json("legacy-posts.json", [])}
    valid_slugs = {p["slug"] for p in posts} | legacy_slugs
    removed = []

    blog_dir = os.path.join(HTML, "blog")
    for name in sorted(os.listdir(blog_dir)):
        path = os.path.join(blog_dir, name)
        if not os.path.isdir(path) or name == "danh-muc":
            continue
        if name not in valid_slugs:
            shutil.rmtree(path)
            removed.append("blog/" + name)

    cat_dir = os.path.join(blog_dir, "danh-muc")
    if os.path.isdir(cat_dir):
        for name in sorted(os.listdir(cat_dir)):
            path = os.path.join(cat_dir, name)
            if os.path.isdir(path) and name not in built_categories:
                shutil.rmtree(path)
                removed.append("blog/danh-muc/" + name)
    return removed


def main():
    posts = all_posts()
    cms = build_posts(posts)
    build_blog_list(posts)
    cats = build_categories(posts)
    removed = prune_orphans(posts, cats)

    print("bài CMS   : %d" % len(cms))
    print("bài cũ    : %d" % len([p for p in posts if p.get("legacy")]))
    print("tổng liệt kê: %d" % len(posts))
    print("chuyên mục : %s" % (", ".join(cats) or "(không có)"))
    if removed:
        print("đã dọn     : %s" % ", ".join(removed))


if __name__ == "__main__":
    main()
