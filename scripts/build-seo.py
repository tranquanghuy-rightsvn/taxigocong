#!/usr/bin/env python3
"""
Regenerate <head> (meta tags, canonical, Open Graph, Twitter, JSON-LD) for every
page in html/, plus robots.txt and sitemap.xml.

Run from anywhere:  python3 scripts/build-seo.py
"""
import json
import os
import re
from datetime import date

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "html")
ROOT = os.path.normpath(ROOT)

SITE = "https://taxigocongdongthap.com"
BRAND = "Taxi Gò Công"
PHONE = "+84386263287"
PHONE_DISPLAY = "0386 263 287"
EMAIL = "taxigocong@gmail.com"
LOCALITY = "Gò Công"
REGION = "Tiền Giang"
GEO_LAT = "10.3653"
GEO_LON = "106.6664"
THEME = "#cc1e2c"
TODAY = date.today().isoformat()
BLOG_PUBLISHED = "2026-09-16"

AREA_SERVED = [
    "Gò Công", "Tiền Giang", "Đồng Tháp",
    "Mỹ Tho", "Cao Lãnh", "Lấp Vò", "Gò Công Đông", "Gò Công Tây",
]

# ---------------------------------------------------------------- page config
# key = path of index.html relative to html/
P = {}


def page(path, **kw):
    # Ảnh OG dựng sẵn trong /assets/og/ luôn đúng 1200x630 (scripts/make-og-images.py sinh ra).
    # Ảnh bìa bài CMS (đường dẫn bắt đầu bằng "/") thì không biết kích thước -> để trống.
    if not kw["og"].startswith("/"):
        kw.setdefault("og_w", 1200)
        kw.setdefault("og_h", 630)
    P[path] = kw


page(
    "index.html",
    url="/",
    kind="home",
    title="Taxi Gò Công - Đặt Xe Nhanh 24/7 | Nội Thành, Liên Tỉnh, Sân Bay",
    desc="Taxi Gò Công - taxi nội thành, liên tỉnh, đưa đón sân bay tại Gò Công, Tiền Giang, Đồng Tháp. Giá cước niêm yết, đón đúng giờ. Hotline 0386 263 287, 24/7.",
    kw="taxi Gò Công, taxi Tiền Giang, đặt taxi Gò Công, taxi giá rẻ Gò Công, taxi liên tỉnh Tiền Giang Đồng Tháp, xe đưa đón sân bay Gò Công",
    og="og-default.jpg",
    og_alt="Taxi Gò Công - đặt xe nhanh 24/7 tại Gò Công, Tiền Giang, Đồng Tháp",
    crumbs=[],
)

page(
    "gioi-thieu/index.html",
    url="/gioi-thieu/",
    kind="about",
    title="Giới Thiệu Taxi Gò Công - Đơn Vị Vận Tải Uy Tín Tại Tiền Giang",
    desc="Taxi Gò Công - đơn vị vận tải hành khách uy tín tại Gò Công, Tiền Giang, Đồng Tháp. Đội xe đời mới 4-16 chỗ, tài xế thông thạo địa bàn, phục vụ 24/7.",
    kw="giới thiệu taxi Gò Công, về chúng tôi, taxi uy tín Tiền Giang, hãng taxi Gò Công",
    og="og-gioi-thieu.jpg",
    og_alt="Giới thiệu Taxi Gò Công",
    crumbs=[("Giới thiệu", "/gioi-thieu/")],
)

page(
    "dich-vu/index.html",
    url="/dich-vu/",
    kind="service_list",
    title="Dịch Vụ Taxi Gò Công - Nội Thành, Liên Tỉnh, Sân Bay, Du Lịch",
    desc="Dịch vụ Taxi Gò Công: taxi nội thành, liên tỉnh Tiền Giang - Đồng Tháp, đưa đón sân bay, xe du lịch, xe hợp đồng và cho thuê xe tự lái. Phục vụ 24/7.",
    kw="dịch vụ taxi Gò Công, taxi liên tỉnh, đưa đón sân bay, xe du lịch, xe hợp đồng, cho thuê xe tự lái",
    og="og-default.jpg",
    og_alt="Các dịch vụ của Taxi Gò Công",
    crumbs=[("Dịch vụ", "/dich-vu/")],
)

page(
    "bang-gia/index.html",
    url="/bang-gia/",
    kind="pricing",
    title="Bảng Giá Taxi Gò Công 2026 - Giá Cước Niêm Yết Minh Bạch",
    desc="Bảng giá Taxi Gò Công: nội thành từ 45.000đ, liên tỉnh Tiền Giang - Đồng Tháp, sân bay Tân Sơn Nhất, Cần Thơ. Giá niêm yết rõ ràng, không phát sinh.",
    kw="bảng giá taxi Gò Công, giá cước taxi Gò Công, giá xe sân bay Tân Sơn Nhất, giá taxi liên tỉnh Tiền Giang",
    og="og-bang-gia.jpg",
    og_alt="Bảng giá dịch vụ Taxi Gò Công",
    crumbs=[("Bảng giá", "/bang-gia/")],
)

page(
    "tuyen-duong/index.html",
    url="/tuyen-duong/",
    kind="routes",
    title="Tuyến Đường Taxi Gò Công - Nội Thành, Liên Tỉnh Và Sân Bay",
    desc="Tuyến đường Taxi Gò Công phục vụ: nội thành Gò Công, liên tỉnh Tiền Giang - Đồng Tháp, sân bay Tân Sơn Nhất, Cần Thơ và tuyến đường dài theo yêu cầu.",
    kw="tuyến đường taxi Gò Công, taxi Tiền Giang Đồng Tháp, tuyến taxi sân bay, xe Gò Công đi Mỹ Tho",
    og="og-tuyen-duong.jpg",
    og_alt="Các tuyến đường Taxi Gò Công phục vụ",
    crumbs=[("Tuyến đường", "/tuyen-duong/")],
)

