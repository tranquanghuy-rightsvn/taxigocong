# GAS.md — Guideline CMS Taxi Gò Công Đồng Tháp

> Nguồn quyết định CHỐT cho toàn bộ `gas/`. Đọc TOÀN BỘ file này trước khi sửa bất kỳ dòng
> nào trong `gas/Code.js`, `gas/app.html`, `gas/js.html`, `gas/css.html`, `gas/index.html`,
> `gas/email.html`. Không tự suy đoán thêm field/quy tắc nào không có ở đây.
>
> Theo playbook skill `free-cms-static-site-pipeline`, dự án mẫu ưu tiên: `xevip`.
> Sửa code xong phải đồng bộ ngược lại file này trong CÙNG một lượt sửa.

## 0. Phạm vi — ĐÚNG 4 tab quản lý, không làm rộng hơn

| Tab | Nguồn dữ liệu | Quyền tối thiểu |
|---|---|---|
| 1. Danh sách đặt xe | Sheet `Bookings` (form công khai ghi vào) | `admin` |
| 2. Danh sách liên hệ | Sheet `Contacts` (form công khai ghi vào) | `admin` |
| 3. Tin tức | GitHub `data/posts.json` + `data/blog/<slug>.json` | `editor` |
| 4. Người dùng | Sheet `Users` | `admin` |

Đặt xe và Liên hệ là **dữ liệu khách hàng** → `editor` cố ý KHÔNG thấy 2 tab này.

Domain thật: **https://taxigocongdongthap.com** (đã chốt 17/09/2026). Mọi canonical/og:url/
JSON-LD/sitemap của site dùng domain này.

## I. Đăng nhập

1. Luồng: nhập email → nhận OTP qua email → xác nhận → vào Admin. Không mật khẩu, không dựa
   vào session Google (người dùng không cùng Workspace domain với chủ script).
2. Chỉ email đã có trong sheet `Users` mới được gửi OTP.
3. **Account chủ script (người deploy) LUÔN hợp lệ và LUÔN là `root`** — không cần khai trong
   `Users`, không hiện trong UI quản lý người dùng. `requestOtp` phải tự cho phép ngoại lệ với
   email này (`ownerEmail_()`), song song với việc tra sheet `Users` — nếu không sẽ tự khoá
   chủ script ra khỏi hệ thống ngay từ lần đăng nhập đầu tiên.
4. **Phân quyền 3 cấp: `root` > `admin` > `editor`** (chốt 17/09/2026). Hành vi phân biệt:
   - `editor` — chỉ tab **Tin tức** (thêm/sửa/xoá bài). KHÔNG thấy đặt xe, liên hệ, người dùng.
   - `admin` — thêm tab **Đặt xe**, **Liên hệ**, **Người dùng** (quản lý được `admin`+`editor`).
   - `root` — chủ script, toàn quyền. Chỉ set được bằng cách sửa tay Sheet `Users`; UI không
     bao giờ hiển thị/đụng vào dòng `root`.
5. OTP sống **10 phút**, cooldown **60 giây**/email, tối đa **5 lần** nhập sai rồi phải xin mã
   mới. Token phiên sống **30 ngày**, lưu `localStorage`.
6. Server luôn `requireRole_` ở MỌI hàm. Ẩn nút/tab trên giao diện KHÔNG phải là bảo mật.

## II. Tin tức (bài viết blog)

1. **Field có ô nhập riêng trên giao diện:**
   - Tiêu đề (bắt buộc)
   - URL/slug — tự sinh từ tiêu đề (bỏ dấu + gạch ngang), **bất biến sau lần Lưu đầu** (mục III)
   - Danh mục — chọn từ danh sách CỐ ĐỊNH ở mục II.5, để trống được
   - Mô tả ngắn (dùng cho `meta description` + thẻ bài trên trang `/blog/`)
   - Ảnh bìa (bắt buộc — chặn Lưu nếu chưa có)
   - Nội dung: TinyMCE. Định dạng cần có: heading, bold/italic, list (bullet/số), link, bảng,
     blockquote, **và chèn ảnh trong nội dung**.
