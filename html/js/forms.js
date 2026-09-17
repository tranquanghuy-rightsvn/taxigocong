/**
 * Gửi form công khai (Đặt xe + Liên hệ) lên backend.
 *
 * Vì sao dùng fetch() chứ không phải submit thường: backend nằm ở domain khác, và phải trả
 * lời ngay trên trang (không điều hướng đi đâu).
 *
 * ⚠️ Content-Type BẮT BUỘC là "text/plain;charset=utf-8" — giữ request ở dạng "simple
 * request" nên trình duyệt KHÔNG gửi OPTIONS preflight trước. Backend không xử lý được
 * OPTIONS, đổi sang application/json là hỏng ngay bằng lỗi CORS.
 *
 * Kết quả báo bằng POPUP giữa màn hình, phải bấm OK mới tắt — không dùng dòng chữ nhỏ tự ẩn,
 * để khách không bỏ lỡ thông báo "đã nhận yêu cầu".
 *
 * Mỗi form đều có 1 ô bẫy bot tên "_hp" ẩn bằng CSS (.hp-field trong style.css). Người thật
 * không bao giờ thấy nên luôn để trống; bot điền tự động thì server âm thầm bỏ qua.
 */
(function () {
  'use strict';

  var ENDPOINT =
    'https://script.google.com/macros/s/AKfycbyqFeqplYsJOjrQgSMCyPs7f0MtZz_UGk8uYuMgbXUiRCfO_PEoN2M9jaQR1J3B59dq/exec';

  var ICON_SUCCESS =
    '<svg viewBox="0 0 24 24" width="32" height="32" fill="none" stroke="currentColor" ' +
    'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<path d="M20 6L9 17l-5-5"/></svg>';
  var ICON_ERROR =
    '<svg viewBox="0 0 24 24" width="32" height="32" fill="none" stroke="currentColor" ' +
    'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<path d="M12 8v5M12 17h.01"/><circle cx="12" cy="12" r="9"/></svg>';

  var overlay = null;
  var lastFocused = null;

  function buildModal() {
    if (overlay) return overlay;
    overlay = document.createElement('div');
    overlay.className = 'form-modal-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-labelledby', 'formModalTitle');
    overlay.hidden = true;
    overlay.innerHTML =
      '<div class="form-modal">' +
      '<div class="form-modal-icon"></div>' +
      '<h3 class="form-modal-title" id="formModalTitle"></h3>' +
      '<p class="form-modal-text"></p>' +
      '<button type="button" class="form-modal-ok">OK</button>' +
      '</div>';
    document.body.appendChild(overlay);

    overlay.querySelector('.form-modal-ok').addEventListener('click', closeModal);
    // Bấm ra ngoài hộp cũng đóng được, nhưng bấm BÊN TRONG hộp thì không.
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeModal();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !overlay.hidden) closeModal();
    });
    return overlay;
  }

  function showModal(type, title, text) {
    var el = buildModal();
    var box = el.querySelector('.form-modal');
    box.className = 'form-modal form-modal--' + type;
    el.querySelector('.form-modal-icon').innerHTML = type === 'success' ? ICON_SUCCESS : ICON_ERROR;
    el.querySelector('.form-modal-title').textContent = title;
    el.querySelector('.form-modal-text').textContent = text;

    lastFocused = document.activeElement;
    el.hidden = false;
    // Đọc offsetWidth ép trình duyệt vẽ trạng thái đầu trước khi thêm class -> transition chạy.
    void el.offsetWidth;
    el.classList.add('is-open');
    el.querySelector('.form-modal-ok').focus();
  }

  function closeModal() {
    if (!overlay || overlay.hidden) return;
    overlay.classList.remove('is-open');
    window.setTimeout(function () {
      overlay.hidden = true;
      // Trả con trỏ về đúng chỗ người dùng đang đứng trước khi popup mở.
      if (lastFocused && typeof lastFocused.focus === 'function') lastFocused.focus();
    }, 180);
  }

  /** Số điện thoại VN: 0xxxxxxxxx hoặc +84xxxxxxxxx, cho phép khoảng trắng/chấm/gạch ngang. */
  function isValidPhone(raw) {
    var d = String(raw || '').replace(/[^\d+]/g, '');
    return /^(0\d{9}|\+84\d{9}|84\d{9})$/.test(d);
  }

  function val(form, name) {
    var el = form.querySelector('[name="' + name + '"]');
    return el ? String(el.value || '').trim() : '';
  }

  function send(payload) {
    return fetch(ENDPOINT, {
      method: 'POST',
      // Không đổi thành application/json — xem ghi chú đầu file.
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(payload),
    })
      .then(function (res) {
        return res.json();
      })
      .catch(function () {
        // Lỗi mạng / backend chưa sẵn sàng — không để form "im lặng không phản hồi".
        return { ok: false, error: 'Không gửi được, quý khách vui lòng gọi hotline 0386 263 287 giúp em.' };
      });
  }

  /**
   * @param {HTMLFormElement} form
   * @param {Function} collect  trả về {payload} hoặc {error} nếu dữ liệu chưa hợp lệ
   * @param {string} successTitle
   * @param {string} successText
   */
  function wire(form, collect, successTitle, successText) {
    if (!form) return;
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var submitBtn = form.querySelector('[type="submit"]');
      var collected = collect(form);
      if (collected.error) {
        showModal('error', 'Thiếu thông tin', collected.error);
        return;
      }

      // Chặn bấm lại nhiều lần trong lúc chờ (~1-2s) — tránh tạo bản ghi trùng.
      if (submitBtn) submitBtn.disabled = true;

      send(collected.payload)
        .then(function (res) {
          if (res && res.ok) {
            form.reset();
            showModal('success', successTitle, successText);
          } else {
            showModal('error', 'Gửi không thành công', (res && res.error) || 'Có lỗi xảy ra, quý khách vui lòng thử lại.');
          }
        })
        .finally(function () {
          // finally: nút luôn được bật lại kể cả khi lỗi giữa chừng.
          if (submitBtn) submitBtn.disabled = false;
        });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    // ---------- Đặt xe (widget trang chủ) ----------
    wire(
      document.getElementById('quickBookForm'),
      function (form) {
        var name = val(form, 'name');
        var phone = val(form, 'phone');
        if (!name) return { error: 'Quý khách vui lòng nhập họ tên để tổng đài gọi lại xác nhận.' };
        if (!isValidPhone(phone)) return { error: 'Số điện thoại chưa đúng, quý khách vui lòng kiểm tra lại.' };

        // 2 ô địa chỉ dùng chung class (có gợi ý địa chỉ), không có name riêng — lấy theo
        // thứ tự xuất hiện: [0] điểm đón, [1] điểm đến.
        var places = form.querySelectorAll('.place-autocomplete-input');
        var timeEl = form.querySelector('#qbDateTime');
        return {
          payload: {
            formType: 'booking',
            name: name,
            phone: phone,
            pickup: places[0] ? String(places[0].value || '').trim() : '',
            dropoff: places[1] ? String(places[1].value || '').trim() : '',
            pickup_time: timeEl ? String(timeEl.value || '').trim() : '',
            _hp: val(form, '_hp'),
          },
        };
      },
      'Đã nhận yêu cầu đặt xe!',
      'Tổng đài Taxi Gò Công sẽ gọi lại xác nhận chuyến đi trong ít phút. Cảm ơn quý khách!'
    );

    // ---------- Liên hệ (trang chủ + /lien-he/) ----------
    // 2 form khác nhau về field (trang chủ có thêm ô email) nhưng cùng 1 luồng xử lý; phân
    // biệt nguồn bằng data-source trên thẻ <form>.
    Array.prototype.forEach.call(
      document.querySelectorAll('form.contact-form[data-source]'),
      function (form) {
        wire(
          form,
          function (f) {
            var name = val(f, 'name');
            var phone = val(f, 'phone');
            if (!name) return { error: 'Quý khách vui lòng nhập họ và tên.' };
            if (!isValidPhone(phone)) return { error: 'Số điện thoại chưa đúng, quý khách vui lòng kiểm tra lại.' };
            return {
              payload: {
                formType: 'contact',
                name: name,
                phone: phone,
                email: val(f, 'email'),
                message: val(f, 'message'),
                source: f.getAttribute('data-source') || 'lien-he',
                _hp: val(f, '_hp'),
              },
            };
          },
          'Đã gửi liên hệ!',
          'Cảm ơn quý khách đã liên hệ. Chúng tôi sẽ phản hồi trong thời gian sớm nhất.'
        );
      }
    );
  });
})();