page(
    "lien-he/index.html",
    url="/lien-he/",
    kind="contact",
    title="Liên Hệ Taxi Gò Công - Hotline 0386 263 287 Hỗ Trợ 24/7",
    desc="Liên hệ Taxi Gò Công - gọi hotline 0386 263 287, gửi email taxigocong@gmail.com hoặc để lại lời nhắn, chúng tôi phản hồi nhanh nhất và hỗ trợ đặt xe 24/7.",
    kw="liên hệ taxi Gò Công, hotline taxi Gò Công, số điện thoại taxi Gò Công, đặt xe Gò Công",
    og="og-lien-he.jpg",
    og_alt="Liên hệ Taxi Gò Công - hotline 0386 263 287",
    crumbs=[("Liên hệ", "/lien-he/")],
)

# --- service detail pages ------------------------------------------------
SERVICES = [
    dict(
        slug="taxi-noi-thanh-go-cong",
        title="Taxi Nội Thành Gò Công - Giá Rẻ, Đón Đúng Giờ 24/7",
        name="Taxi nội thành Gò Công",
        desc="Taxi nội thành Gò Công giá rẻ từ 45.000đ, đón đúng giờ, phục vụ 24/7. Đặt xe nhanh chóng tới mọi điểm trong khu vực Gò Công, Tiền Giang.",
        kw="taxi nội thành Gò Công, taxi giá rẻ Gò Công, đặt taxi Gò Công, tổng đài taxi Gò Công",
        og="og-taxi-noi-thanh.jpg",
        service_type="Taxi nội thành",
        tab="noithanh",
        area=["Gò Công", "Gò Công Đông", "Gò Công Tây", "Tiền Giang"],
    ),
    dict(
        slug="taxi-lien-tinh-tien-giang-dong-thap",
        title="Taxi Liên Tỉnh Tiền Giang - Đồng Tháp | Đón Tận Nơi, Giá Rẻ",
        name="Taxi liên tỉnh Tiền Giang - Đồng Tháp",
        desc="Dịch vụ taxi liên tỉnh Gò Công đi Tiền Giang, Đồng Tháp giá rẻ, đón tận nơi, xe đời mới 4-16 chỗ, phục vụ 24/7, báo giá trọn gói trước chuyến đi.",
        kw="taxi liên tỉnh Tiền Giang, taxi Gò Công đi Đồng Tháp, xe liên tỉnh giá rẻ, taxi đi Mỹ Tho Cao Lãnh",
        og="og-lien-tinh.jpg",
        service_type="Taxi liên tỉnh",
        tab="tiengiang",
        area=["Tiền Giang", "Đồng Tháp", "Mỹ Tho", "Cao Lãnh", "Lấp Vò"],
    ),
    dict(
        slug="dua-don-san-bay-tan-son-nhat",
        title="Xe Đưa Đón Sân Bay Tân Sơn Nhất Từ Gò Công - Giá Rẻ, Đúng Giờ",
        name="Xe đưa đón sân bay Tân Sơn Nhất",
        desc="Dịch vụ đưa đón sân bay Tân Sơn Nhất từ Gò Công, Tiền Giang, Đồng Tháp - giá niêm yết, đón tận nơi, theo dõi giờ bay, hỗ trợ 24/7.",
        kw="xe sân bay Tân Sơn Nhất, đưa đón sân bay Tân Sơn Nhất, taxi sân bay giá rẻ, xe Gò Công đi Tân Sơn Nhất",
        og="og-san-bay-tsn.jpg",
        service_type="Đưa đón sân bay",
        tab="tsn",
        area=["Gò Công", "Tiền Giang", "Đồng Tháp", "Thành phố Hồ Chí Minh"],
    ),
    dict(
        slug="dua-don-san-bay-can-tho",
        title="Xe Đưa Đón Sân Bay Cần Thơ Từ Gò Công - Giá Rẻ, Đúng Giờ",
        name="Xe đưa đón sân bay Cần Thơ",
        desc="Dịch vụ đưa đón sân bay Cần Thơ từ Gò Công, Tiền Giang, Đồng Tháp - giá niêm yết, đón tận nơi, tài xế đúng giờ, hỗ trợ 24/7.",
        kw="xe sân bay Cần Thơ, đưa đón sân bay Cần Thơ, taxi sân bay giá rẻ, xe Gò Công đi Cần Thơ",
        og="og-san-bay-can-tho.jpg",
        service_type="Đưa đón sân bay",
        tab="cantho",
        area=["Gò Công", "Tiền Giang", "Đồng Tháp", "Cần Thơ"],
    ),
    dict(
        slug="xe-du-lich-tham-quan",
        title="Xe Du Lịch, Tham Quan Gò Công - Thuê Xe Theo Tour Giá Rẻ",
        name="Xe du lịch, tham quan",
        desc="Dịch vụ xe du lịch, tham quan tại Gò Công, Tiền Giang, Đồng Tháp - đón trả tận nơi, đa dạng xe 4-16 chỗ, giá trọn gói theo lịch trình.",
        kw="xe du lịch Gò Công, thuê xe tham quan, xe đi tour Tiền Giang, thuê xe du lịch miền Tây",
        og="og-du-lich.jpg",
        service_type="Xe du lịch",
        tab="dulich",
        area=AREA_SERVED,
    ),
    dict(
        slug="xe-hop-dong-su-kien",
        title="Xe Hợp Đồng, Sự Kiện Gò Công - Thuê Xe Theo Yêu Cầu",
        name="Xe hợp đồng, sự kiện",
        desc="Dịch vụ xe hợp đồng, xe sự kiện tại Gò Công, Tiền Giang - phục vụ công ty, đám cưới, hội nghị, đưa đón nhân viên theo hợp đồng dài hạn.",
        kw="xe hợp đồng Gò Công, thuê xe sự kiện, xe đưa đón công ty, xe cưới Gò Công",
        og="og-hop-dong.jpg",
        service_type="Xe hợp đồng",
        tab=None,
        area=AREA_SERVED,
    ),
    dict(
        slug="xe-duong-dai-theo-yeu-cau",
        title="Xe Đường Dài Theo Yêu Cầu - Taxi Gò Công Đi Tỉnh Xa",
        name="Xe đường dài theo yêu cầu",
        desc="Dịch vụ xe đường dài theo yêu cầu từ Gò Công đi các tỉnh, thành xa - xe đời mới, tài xế kinh nghiệm, giá thoả thuận rõ ràng trước chuyến đi.",
        kw="xe đường dài Gò Công, taxi đường dài giá rẻ, thuê xe đi tỉnh xa, xe Gò Công đi Đà Lạt",
        og="og-duong-dai.jpg",
        service_type="Xe đường dài",
        tab=None,
        area=AREA_SERVED,
    ),
    dict(
        slug="cho-thue-xe-tu-lai",
        title="Cho Thuê Xe Tự Lái Gò Công - Thủ Tục Nhanh, Giá Tốt",
        name="Cho thuê xe tự lái",
        desc="Dịch vụ cho thuê xe tự lái tại Gò Công, Tiền Giang - xe đời mới, thủ tục nhanh gọn, giao nhận xe tận nơi, giá thuê theo ngày hoặc theo tuần.",
        kw="thuê xe tự lái Gò Công, cho thuê xe tự lái Tiền Giang, thuê xe giá rẻ, thuê xe theo ngày",
        og="og-tu-lai.jpg",
        service_type="Cho thuê xe tự lái",
        tab=None,
        area=["Gò Công", "Tiền Giang"],
    ),
]