2. **CÓ chèn ảnh ngay trong nội dung bài** — bắt buộc có nút `quickimage` trên toolbar, bấm là
   mở thẳng file picker của hệ điều hành (KHÔNG dùng dialog "Image" mặc định của TinyMCE), hỗ
   trợ chọn nhiều ảnh. Dùng lại đúng hàm upload ảnh đã có. Ảnh chèn phải có `alt`/`title`:
   alt = caption ảnh, rơi về tiêu đề bài nếu caption còn rỗng/còn placeholder (mục 4b của
   `gas-backend-patterns.md`). Lúc Lưu: xoá hẳn `<figcaption>` nào còn placeholder.
3. **Field KHÔNG có ô nhập — server tự suy lúc Lưu:**
   - `seo_title` = `"<Tiêu đề> - Taxi Gò Công"` (đúng quy ước `<title>` của 4 bài viết tay đã có)
   - `breadcrumb` = tiêu đề
   - `cover` = luôn suy ra tất định `"<slug>-cover.jpg"` — KHÔNG nhận tên file tự do từ client;
     server tự kiểm tra file đó đã thật sự nằm trên GitHub chưa trước khi cho Lưu
   - `cover_alt` = tiêu đề
   - `date` = ngày Lưu lần đầu; bài đã có thì GIỮ NGUYÊN ngày gốc
   - `updated_at` = thời điểm Lưu (UTC ISO)
4. **Danh sách trong Admin tải từ đâu:** qua GAS đọc GitHub Contents API (`data/posts.json`) —
   luôn mới nhất, chấp nhận tốn quota API. Không fetch file JSON đã deploy.
5. **Danh mục bài viết — danh sách CỐ ĐỊNH, không quản lý qua CMS.** PHẢI khớp y hệt hằng
   `POST_CATEGORIES` trong `scripts/build.py` (`gas/` không nằm trong git nên 2 chỗ này không tự
   đồng bộ — sửa 1 bên phải sửa luôn bên kia):
   - `Cẩm nang du lịch`
   - `Kinh nghiệm đi lại`
   - `Bảng giá`
   - `Tin tức`
6. **Ảnh:** nén/resize phía client bằng `<canvas>` TRƯỚC khi upload — cạnh dài tối đa **1600px**,
   JPEG chất lượng **0.85**. Upload chạy nền, không chặn thao tác. Đẩy **thẳng lên GitHub**
   Contents API ngay khi chọn, KHÔNG qua Google Drive.
   Ảnh **RIÊNG 1-1 cho từng bài**, tên tất định theo slug:
   - ảnh bìa: `html/assets/images/blog/<slug>-cover.jpg`
   - ảnh nội dung: `html/assets/images/blog/<slug>-content-<N>.jpg` (đánh số **bất biến** — ảnh
     cũ giữ nguyên tên, ảnh mới lấy số tiếp theo)
   Vì ảnh riêng 1-1 nên xoá bài **được phép** xoá kèm ảnh (mục IV).
7. **Đường dẫn ảnh lưu trong `content_html` là đường dẫn TUYỆT ĐỐI** (`/assets/images/blog/...`)
   — toàn site dùng đường dẫn tuyệt đối, nên chuỗi đã lưu không phụ thuộc độ sâu thư mục của
   trang chi tiết (`html/blog/<slug>/index.html`, sâu 2 cấp). Build script KHÔNG viết lại `src`.

## III. Sửa bài viết

- **Slug bất biến sau lần Lưu đầu** — chặn ở CẢ hai phía:
  - server: trong `savePost`, nếu bài đã tồn tại mà slug khác → `throw`
  - client: `disabled` ô slug khi mở bài đã tồn tại; **nhớ bật lại `disabled = false`** khi mở
    form tạo mới (form dùng lại DOM, trạng thái khoá dễ dính lại từ lần sửa trước)
