(function () {
  var nav = document.querySelector('.navbar');
  var toggle = document.querySelector('.nav-toggle');

  function onScroll() {
    if (!nav) return;
    if (window.scrollY > 12) nav.classList.add('is-scrolled');
    else nav.classList.remove('is-scrolled');
  }
  document.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      nav.classList.toggle('is-open');
      toggle.classList.toggle('is-open');
    });
  }

  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealEls.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('in-view');
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in-view'); });
  }

  var autoAlerts = document.querySelectorAll('.django-messages .alert');
  autoAlerts.forEach(function (el) {
    setTimeout(function () {
      el.style.transition = 'opacity .4s ease';
      el.style.opacity = '0';
      setTimeout(function () { el.remove(); }, 400);
    }, 5000);
  });

  /* ---------- Product demo tabs (click + autoplay) ---------- */
  var demoStage = document.querySelector('.demo-stage');
  var demoTabs = document.querySelectorAll('.demo-tab');
  var demoPanels = document.querySelectorAll('.demo-panel');
  var demoProgressBar = document.querySelector('.demo-progress-bar');

  if (demoStage && demoTabs.length && demoPanels.length) {
    var demoIndex = 0;
    var demoDuration = 5000;
    var demoTimer = null;
    var demoRAF = null;

    function showDemo(i) {
      demoIndex = i;
      demoTabs.forEach(function (t, idx) { t.classList.toggle('is-active', idx === i); });
      demoPanels.forEach(function (p, idx) { p.classList.toggle('is-active', idx === i); });
    }

    function stopProgress() {
      if (demoRAF) cancelAnimationFrame(demoRAF);
      if (demoProgressBar) {
        demoProgressBar.classList.remove('is-animating');
        demoProgressBar.style.width = '0%';
      }
    }

    function runProgress() {
      if (!demoProgressBar) return;
      requestAnimationFrame(function () {
        demoProgressBar.classList.add('is-animating');
        demoProgressBar.style.transitionDuration = demoDuration + 'ms';
        demoProgressBar.style.width = '100%';
      });
    }

    function stopAutoplay() {
      if (demoTimer) clearTimeout(demoTimer);
      stopProgress();
    }

    function startAutoplay() {
      stopAutoplay();
      runProgress();
      demoTimer = setTimeout(function () {
        showDemo((demoIndex + 1) % demoTabs.length);
        startAutoplay();
      }, demoDuration);
    }

    demoTabs.forEach(function (tab, idx) {
      tab.addEventListener('click', function () {
        showDemo(idx);
        startAutoplay();
      });
    });

    demoStage.addEventListener('mouseenter', stopAutoplay);
    demoStage.addEventListener('mouseleave', startAutoplay);

    showDemo(0);
    startAutoplay();
  }

  /* ---------- Stat count-up ---------- */
  var countEls = document.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window && countEls.length) {
    var countIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        countIO.unobserve(el);
        var target = parseInt(el.getAttribute('data-count'), 10) || 0;
        var suffix = el.getAttribute('data-suffix') || '';
        var duration = 1200;
        var start = null;
        function step(ts) {
          if (!start) start = ts;
          var progress = Math.min((ts - start) / duration, 1);
          var eased = 1 - Math.pow(1 - progress, 3);
          el.textContent = Math.round(eased * target) + suffix;
          if (progress < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.4 });
    countEls.forEach(function (el) { countIO.observe(el); });
  }

  /* ---------- Live activity ticker ---------- */
  var tickerWrap = document.querySelector('.ticker-text-wrap');
  if (tickerWrap) {
    var tickerItems = tickerWrap.querySelectorAll('.ticker-text');
    if (tickerItems.length > 1) {
      var tickerIndex = 0;
      setInterval(function () {
        tickerItems[tickerIndex].classList.remove('is-active');
        tickerIndex = (tickerIndex + 1) % tickerItems.length;
        tickerItems[tickerIndex].classList.add('is-active');
      }, 3200);
    }
  }

  /* ---------- Gallery lightbox ---------- */
  var lightbox = document.querySelector('.lightbox');
  if (lightbox) {
    var lightboxImg = lightbox.querySelector('img');
    var galleryTriggers = document.querySelectorAll('[data-lightbox]');
    var lightboxClose = lightbox.querySelector('.lightbox-close');

    function openLightbox(src, alt) {
      lightboxImg.src = src;
      lightboxImg.alt = alt || '';
      lightbox.classList.add('is-open');
    }
    function closeLightbox() {
      lightbox.classList.remove('is-open');
    }

    galleryTriggers.forEach(function (trigger) {
      trigger.addEventListener('click', function () {
        var img = trigger.querySelector('img');
        openLightbox(trigger.getAttribute('data-lightbox'), img ? img.alt : '');
      });
    });
    if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox) closeLightbox();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeLightbox();
    });
  }
})();