for sv in SERVICES:
    page(
        "dich-vu/%s/index.html" % sv["slug"],
        url="/dich-vu/%s/" % sv["slug"],
        kind="service",
        title=sv["title"],
        desc=sv["desc"],
        kw=sv["kw"],
        og=sv["og"],
        og_alt=sv["name"] + " - " + BRAND,
        crumbs=[("Dịch vụ", "/dich-vu/"), (sv["name"], "/dich-vu/%s/" % sv["slug"])],
        service=sv,
    )

# --- blog ----------------------------------------------------------------
# Bài viết + chuyên mục KHÔNG khai cứng ở đây: đọc từ data/ để bài mới do CMS đăng cũng có
# <head> đầy đủ mà không phải sửa script. scripts/build.py chạy TRƯỚC, sinh ra file .html;
# script này chạy SAU, điền <head> cho chúng.
DATA_DIR = os.path.join(ROOT, "..", "data")


def load_data(name, default):
    path = os.path.normpath(os.path.join(DATA_DIR, name))
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


CATEGORY_SLUGS = {
    "Cẩm nang du lịch": "cam-nang-du-lich",
    "Kinh nghiệm đi lại": "kinh-nghiem-di-lai",
    "Bảng giá": "bang-gia",
    "Tin tức": "tin-tuc",
}

# Ảnh OG dựng sẵn cho 4 bài viết tay cũ (ảnh bìa gốc của chúng không đúng tỉ lệ 1200x630).
LEGACY_POST_OG = {
    "kinh-nghiem-don-xe-san-bay-tan-son-nhat": "og-blog-tsn.jpg",
    "kinh-nghiem-don-xe-san-bay-can-tho": "og-blog-cantho.jpg",
    "cam-nang-du-lich-go-cong": "og-blog-gocong.jpg",
    "kinh-nghiem-du-lich-dong-thap-mua-nuoc-noi": "og-blog-dongthap.jpg",
}
CATEGORY_OG = {
    "cam-nang-du-lich": "og-dm-cam-nang.jpg",
    "kinh-nghiem-di-lai": "og-dm-kinh-nghiem.jpg",
}

_legacy = load_data("legacy-posts.json", [])
_cms = load_data("posts.json", [])
_by_slug = {p["slug"]: dict(p, legacy=True) for p in _legacy}
for _p in _cms:
    _by_slug[_p["slug"]] = dict(_p, legacy=False)
ALL_POSTS = sorted(
    _by_slug.values(),
    key=lambda p: (str(p.get("date", "")), -int(p.get("order", 9999))),
    reverse=True,
)

page(
    "blog/index.html",
    url="/blog/",
    kind="blog",
    title="Blog Taxi Gò Công - Kinh Nghiệm Đi Lại & Cẩm Nang Du Lịch",
    desc="Blog Taxi Gò Công - kinh nghiệm đi lại, cẩm nang du lịch, bảng giá và tin tức mới nhất về dịch vụ taxi tại Gò Công, Tiền Giang, Đồng Tháp.",
    kw="blog taxi Gò Công, kinh nghiệm đi lại, cẩm nang du lịch Gò Công, tin tức taxi",
    og="og-blog.jpg",
    og_alt="Blog Taxi Gò Công",
    crumbs=[("Blog", "/blog/")],
)

def _cat_desc(cat):
    return ("Các bài viết thuộc chuyên mục %s trên blog Taxi Gò Công — kinh nghiệm, cẩm nang "
            "và tin tức mới nhất tại Gò Công, Tiền Giang, Đồng Tháp." % cat.lower())


# Chuyên mục: chỉ sinh trang cho chuyên mục THẬT SỰ có bài (khớp scripts/build.py).
_used_cats = [c for c in CATEGORY_SLUGS if any(p.get("category") == c for p in ALL_POSTS)]