- Muốn đổi URL thật sự: xoá bài cũ, tạo bài mới với slug khác.
- Ảnh hiển thị lúc sửa dùng URL TUYỆT ĐỐI
  `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>` — KHÔNG dùng domain thật
  của site (có thể chưa deploy bản mới). `owner/repo/branch` lấy từ response `boot()`.

## IV. Xoá bài viết

- Xoá ĐỦ trong 1 thao tác: `data/blog/<slug>.json` + ảnh bìa + mọi ảnh nội dung
  (`<slug>-content-*`) + gỡ khỏi `data/posts.json` (ghi SAU CÙNG).
- Xoá kèm ảnh AN TOÀN vì ảnh riêng 1-1 theo slug, không có cơ chế dùng chung giữa các bài (II.6).
- Bắt buộc có modal xác nhận trước khi xoá thật — không hoàn tác được.

## V. Form công khai 1 — Liên hệ

Có **2 form liên hệ** trên site, cùng ghi vào sheet `Contacts`, cùng `formType: "contact"`:

| Trang | Field |
|---|---|
| `/` (trang chủ, `.contact-form`) | `name`, `phone`, `email`, `message` |
| `/lien-he/` | `name`, `phone`, `message` (KHÔNG có email) |

- Bắt buộc: `name` + `phone`. `email`, `message` tuỳ chọn.
- Honeypot: field ẩn tên **`_hp`** — có giá trị thì âm thầm trả `{ok:true}` và KHÔNG lưu gì
  (không "dạy" bot biết đã bị phát hiện). Rule CSS ẩn nó (`.hp-field`) nằm trong
  `html/css/style.css` — **cơ chế này hỏng thì hỏng IM LẶNG**, sau mọi lần sửa CSS phải kiểm:
  `curl -s https://taxigocongdongthap.com/css/style.css | grep -c hp-field` phải khác 0.
- Rate-limit **20 giây**/lần theo số điện thoại (`CacheService`).
- **CÓ gửi email báo** về `NOTIFY_EMAIL` (mục X), dùng template `gas/email.html` (mục VIII).
- Gọi từ site tĩnh qua `fetch()` với `Content-Type: text/plain;charset=utf-8` để né CORS
  preflight (GAS không xử lý được `OPTIONS`).

## VI. Form công khai 2 — Đặt xe

Widget "ĐẶT XE NHANH" ở trang chủ. **Chốt 17/09/2026: bổ sung Họ tên + Số điện thoại** vào
widget (trước đó chỉ có điểm đón/đến/thời gian — email báo không có cách nào gọi lại cho khách).

- Field: `name` (bắt buộc), `phone` (bắt buộc), `pickup` (điểm đón), `dropoff` (điểm đến),
  `pickup_time` (thời gian, `datetime-local`).
- `formType: "booking"`.
- Honeypot `_hp` + rate-limit **20 giây**/lần theo số điện thoại — giống mục V.
- **LockService khi ghi Sheet** (tránh 2 yêu cầu ghi đè nhau lúc cao điểm).
- **CÓ gửi email báo** về `NOTIFY_EMAIL`, template `gas/email.html`, tiêu đề phân biệt rõ với
  liên hệ.
- Giới hạn thực tế là BURST tại một thời điểm, không phải tổng/ngày. Vượt vài trăm đơn/ngày đều
  hoặc dồn cục mạnh → cân nhắc tách backend riêng.

### VI-A. Trạng thái bản ghi

- `Bookings.status`: `Mới` → `Đã xác nhận` → `Hoàn thành`, hoặc `Huỷ`.
- `Contacts.status`: `Mới` → `Đã xử lý`.
- Đổi trạng thái chỉ `admin` trở lên. Server kiểm giá trị nằm trong enum, không tin `<select>`.

## VII. UX chung trong Admin

