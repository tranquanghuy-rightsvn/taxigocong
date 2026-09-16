/*
 * Gợi ý địa chỉ cho ô "Điểm đón"/"Điểm đến" trong form Đặt xe nhanh, dùng
 * chung API Goong Maps autocomplete của xevipsanbay (api.xevipsanbay.com).
 *
 * QUAN TRỌNG: backend này giới hạn CORS chỉ cho phép origin
 * https://xevipsanbay.com gọi tới. Nếu taxigocong.com không nằm trong danh
 * sách origin được phép, mọi request ở đây sẽ bị trình duyệt chặn ở bước
 * preflight (lỗi CORS trong console, không phải lỗi code) — cần liên hệ bên
 * quản lý api.xevipsanbay.com để whitelist thêm domain taxigocong.com/
 * localhost khi test.
 */
(function () {
  "use strict";

  var API_BASE = "https://api.xevipsanbay.com";

  function buildQuery(params) {
    return Object.keys(params)
      .filter(function (k) {
        return params[k] !== undefined && params[k] !== null && params[k] !== "";
      })
      .map(function (k) {
        return encodeURIComponent(k) + "=" + encodeURIComponent(params[k]);
      })
      .join("&");
  }

  async function fetchAddressSuggestions(input) {
    if (!input || !input.trim()) return [];
    try {
      var qs = buildQuery({ input: input, has_deprecated_administrative_unit: true });
      var res = await fetch(API_BASE + "/v1/goong-map/autocomplete?" + qs);
      var json = await res.json();
      if (!json.success) {
        console.error("[address-autocomplete] Lỗi tìm địa chỉ:", json);
        return [];
      }
      return (json.data && json.data.predictions) || [];
    } catch (err) {
      console.error("[address-autocomplete] Không gọi được goong-map/autocomplete:", err);
      return [];
    }
  }

  function attachAddressAutocomplete(input, list) {
    if (!input || !list) return;

    var activeIndex = -1;
    var currentItems = [];
    var debounceTimer = null;
    var requestSeq = 0;

    function closeList() {
      list.hidden = true;
      list.innerHTML = "";
      activeIndex = -1;
      currentItems = [];
    }

    function renderList(items) {
      currentItems = items;
      activeIndex = -1;
      if (!items.length) {
        closeList();
        return;
      }
      list.innerHTML = items
        .map(function (item, i) {
          var fmt = item.structured_formatting || {};
          var main = fmt.main_text || item.description || "";
          var rest = fmt.secondary_text || "";
          return (
            '<li class="address-suggestion-item" data-index="' +
            i +
            '"><strong>' +
            main +
            "</strong>" +
            (rest ? ", " + rest : "") +
            "</li>"
          );
        })
        .join("");
      list.hidden = false;
    }

    function selectItem(item) {
      input.value = item.description || "";
      try {
        input.setSelectionRange(0, 0);
      } catch (err) {
        /* setSelectionRange không áp dụng cho vài loại input — bỏ qua */
      }
      input.scrollLeft = 0;
      closeList();
    }

    function setActive(index) {
      var children = list.querySelectorAll(".address-suggestion-item");
      children.forEach(function (el) {
        el.classList.remove("active");
      });
      if (index >= 0 && children[index]) {
        children[index].classList.add("active");
        children[index].scrollIntoView({ block: "nearest" });
      }
      activeIndex = index;
    }

    input.addEventListener("input", function () {
      var query = input.value;
      var seq = ++requestSeq;
      clearTimeout(debounceTimer);
      if (!query.trim()) {
        closeList();
        return;
      }
      debounceTimer = setTimeout(function () {
        fetchAddressSuggestions(query).then(function (items) {
          if (seq === requestSeq) renderList(items);
        });
      }, 250);
    });

    input.addEventListener("keydown", function (e) {
      if (list.hidden || !currentItems.length) return;
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setActive((activeIndex + 1) % currentItems.length);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        setActive((activeIndex - 1 + currentItems.length) % currentItems.length);
      } else if (e.key === "Enter") {
        if (activeIndex >= 0) {
          e.preventDefault();
          selectItem(currentItems[activeIndex]);
        }
      } else if (e.key === "Escape") {
        closeList();
      }
    });

    list.addEventListener("mousedown", function (e) {
      var item = e.target.closest(".address-suggestion-item");
      if (!item) return;
      e.preventDefault();
      var idx = Number(item.dataset.index);
      if (currentItems[idx]) selectItem(currentItems[idx]);
    });

    document.addEventListener("click", function (e) {
      if (e.target !== input && !list.contains(e.target)) closeList();
    });
  }

  function init() {
    document.querySelectorAll(".place-autocomplete-input").forEach(function (input) {
      var list = input.parentElement.querySelector(".address-suggestions");
      attachAddressAutocomplete(input, list);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