for _cat in _used_cats:
    _slug = CATEGORY_SLUGS[_cat]
    _og = CATEGORY_OG.get(_slug, "og-blog.jpg")
    _desc = _cat_desc(_cat)
    page(
        "blog/danh-muc/%s/index.html" % _slug,
        url="/blog/danh-muc/%s/" % _slug,
        kind="category",
        title="%s - Blog Taxi Gò Công" % _cat,
        desc=_desc[:158],
        kw="%s, blog taxi Gò Công, kinh nghiệm đi lại Tiền Giang" % _cat.lower(),
        og=_og,
        og_alt="%s - Blog Taxi Gò Công" % _cat,
        crumbs=[("Blog", "/blog/"), (_cat, "/blog/danh-muc/%s/" % _slug)],
        category={"slug": _slug, "name": _cat},
    )

for _po in ALL_POSTS:
    _slug = _po["slug"]
    _cat = _po.get("category") or ""
    _title = _po["title"]
    _desc = _po.get("description", "")
    # Bài viết tay cũ dùng ảnh OG dựng sẵn; bài CMS dùng chính ảnh bìa người viết tải lên.
    if _po.get("legacy"):
        _og = LEGACY_POST_OG.get(_slug, "og-blog.jpg")
    else:
        _cover = str(_po.get("cover") or "")
        _og = _cover if _cover.startswith("/") else "/assets/images/blog/" + _cover
    _crumbs = [("Blog", "/blog/")]
    if _cat in CATEGORY_SLUGS:
        _crumbs.append((_cat, "/blog/danh-muc/%s/" % CATEGORY_SLUGS[_cat]))
    _crumbs.append((_po.get("breadcrumb") or _title, "/blog/%s/" % _slug))
    page(
        "blog/%s/index.html" % _slug,
        url="/blog/%s/" % _slug,
        kind="post",
        title=(_title if len(_title) <= 60 else _title[:57].rstrip() + "..."),
        desc=_desc,
        kw=", ".join(filter(None, [_cat.lower(), "taxi Gò Công", "Tiền Giang", "Đồng Tháp"])),
        og=_og,
        og_alt=_title,
        crumbs=_crumbs,
        post={
            "slug": _slug,
            "headline": _title,
            "cat": CATEGORY_SLUGS.get(_cat, ""),
            "cat_name": _cat,
            "date": _po.get("date", BLOG_PUBLISHED),
        },
    )


# ------------------------------------------------------- content extraction
def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]*>", " ", s)).strip()


def count_words(rel):
    """Words in the page body only - head, scripts, styles and svg excluded."""
    html = read(rel)
    html = re.sub(r"<head>.*?</head>", " ", html, flags=re.S)
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S)
    html = re.sub(r"<svg.*?</svg>", " ", html, flags=re.S)
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    main = re.search(r"<main.*?</main>", html, re.S)
    return len(strip_tags(main.group(0) if main else html).split())


def extract_faq():
    """Pull the Q/A pairs straight out of the homepage so schema can't drift."""
    html = read("index.html")
    chunks = html.split('<div class="faq-item">')[1:]
    faqs = []
    for chunk in chunks:
        q = re.search(r'<button class="faq-question".*?>(.*?)</button>', chunk, re.S)
        a = re.search(r'<div class="faq-answer">(.*?)(?:</div>|\Z)', chunk, re.S)
        if not (q and a):
            continue
        qt = strip_tags(re.sub(r"<svg.*?</svg>", "", q.group(1), flags=re.S))
        at = strip_tags(a.group(1))
        if qt and at:
            faqs.append((qt, at))
    if not faqs:
        raise SystemExit("extract_faq(): no FAQ items found on the homepage")
    return faqs


PRICE_TABS = [
    ("noithanh", "Taxi nội thành Gò Công"),
    ("tiengiang", "Taxi liên tỉnh Tiền Giang"),
    ("dongthap", "Taxi liên tỉnh Đồng Tháp"),
    ("tsn", "Xe đưa đón sân bay Tân Sơn Nhất"),
    ("cantho", "Xe đưa đón sân bay Cần Thơ"),
    ("dulich", "Xe du lịch, tham quan"),
]


def extract_prices():
    """{tab: (min, max)} parsed from the real bảng giá tables."""
    html = read("bang-gia/index.html")
    out = {}
    for tab, _ in PRICE_TABS:
        m = re.search(r'id="tab-%s".*?</table>' % tab, html, re.S)
        if not m:
            continue
        nums = [int(x.replace(".", "")) for x in re.findall(r"([0-9]{1,3}(?:\.[0-9]{3})+)đ", m.group(0))]
        if nums:
            out[tab] = (min(nums), max(nums))
    return out


FAQS = extract_faq()
PRICES = extract_prices()
ALL_PRICES = [v for pair in PRICES.values() for v in pair]
PRICE_MIN, PRICE_MAX = (min(ALL_PRICES), max(ALL_PRICES)) if ALL_PRICES else (0, 0)


# ------------------------------------------------------------------ JSON-LD
def org_node():
    node = {
        "@type": ["TaxiService", "LocalBusiness"],
        "@id": SITE + "/#organization",
        "name": BRAND,
        "alternateName": "Taxi Go Cong",
        "url": SITE + "/",
        "description": "Dịch vụ taxi và cho thuê xe uy tín tại Gò Công, Tiền Giang, Đồng Tháp: taxi nội thành, taxi liên tỉnh, đưa đón sân bay, xe du lịch, xe hợp đồng và cho thuê xe tự lái, phục vụ 24/7.",
        "logo": {
            "@type": "ImageObject",
            "@id": SITE + "/#logo",
            "url": SITE + "/assets/images/logo.webp",
            "contentUrl": SITE + "/assets/images/logo.webp",
            "width": 285,
            "height": 168,
            "caption": BRAND,
        },
        "image": {"@id": SITE + "/#logo"},
        "telephone": PHONE,
        "email": EMAIL,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": LOCALITY,
            "addressRegion": REGION,
            "addressCountry": "VN",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": float(GEO_LAT),
            "longitude": float(GEO_LON),
        },
        "areaServed": [{"@type": "City", "name": n} for n in AREA_SERVED],
        "serviceArea": {
            "@type": "GeoCircle",
            "geoMidpoint": {
                "@type": "GeoCoordinates",
                "latitude": float(GEO_LAT),
                "longitude": float(GEO_LON),
            },
            "geoRadius": "100000",
        },
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": [
                "Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday", "Sunday",
            ],
            "opens": "00:00",
            "closes": "23:59",
        }],
        "currenciesAccepted": "VND",
        "paymentAccepted": "Tiền mặt, Chuyển khoản ngân hàng, Ví điện tử",
        "priceRange": "45.000đ - 1.300.000đ",
        "knowsLanguage": "vi",
        "contactPoint": [{
            "@type": "ContactPoint",
            "telephone": PHONE,
            "email": EMAIL,
            "contactType": "customer service",
            "areaServed": "VN",
            "availableLanguage": ["vi"],
            "hoursAvailable": {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": [
                    "Monday", "Tuesday", "Wednesday", "Thursday",
                    "Friday", "Saturday", "Sunday",
                ],
                "opens": "00:00",
                "closes": "23:59",
            },
        }],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Dịch vụ Taxi Gò Công",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "@id": SITE + "/dich-vu/%s/#service" % sv["slug"],
                        "name": sv["name"],
                        "url": SITE + "/dich-vu/%s/" % sv["slug"],
                    },
                }
                for sv in SERVICES
            ],
        },
    }
    return node