- **2 loại pop-up RIÊNG BIỆT** — không `alert()`/`confirm()` native, không toast tự ẩn:
  1. **Xác nhận** (Huỷ / Đồng ý) — hỏi TRƯỚC khi xử lý. Dùng cho mọi thao tác xoá.
  2. **Thông báo kết quả** (1 nút Đóng) — hiện SAU khi xong, không tự ẩn.
- Mọi nút async: `disabled` + spinner trong lúc chờ, tự phục hồi trong `finally` kể cả khi lỗi.
- Sau Lưu/Xoá thành công: quay lại **danh sách của chính entity đó**, danh sách tự cập nhật ngay,
  không đợi F5.
- Sau mọi mutation thành công với tin tức: hiện thêm dòng ghi chú *"Cần khoảng 1–2 phút để website
  cập nhật xong"* (độ trễ build + deploy).
- Chuyển tab CHỈ là hiệu ứng giao diện — không tải lại trang, không gọi lại toàn bộ dữ liệu.
  Mỗi tab giữ dữ liệu lần trước trong **localStorage** (không chỉ biến bộ nhớ — biến bộ nhớ
  không sống sót qua F5), render ngay rồi mới load ngầm với cờ `silent`.
- Đăng nhập lần đầu: **1 lượt gọi `boot(token)` duy nhất** lấy hết dữ liệu cần.
- Lần vào sau: render ngay từ cache (stale-while-revalidate), rồi làm mới ngầm. Không vẽ đè khi
  người dùng đang mở form soạn/sửa.
- **Mọi key `localStorage` (TRỪ token đăng nhập) phải mang hậu tố phiên bản client**, kèm hàm tự
  dọn key khác phiên bản lúc tải script. Phiên bản này **băm ra từ chính nội dung `app.html` +
  `js.html`** (`clientBuild_()`) — KHÔNG dùng hằng số gõ tay, vì quên bump là khách kẹt vĩnh viễn
  ở giao diện cũ.
- TinyMCE chỉ `init` SAU KHI tab chứa nó đã thật sự hiện (`display:block`) — init lúc tab còn ẩn
  thì editor cao 0px và không tự đo lại.
- Mọi hàm chạy ngầm phải `console.warn`/`console.error` khi lỗi — không `.catch(() => {})`.

## VIII. Email thông báo — `gas/email.html`

- 1 template HTML dùng chung cho cả **Đặt xe** và **Liên hệ**, render bằng
  `HtmlService.createTemplateFromFile("email")`.
- **Chưa có logo** → dùng **chữ `Taxigocongdongthap.com`** làm phần nhận diện ở đầu mail, kèm
  CSS cho đẹp (màu thương hiệu `#cc1e2c`, nền trắng, bo góc, bảng thông tin 2 cột).
- CSS phải **inline/`<style>` trong `<head>`** và layout dùng `<table>` — mọi mail client
  (Gmail, Outlook, Apple Mail) đều strip CSS ngoài và hỗ trợ flex/grid rất kém.
- Gửi kèm `htmlBody` + `body` (bản text thuần fallback).
- Tiêu đề mail phân biệt rõ 2 loại:
  - `[Đặt xe] <Họ tên> - <SĐT>`
  - `[Liên hệ] <Họ tên> - <SĐT>`
- Nút CTA "Gọi lại ngay" dạng `tel:` link.
- **`NOTIFY_EMAIL` chưa cấu hình = KHÔNG gửi mail, và điều đó TUYỆT ĐỐI không được làm hỏng việc
  đã lưu bản ghi vào Sheet** — `requireCfg_` phải nằm TRONG `try`, lỗi chỉ `Logger.log`.
- ⚠️ **Quota**: dùng CHUNG tài khoản Gmail với OTP đăng nhập — **100 mail/ngày**. Chạm trần thì
  OTP không gửi được nữa. Nếu lượng đặt xe lớn dần, cân nhắc đổi kênh báo sang Telegram.

