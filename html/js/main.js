document.addEventListener('DOMContentLoaded', () => {
  console.log('Taxi Go Cong site loaded');

  const navToggle = document.querySelector('.nav-toggle');
  const mainNav = document.getElementById('main-nav');

  if (navToggle && mainNav) {
    const navOverlay = document.createElement('div');
    navOverlay.className = 'nav-overlay';
    document.body.appendChild(navOverlay);

    const navClose = document.createElement('button');
    navClose.type = 'button';
    navClose.className = 'nav-close';
    navClose.setAttribute('aria-label', 'Đóng menu');
    navClose.innerHTML = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>';
    mainNav.prepend(navClose);

    const openNav = () => {
      mainNav.classList.add('is-open');
      navOverlay.classList.add('is-open');
      document.body.classList.add('nav-open');
      navToggle.setAttribute('aria-expanded', 'true');
    };

    const closeNav = () => {
      mainNav.classList.remove('is-open');
      navOverlay.classList.remove('is-open');
      document.body.classList.remove('nav-open');
      navToggle.setAttribute('aria-expanded', 'false');
    };

    navToggle.addEventListener('click', () => {
      if (mainNav.classList.contains('is-open')) {
        closeNav();
      } else {
        openNav();
      }
    });

    navClose.addEventListener('click', closeNav);
    navOverlay.addEventListener('click', closeNav);

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeNav();
    });
  }

  document.querySelectorAll('.faq-question').forEach((button) => {
    button.addEventListener('click', () => {
      const item = button.closest('.faq-item');
      const answer = item.querySelector('.faq-answer');
      const isOpen = item.classList.contains('is-open');

      document.querySelectorAll('.faq-item.is-open').forEach((openItem) => {
        if (openItem !== item) {
          openItem.classList.remove('is-open');
          openItem.querySelector('.faq-question').setAttribute('aria-expanded', 'false');
          openItem.querySelector('.faq-answer').style.maxHeight = null;
        }
      });

      item.classList.toggle('is-open', !isOpen);
      button.setAttribute('aria-expanded', String(!isOpen));
      answer.style.maxHeight = isOpen ? null : `${answer.scrollHeight}px`;
    });
  });

  document.querySelectorAll('.nav-dropdown-toggle').forEach((toggle) => {
    toggle.addEventListener('click', (e) => {
      e.preventDefault();
      const parent = toggle.closest('.has-dropdown');
      const isOpen = parent.classList.contains('is-open');

      document.querySelectorAll('.has-dropdown.is-open').forEach((openItem) => {
        if (openItem !== parent) {
          openItem.classList.remove('is-open');
        }
      });

      parent.classList.toggle('is-open', !isOpen);
    });
  });

  document.addEventListener('click', (e) => {
    document.querySelectorAll('.has-dropdown.is-open').forEach((openItem) => {
      if (!openItem.contains(e.target)) {
        openItem.classList.remove('is-open');
      }
    });
  });

  document.querySelectorAll('.pricing-tab').forEach((tab) => {
    tab.addEventListener('click', () => {
      const target = document.getElementById(tab.dataset.target);
      if (!target) return;

      document.querySelectorAll('.pricing-tab').forEach((t) => t.classList.remove('is-active'));
      document.querySelectorAll('.pricing-panel').forEach((p) => p.classList.remove('is-active'));

      tab.classList.add('is-active');
      target.classList.add('is-active');
    });
  });

  const qbDateTime = document.getElementById('qbDateTime');
  if (qbDateTime) {
    const pad = (n) => String(n).padStart(2, '0');
    const now = new Date();
    const localNow = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}T${pad(now.getHours())}:${pad(now.getMinutes())}`;
    qbDateTime.min = localNow;
  }

  const contactForm = document.querySelector('.contact-form');

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const note = contactForm.querySelector('[data-form-note]');
      if (note) {
        note.textContent = 'Cảm ơn bạn! Chúng tôi sẽ liên hệ lại sớm nhất có thể.';
      }
      contactForm.reset();
    });
  }
});