def website_node():
    return {
        "@type": "WebSite",
        "@id": SITE + "/#website",
        "url": SITE + "/",
        "name": BRAND,
        "description": "Dịch vụ taxi uy tín tại Gò Công, Tiền Giang, Đồng Tháp - đặt xe nhanh 24/7.",
        "publisher": {"@id": SITE + "/#organization"},
        "inLanguage": "vi-VN",
    }


def visible_breadcrumb(rel):
    """Read the <nav class="breadcrumb"> the visitor actually sees.

    Google wants BreadcrumbList to mirror the on-page trail, so the markup is
    the source of truth and the `crumbs` config is only a fallback.
    """
    body = re.sub(r"<head>.*?</head>", "", read(rel), flags=re.S)
    nav = re.search(r'<nav[^>]*class="[^"]*breadcrumb[^"]*"[^>]*>(.*?)</nav>', body, re.S)
    if not nav:
        return None
    out = []
    for m in re.finditer(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>|<span[^>]*>(.*?)</span>',
                         nav.group(1), re.S):
        href, txt = (m.group(1), m.group(2)) if m.group(1) is not None else (None, m.group(3))
        label = strip_tags(txt)
        if not label or label == "/":
            continue
        out.append((label, href))
    return out or None


def norm_url(href):
    """Site-absolute URL with the trailing slash the canonical uses."""
    if href is None:
        return None
    if href.startswith("http"):
        return href
    if not href.endswith("/"):
        href += "/"
    return SITE + href


def breadcrumb_node(cfg):
    crumbs = visible_breadcrumb(cfg["_file"])
    if crumbs is None:  # no on-page trail (homepage) -> fall back to config
        crumbs = [("Trang chủ", "/")] + list(cfg["crumbs"])

    items = []
    for i, (name, href) in enumerate(crumbs, start=1):
        it = {"@type": "ListItem", "position": i, "name": name}
        url = norm_url(href)
        if url is None and i == len(crumbs):
            url = SITE + cfg["url"]          # current page has no link in the nav
        if url:
            it["item"] = url
        items.append(it)

    return {
        "@type": "BreadcrumbList",
        "@id": SITE + cfg["url"] + "#breadcrumb",
        "itemListElement": items,
    }


WEBPAGE_TYPE = {
    "home": ["WebPage", "FAQPage"],
    "about": "AboutPage",
    "contact": "ContactPage",
    "service_list": "CollectionPage",
    "service": "WebPage",
    "pricing": "WebPage",
    "routes": "CollectionPage",
    "blog": "CollectionPage",
    "category": "CollectionPage",
    "post": "WebPage",
}


def webpage_node(cfg):
    url = SITE + cfg["url"]
    node = {
        "@type": WEBPAGE_TYPE[cfg["kind"]],
        "@id": url + "#webpage",
        "url": url,
        "name": cfg["title"],
        "description": cfg["desc"],
        "isPartOf": {"@id": SITE + "/#website"},
        "about": {"@id": SITE + "/#organization"},
        "breadcrumb": {"@id": url + "#breadcrumb"},
        "primaryImageOfPage": {"@id": url + "#primaryimage"},
        "inLanguage": "vi-VN",
        "datePublished": BLOG_PUBLISHED + "T00:00:00+07:00",
        "dateModified": TODAY + "T00:00:00+07:00",
        "potentialAction": {
            "@type": "ReadAction",
            "target": [url],
        },
    }
    if cfg["kind"] == "home":
        node["mainEntity"] = [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in FAQS
        ]
    return node


def og_path(cfg):
    """Đường dẫn ảnh OG tính từ gốc site.

    2 nguồn: ảnh OG dựng sẵn 1200x630 trong /assets/og/ (21 trang tĩnh), và ảnh bìa do người
    viết tải lên cho bài CMS (kích thước tuỳ ảnh gốc). Giá trị bắt đầu bằng "/" là đã đủ
    đường dẫn, không ghép tiền tố nữa."""
    og = cfg["og"]
    return og if og.startswith("/") else "/assets/og/" + og


def image_node(cfg):
    url = SITE + cfg["url"]
    node = {
        "@type": "ImageObject",
        "@id": url + "#primaryimage",
        "url": SITE + og_path(cfg),
        "contentUrl": SITE + og_path(cfg),
        "caption": cfg["og_alt"],
        "inLanguage": "vi-VN",
    }
    # Chỉ khai kích thước khi BIẾT CHẮC. Ảnh bìa người viết tải lên không cố định tỉ lệ -
    # khai bừa 1200x630 là nói sai với Google.
    if cfg.get("og_w") and cfg.get("og_h"):
        node["width"] = cfg["og_w"]
        node["height"] = cfg["og_h"]
    return node