## IX. Kiến trúc lưu trữ

### Google Sheet `Taxi Go Cong CMS Data` (code tự tạo lần đầu, tự lưu `SPREADSHEET_ID`)

Tên sheet/cột dưới đây **CỐ ĐỊNH**:

- `Users` — `email`, `role`  (role ∈ `root` | `admin` | `editor`)
- `Bookings` — `id`, `created_at`, `name`, `phone`, `pickup`, `dropoff`, `pickup_time`, `status`
- `Contacts` — `id`, `created_at`, `name`, `phone`, `email`, `message`, `source`, `status`
  - `source` = `trang-chu` | `lien-he` (phân biệt 2 form ở mục V)

**KHÔNG bao giờ đẩy `Bookings`/`Contacts` lên GitHub** — dữ liệu khách hàng chỉ nằm trong Sheet.

Thêm cột mới sau này: đặt ở **CUỐI** danh sách header, code tự bổ sung header nếu sheet cũ thiếu.

### GitHub (`tranquanghuy-rightsvn/taxigocong`, branch `master`) — đường dẫn CỐ ĐỊNH

| Đường dẫn | Vai trò |
|---|---|
| `data/posts.json` | index nhẹ mọi bài — **commit CHỐT, trigger CI**, luôn ghi SAU CÙNG |
| `data/blog/<slug>.json` | nội dung đầy đủ 1 bài (có `content_html`) |
| `html/assets/images/blog/<slug>-cover.jpg` | ảnh bìa |
| `html/assets/images/blog/<slug>-content-<N>.jpg` | ảnh trong nội dung |

File build ra (`html/blog/**/index.html`) do CI ghi đè — **không sửa tay**.

### Pipeline build (repo site, KHÔNG nằm trong gas/)

| File | Vai trò |
|---|---|
| `templates/blog-post.html` | Khung trang chi tiết bài viết — **nguồn thiết kế sống, sửa tay** |
| `templates/blog-list.html` | Khung trang `/blog/` và trang chuyên mục (dùng chung) |
| `scripts/build.py` | data/ + templates/ → `html/blog/**`. Chạy TRƯỚC |
| `scripts/build-seo.py` | Sinh `<head>` cho mọi trang + `robots.txt` + `sitemap.xml`. Chạy SAU |
| `scripts/scrape-legacy-posts.py` | Sinh `data/legacy-posts.json` từ 4 bài viết tay cũ. Hiếm khi chạy |
| `scripts/make-og-images.py` | Dựng ảnh xem trước 1200×630 cho 21 trang tĩnh. Hiếm khi chạy, cần Pillow |
| `.github/workflows/build.yml` | CI: trigger ĐÚNG khi `data/posts.json` đổi |

```bash
python3 scripts/build.py && python3 scripts/build-seo.py
```

- **4 bài viết tay cũ là `legacy`**: `build.py` KHÔNG sinh lại trang chi tiết của chúng, chỉ
  liệt kê thêm ở `/blog/` và trang chuyên mục. CMS không đụng `data/legacy-posts.json`.
- **Chỉ sinh trang chuyên mục CÓ bài** — chuyên mục rỗng không đẻ ra trang trắng.
- **Dọn trang mồ côi**: xoá bài qua CMS thì `build.py` xoá luôn thư mục `html/blog/<slug>/`
  (không dọn thì trang đã xoá vẫn truy cập được và Google vẫn lập chỉ mục tiếp).
- Ảnh xem trước khi chia sẻ link: 21 trang tĩnh dùng ảnh dựng sẵn 1200×630 trong
  `html/assets/og/`; bài do CMS đăng dùng **chính ảnh bìa** người viết tải lên (không khai
  `og:image:width/height` vì không biết chắc kích thước — khai bừa là nói sai với Google).
- `html/admin/index.html` cố ý **không** nằm trong pipeline SEO (`SEO_EXCLUDED` trong
  `build-seo.py`): có `<head>` riêng, `noindex`, không vào sitemap.

