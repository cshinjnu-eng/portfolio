'use strict';

// Nav scroll effect — starts transparent over dark hero
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 60);
}, { passive: true });

// Scroll reveal with IntersectionObserver
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.08, rootMargin: '0px 0px -32px 0px' });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// Stagger sibling reveals within timeline groups
document.querySelectorAll('.bt-group').forEach((group, gi) => {
  group.style.setProperty('--delay', `${gi * 40}ms`);
  group.querySelectorAll('.bt-event').forEach((ev, ei) => {
    ev.style.setProperty('--delay', `${gi * 40 + ei * 60}ms`);
  });
});

// Stagger workflow cards
document.querySelectorAll('.wfc').forEach((card, i) => {
  card.style.setProperty('--delay', `${(i % 2) * 80}ms`);
});

// Stagger research items
document.querySelectorAll('.ra-item').forEach((item, i) => {
  item.style.setProperty('--delay', `${i * 50}ms`);
});

// Stagger about statements
document.querySelectorAll('.as-item').forEach((item, i) => {
  item.style.setProperty('--delay', `${i * 70}ms`);
});