def service_node(cfg):
    sv = cfg["service"]
    url = SITE + cfg["url"]
    node = {
        "@type": "Service",
        "@id": url + "#service",
        "name": sv["name"],
        "description": sv["desc"],
        "url": url,
        "serviceType": sv["service_type"],
        "category": "Vận tải hành khách",
        "provider": {"@id": SITE + "/#organization"},
        "areaServed": [{"@type": "City", "name": n} for n in sv["area"]],
        "image": {"@id": url + "#primaryimage"},
        "mainEntityOfPage": {"@id": url + "#webpage"},
        "availableChannel": {
            "@type": "ServiceChannel",
            "serviceUrl": url,
            "servicePhone": {"@type": "ContactPoint", "telephone": PHONE},
            "availableLanguage": {"@type": "Language", "name": "Vietnamese", "alternateName": "vi"},
        },
    }
    rng = PRICES.get(sv["tab"]) if sv["tab"] else None
    if rng:
        node["offers"] = {
            "@type": "AggregateOffer",
            "priceCurrency": "VND",
            "lowPrice": rng[0],
            "highPrice": rng[1],
            "offerCount": 12,
            "availability": "https://schema.org/InStock",
            "url": SITE + "/bang-gia/",
            "seller": {"@id": SITE + "/#organization"},
        }
    return node


def offercatalog_node():
    """Real numbers, read back out of the bảng giá tables."""
    items = []
    for i, (tab, label) in enumerate(PRICE_TABS, start=1):
        rng = PRICES.get(tab)
        if not rng:
            continue
        items.append({
            "@type": "Offer",
            "position": i,
            "name": label,
            "priceCurrency": "VND",
            "priceSpecification": {
                "@type": "PriceSpecification",
                "priceCurrency": "VND",
                "minPrice": rng[0],
                "maxPrice": rng[1],
                "valueAddedTaxIncluded": True,
            },
            "availability": "https://schema.org/InStock",
            "seller": {"@id": SITE + "/#organization"},
            "itemOffered": {"@type": "Service", "name": label, "provider": {"@id": SITE + "/#organization"}},
        })
    return {
        "@type": "OfferCatalog",
        "@id": SITE + "/bang-gia/#offercatalog",
        "name": "Bảng giá dịch vụ Taxi Gò Công",
        "url": SITE + "/bang-gia/",
        "numberOfItems": len(items),
        "itemListElement": items,
    }


def blogposting_node(cfg):
    po = cfg["post"]
    url = SITE + cfg["url"]
    words = count_words(cfg["_file"])
    return {
        "@type": "BlogPosting",
        "@id": url + "#article",
        "headline": po["headline"],
        "name": po["headline"],
        "description": cfg["desc"],
        "url": url,
        "mainEntityOfPage": {"@id": url + "#webpage"},
        "isPartOf": {"@id": SITE + "/blog/#blog"},
        "datePublished": po["date"] + "T08:00:00+07:00",
        "dateModified": TODAY + "T00:00:00+07:00",
        "author": {"@id": SITE + "/#organization"},
        "publisher": {"@id": SITE + "/#organization"},
        "image": {"@id": url + "#primaryimage"},
        "thumbnailUrl": SITE + og_path(cfg),
        "articleSection": po["cat_name"],
        "keywords": cfg["kw"],
        "wordCount": words,
        "inLanguage": "vi-VN",
    }


def blog_node():
    return {
        "@type": "Blog",
        "@id": SITE + "/blog/#blog",
        "name": "Blog " + BRAND,
        "url": SITE + "/blog/",
        "description": "Kinh nghiệm đi lại và cẩm nang du lịch tại Gò Công, Tiền Giang, Đồng Tháp.",
        "publisher": {"@id": SITE + "/#organization"},
        "inLanguage": "vi-VN",
        "blogPost": [
            {
                "@type": "BlogPosting",
                "@id": SITE + "/blog/%s/#article" % po["slug"],
                "headline": po["title"],
                "url": SITE + "/blog/%s/" % po["slug"],
                "datePublished": po.get("date", BLOG_PUBLISHED) + "T08:00:00+07:00",
                "author": {"@id": SITE + "/#organization"},
            }
            for po in ALL_POSTS
        ],
    }


def itemlist_node(cfg, entries, name):
    return {
        "@type": "ItemList",
        "@id": SITE + cfg["url"] + "#itemlist",
        "name": name,
        "numberOfItems": len(entries),
        "itemListOrder": "https://schema.org/ItemListOrderAscending",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": n, "url": SITE + u}
            for i, (n, u) in enumerate(entries, start=1)
        ],
    }


def build_graph(cfg):
    graph = [org_node(), website_node(), webpage_node(cfg), image_node(cfg), breadcrumb_node(cfg)]
    kind = cfg["kind"]

    if kind == "service":
        graph.append(service_node(cfg))
    elif kind == "service_list":
        graph.append(itemlist_node(
            cfg,
            [(sv["name"], "/dich-vu/%s/" % sv["slug"]) for sv in SERVICES],
            "Dịch vụ Taxi Gò Công",
        ))
    elif kind == "pricing":
        graph.append(offercatalog_node())
    elif kind == "blog":
        graph.append(blog_node())
        graph.append(itemlist_node(
            cfg,
            [(po["title"], "/blog/%s/" % po["slug"]) for po in ALL_POSTS],
            "Bài viết mới nhất",
        ))
    elif kind == "category":
        posts = [po for po in ALL_POSTS
                 if CATEGORY_SLUGS.get(po.get("category")) == cfg["category"]["slug"]]
        graph.append(itemlist_node(
            cfg,
            [(po["title"], "/blog/%s/" % po["slug"]) for po in posts],
            cfg["category"]["name"],
        ))
    elif kind == "post":
        graph.append({
            "@type": "Blog",
            "@id": SITE + "/blog/#blog",
            "name": "Blog " + BRAND,
            "url": SITE + "/blog/",
            "publisher": {"@id": SITE + "/#organization"},
            "inLanguage": "vi-VN",
        })
        graph.append(blogposting_node(cfg))
    elif kind == "contact":
        graph.append({
            "@type": "ContactPoint",
            "@id": SITE + "/lien-he/#contactpoint",
            "telephone": PHONE,
            "email": EMAIL,
            "contactType": "customer service",
            "areaServed": "VN",
            "availableLanguage": ["vi"],
        })
    elif kind == "routes":
        graph.append(itemlist_node(
            cfg,
            [(label, "/bang-gia/") for _, label in PRICE_TABS],
            "Tuyến đường phục vụ",
        ))

    return {"@context": "https://schema.org", "@graph": graph}