### Độ trễ từ lúc Lưu tới lúc thấy trên site thật

~1–2 phút: GitHub Actions build (~30–60s) + Cloudflare deploy (~30s).

## X. Script Properties

Tên biến **CỐ ĐỊNH** sau khi đã chốt. Giá trị do người deploy tự điền trong
**Project Settings → Script Properties**, không hard-code trong code:

| Biến | Bắt buộc | Ghi chú |
|---|---|---|
| `GITHUB_TOKEN` | ✅ | PAT có quyền `contents:write` trên repo site |
| `GITHUB_OWNER` | ✅ | `tranquanghuy-rightsvn` |
| `GITHUB_REPO` | ✅ | `taxigocong` |
| `GITHUB_BRANCH` | ✅ | `master` |
| `NOTIFY_EMAIL` | ⬜ | Nơi nhận mail báo đặt xe + liên hệ. Trống = không gửi mail (không lỗi) |
| `SPREADSHEET_ID` | ⬜ | **KHÔNG tự điền** — code tự tạo Sheet lần đầu chạy và tự lưu lại |

Chỉ tự tạo Spreadsheet khi `SPREADSHEET_ID` **hoàn toàn rỗng**. Nếu đã có giá trị mà mở thất bại
(sai id / bị xoá / mất quyền) → **throw lỗi rõ ràng, KHÔNG tự tạo mới thay thế** (sẽ sinh
Spreadsheet mồ côi rỗng, khách tưởng "mất hết user").

## XI. Giấu hạ tầng khỏi mắt người dùng cuối

Không nhắc tên Sheet / Drive / Apps Script / GitHub trong BẤT KỲ chuỗi nào gửi xuống trình
duyệt — kể cả **comment** trong `app.html`/`js.html`/`index.html`/`css.html` (các file này gửi
nguyên văn xuống trình duyệt, F12 đọc được hết) và kể cả **thông báo lỗi** được `throw` từ
`Code.js`. Viết "không sửa được ở đây" / "liên hệ bên kỹ thuật".

Kiểm trước mỗi lần deploy — chỉ được phép còn ĐÚNG 1 dòng ngoại lệ đã biết dưới đây:

```bash
grep -niE 'sheet|spreadsheet|drive|apps script|github' gas/app.html gas/js.html gas/index.html gas/css.html
```

**Ngoại lệ duy nhất được chấp nhận** (`gas/js.html`, hàm `repoRawUrl_`):

```
return "https://raw.githubusercontent.com/" + REPO_INFO.owner + ...
```

Lý do giữ: ảnh VỪA tải lên chưa có trên domain thật cho tới khi CI build + deploy xong (~1–2
phút), nên trình soạn thảo bắt buộc phải xem ảnh qua URL tuyệt đối của kho lưu trữ, nếu không
người viết chèn ảnh xong sẽ thấy ảnh vỡ. Đây là ràng buộc CHỨC NĂNG, không phải sơ suất.
Đã giảm thiểu: tên biến/key trong response đổi thành trung tính (`repo`, `REPO_INFO`), không
còn chữ `github` nào ngoài chính URL. Nhắc lại ranh giới của skill: đây là che giấu ở mức giao
diện, KHÔNG phải biện pháp bảo mật — bảo mật thật nằm ở `requireRole_` phía server.

Nếu sau này muốn bỏ hẳn dòng này: phải có nơi khác phục vụ được ảnh ngay lập tức sau khi
upload (vd đẩy ảnh qua một endpoint trung gian trên chính domain), không phải chỉ đổi tên biến.

Trang `/admin/` **nhúng iframe**, không redirect — thanh địa chỉ luôn là domain của khách.

## XII. Bug đã gặp ở chính dự án này

*(cập nhật dần khi thực sự gặp — không copy từ dự án khác)*

- *(chưa có)*
