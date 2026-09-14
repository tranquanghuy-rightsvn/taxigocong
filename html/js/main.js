document.addEventListener('DOMContentLoaded', () => {
  console.log('Taxi Go Cong site loaded');

  const navToggle = document.querySelector('.nav-toggle');
  const mainNav = document.getElementById('main-nav');

  if (navToggle && mainNav) {
    navToggle.addEventListener('click', () => {
      const isOpen = mainNav.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', String(isOpen));
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