# -------------------------------------------------------------- head render
ICONS = """    <link rel="icon" href="/favicon.ico" sizes="any" />
    <link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon/favicon-16x16.png" />
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon/favicon-32x32.png" />
    <link rel="icon" type="image/png" sizes="48x48" href="/assets/favicon/favicon-48x48.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/favicon/apple-touch-icon.png" />
    <link rel="manifest" href="/assets/favicon/site.webmanifest" />"""


def esc(s):
    return (s.replace("&", "&amp;").replace('"', "&quot;")
             .replace("<", "&lt;").replace(">", "&gt;"))


def render_head(cfg):
    url = SITE + cfg["url"]
    ogimg = SITE + og_path(cfg)
    ogtype = "article" if cfg["kind"] == "post" else "website"
    robots = "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"

    L = []
    a = L.append
    a("  <head>")
    a('    <meta charset="UTF-8" />')
    a('    <meta name="viewport" content="width=device-width, initial-scale=1.0" />')
    a("")
    a("    <!-- Primary meta -->")
    a("    <title>%s</title>" % esc(cfg["title"]))
    a('    <meta name="description" content="%s" />' % esc(cfg["desc"]))
    a('    <meta name="keywords" content="%s" />' % esc(cfg["kw"]))
    a('    <meta name="author" content="%s" />' % BRAND)
    a('    <meta name="publisher" content="%s" />' % BRAND)
    a('    <meta name="copyright" content="%s" />' % BRAND)
    a('    <meta name="robots" content="%s" />' % robots)
    a('    <meta name="googlebot" content="%s" />' % robots)
    a('    <meta name="bingbot" content="%s" />' % robots)
    a("")
    a("    <!-- Canonical & language -->")
    a('    <link rel="canonical" href="%s" />' % url)
    a('    <link rel="alternate" hreflang="vi-VN" href="%s" />' % url)
    a('    <link rel="alternate" hreflang="x-default" href="%s" />' % url)
    a("")
    a("    <!-- Local / geo -->")
    a('    <meta name="geo.region" content="VN-46" />')
    a('    <meta name="geo.placename" content="%s, %s" />' % (LOCALITY, REGION))
    a('    <meta name="geo.position" content="%s;%s" />' % (GEO_LAT, GEO_LON))
    a('    <meta name="ICBM" content="%s, %s" />' % (GEO_LAT, GEO_LON))
    a('    <meta name="contact" content="%s" />' % EMAIL)
    a('    <meta name="reply-to" content="%s" />' % EMAIL)
    a("")
    a("    <!-- Open Graph -->")
    a('    <meta property="og:site_name" content="%s" />' % BRAND)
    a('    <meta property="og:type" content="%s" />' % ogtype)
    a('    <meta property="og:locale" content="vi_VN" />')
    a('    <meta property="og:title" content="%s" />' % esc(cfg["title"]))
    a('    <meta property="og:description" content="%s" />' % esc(cfg["desc"]))
    a('    <meta property="og:url" content="%s" />' % url)
    a('    <meta property="og:image" content="%s" />' % ogimg)
    a('    <meta property="og:image:secure_url" content="%s" />' % ogimg)
    a('    <meta property="og:image:type" content="image/jpeg" />')
    if cfg.get("og_w") and cfg.get("og_h"):
        a('    <meta property="og:image:width" content="%d" />' % cfg["og_w"])
        a('    <meta property="og:image:height" content="%d" />' % cfg["og_h"])
    a('    <meta property="og:image:alt" content="%s" />' % esc(cfg["og_alt"]))
    if cfg["kind"] == "post":
        po = cfg["post"]
        a('    <meta property="article:published_time" content="%sT08:00:00+07:00" />' % po["date"])
        a('    <meta property="article:modified_time" content="%sT00:00:00+07:00" />' % TODAY)
        a('    <meta property="article:author" content="%s" />' % BRAND)
        a('    <meta property="article:publisher" content="%s" />' % BRAND)
        a('    <meta property="article:section" content="%s" />' % esc(po["cat_name"]))
        for tag in [t.strip() for t in cfg["kw"].split(",") if t.strip()]:
            a('    <meta property="article:tag" content="%s" />' % esc(tag))
    a("")
    a("    <!-- Twitter -->")
    a('    <meta name="twitter:card" content="summary_large_image" />')
    a('    <meta name="twitter:title" content="%s" />' % esc(cfg["title"]))
    a('    <meta name="twitter:description" content="%s" />' % esc(cfg["desc"]))
    a('    <meta name="twitter:image" content="%s" />' % ogimg)
    a('    <meta name="twitter:image:alt" content="%s" />' % esc(cfg["og_alt"]))
    a("")
    a("    <!-- App / theme -->")
    a('    <meta name="theme-color" content="%s" />' % THEME)
    a('    <meta name="color-scheme" content="light" />')
    a('    <meta name="application-name" content="%s" />' % BRAND)
    a('    <meta name="apple-mobile-web-app-title" content="%s" />' % BRAND)
    a('    <meta name="apple-mobile-web-app-capable" content="yes" />')
    a('    <meta name="apple-mobile-web-app-status-bar-style" content="default" />')
    a('    <meta name="mobile-web-app-capable" content="yes" />')
    a('    <meta name="format-detection" content="telephone=yes" />')
    a("")
    a("    <!-- Icons -->")
    a(ICONS)
    a("")
    a("    <!-- Styles -->")
    a('    <link rel="stylesheet" href="/css/reset.css" />')
    a('    <link rel="stylesheet" href="/css/style.css" />')
    a("")
    a("    <!-- Structured data -->")
    payload = json.dumps(build_graph(cfg), ensure_ascii=False, indent=2)
    payload = payload.replace("</", "<\\/")  # never break out of the script tag
    payload = "\n".join("      " + ln for ln in payload.splitlines())
    a('    <script type="application/ld+json">')
    a(payload)
    a("    </script>")
    a("  </head>")
    return "\n".join(L)


# ------------------------------------------------------------------- writers
HEAD_RE = re.compile(r"[ \t]*<head>.*?</head>", re.S)


def write_pages():
    for rel, cfg in sorted(P.items()):
        cfg["_file"] = rel
        path = os.path.join(ROOT, rel)
        html = read(rel)
        if not HEAD_RE.search(html):
            raise SystemExit("no <head> in " + rel)
        new = HEAD_RE.sub(lambda _: render_head(cfg), html, count=1)
        new = re.sub(r'<html lang="[^"]*">', '<html lang="vi">', new, count=1)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new)
        print("head  ", rel)


def write_manifest():
    data = {
        "id": "/",
        "name": BRAND + " - Đặt xe nhanh 24/7",
        "short_name": BRAND,
        "description": "Dịch vụ taxi uy tín tại Gò Công, Tiền Giang, Đồng Tháp: taxi nội thành, liên tỉnh, đưa đón sân bay, xe du lịch. Hotline " + PHONE_DISPLAY + ".",
        "lang": "vi",
        "dir": "ltr",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "orientation": "portrait-primary",
        "theme_color": THEME,
        "background_color": "#ffffff",
        "categories": ["travel", "navigation", "business"],
        "icons": [
            {"src": "/assets/favicon/favicon-16x16.png", "sizes": "16x16", "type": "image/png"},
            {"src": "/assets/favicon/favicon-32x32.png", "sizes": "32x32", "type": "image/png"},
            {"src": "/assets/favicon/favicon-48x48.png", "sizes": "48x48", "type": "image/png"},
            {"src": "/assets/favicon/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
            {"src": "/assets/favicon/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/assets/favicon/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        ],
        "shortcuts": [
            {"name": "Bảng giá", "url": "/bang-gia/"},
            {"name": "Dịch vụ", "url": "/dich-vu/"},
            {"name": "Liên hệ", "url": "/lien-he/"},
        ],
    }
    path = os.path.join(ROOT, "assets", "favicon", "site.webmanifest")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("wrote  site.webmanifest")


def write_robots():
    body = """# robots.txt - %s
# Cho phép mọi bot thu thập toàn bộ nội dung, kể cả CSS/JS
# (bot cần CSS/JS để render trang đúng như người dùng thấy).

User-agent: *
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Googlebot-Image
Allow: /

User-agent: Bingbot
Allow: /

# AI / answer-engine crawlers
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: %s/sitemap.xml
""" % (SITE, SITE)
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(body)
    print("wrote  robots.txt")


PRIORITY = {
    "home": ("1.0", "daily"),
    "service_list": ("0.9", "weekly"),
    "service": ("0.9", "weekly"),
    "pricing": ("0.9", "weekly"),
    "routes": ("0.8", "weekly"),
    "contact": ("0.7", "monthly"),
    "about": ("0.7", "monthly"),
    "blog": ("0.8", "weekly"),
    "category": ("0.6", "weekly"),
    "post": ("0.7", "monthly"),
}


def write_sitemap():
    rows = []
    for rel, cfg in sorted(P.items(), key=lambda kv: (kv[1]["url"] != "/", kv[1]["url"])):
        prio, freq = PRIORITY[cfg["kind"]]
        rows.append(
            "  <url>\n"
            "    <loc>%s</loc>\n"
            "    <lastmod>%s</lastmod>\n"
            "    <changefreq>%s</changefreq>\n"
            "    <priority>%s</priority>\n"
            "    <image:image>\n"
            "      <image:loc>%s%s</image:loc>\n"
            "      <image:title>%s</image:title>\n"
            "    </image:image>\n"
            "  </url>"
            % (SITE + cfg["url"], TODAY, freq, prio, SITE, og_path(cfg),
               esc(cfg["og_alt"]))
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
        + "\n".join(rows)
        + "\n</urlset>\n"
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(xml)
    print("wrote  sitemap.xml (%d urls)" % len(rows))


# Trang cố ý KHÔNG nằm trong pipeline SEO: có <head> riêng, noindex, không vào sitemap.
SEO_EXCLUDED = {"admin/index.html"}


def check_coverage():
    found = set()
    for dirpath, _, names in os.walk(ROOT):
        for n in names:
            if n.endswith(".html"):
                found.add(os.path.relpath(os.path.join(dirpath, n), ROOT))
    missing = found - set(P) - SEO_EXCLUDED
    if missing:
        raise SystemExit("pages missing from config: " + ", ".join(sorted(missing)))
    stale = SEO_EXCLUDED - found
    if stale:
        raise SystemExit("SEO_EXCLUDED trỏ tới trang không còn tồn tại: " + ", ".join(sorted(stale)))


if __name__ == "__main__":
    check_coverage()
    print("FAQ items: %d | price tabs: %d | range: %s-%s VND"
          % (len(FAQS), len(PRICES), PRICE_MIN, PRICE_MAX))
    write_pages()
    write_manifest()
    write_robots()
    write_sitemap()
