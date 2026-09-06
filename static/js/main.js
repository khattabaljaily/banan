(function () {
  // Must be the first thing this script does: CSS only hides .reveal content
  // once this class is present, so content stays visible by default if this
  // script never runs at all (blocked, dropped connection, etc.).
  document.documentElement.classList.add('reveal-ready');

  var hasGSAP = typeof window.gsap !== 'undefined' && typeof window.ScrollTrigger !== 'undefined';
  if (hasGSAP) { gsap.registerPlugin(ScrollTrigger); }

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
  if (hasGSAP && revealEls.length) {
    // GSAP owns these elements' opacity/transform only for the reveal-in
    // animation — the CSS transition would otherwise fight GSAP's per-frame
    // tweening. Restore it once GSAP is done so each element's OWN hover
    // transitions (.tilt, .card, .product-card, .flip-outer, ...) still work.
    var clearTransition = function (el) { return function () { el.style.transition = ''; }; };
    revealEls.forEach(function (el) { el.style.transition = 'none'; });

    var staggerContainers = document.querySelectorAll('.bento, .products-grid, .stat-strip .container, .process-track');
    var staggeredEls = [];
    staggerContainers.forEach(function (container) {
      var items = container.querySelectorAll(':scope > .reveal');
      if (!items.length) return;
      items.forEach(function (el) { staggeredEls.push(el); });
      gsap.fromTo(items, { autoAlpha: 0, y: 28 }, {
        autoAlpha: 1, y: 0, duration: 0.7, ease: 'power3.out', stagger: 0.08,
        scrollTrigger: { trigger: container, start: 'top 88%' },
        onComplete: function () { items.forEach(function (el) { el.style.transition = ''; }); }
      });
    });

    revealEls.forEach(function (el) {
      if (staggeredEls.indexOf(el) !== -1) return;
      gsap.fromTo(el, { autoAlpha: 0, y: 28 }, {
        autoAlpha: 1, y: 0, duration: 0.7, ease: 'power3.out',
        scrollTrigger: { trigger: el, start: 'top 90%' },
        onComplete: clearTransition(el)
      });
    });
  } else if ('IntersectionObserver' in window && revealEls.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('in-view');
            io.unobserve(entry.target);
          }
        });
      },
      // threshold: 0 fires as soon as any part of the target is visible.
      // A percentage threshold (the previous 0.12) can never be satisfied
      // for a target much taller than the viewport — e.g. the long
      // website-request form — since no single scroll position ever shows
      // 12% of its total height, so it would stay invisible forever.
      { threshold: 0 }
    );
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in-view'); });
  }

  /* ---------- Hero rotating word (real service names) ---------- */
  var rotator = document.querySelector('.rotator');
  if (rotator) {
    var rotatorWords = rotator.querySelectorAll('.rotator-word');
    if (rotatorWords.length > 1) {
      var rotatorIndex = 0;
      setInterval(function () {
        rotatorWords[rotatorIndex].classList.remove('is-active');
        rotatorIndex = (rotatorIndex + 1) % rotatorWords.length;
        rotatorWords[rotatorIndex].classList.add('is-active');
      }, 2600);
    }
  }

  /* ---------- "How we work" process track ---------- */
  var processTrack = document.querySelector('.process-track');
  if (processTrack) {
    var lineFill = processTrack.querySelector('.process-line-fill');
    var processSteps = processTrack.querySelectorAll('.process-step');
    if (hasGSAP && lineFill) {
      gsap.to(lineFill, {
        scaleX: 1, ease: 'none',
        scrollTrigger: { trigger: processTrack, start: 'top 70%', end: 'bottom 60%', scrub: 0.6 }
      });
      processSteps.forEach(function (step) {
        ScrollTrigger.create({
          trigger: step, start: 'top 75%',
          onEnter: function () { step.classList.add('is-active'); }
        });
      });
    } else if ('IntersectionObserver' in window) {
      var stepIO = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-active');
            stepIO.unobserve(entry.target);
          }
        });
      }, { threshold: 0.5 });
      processSteps.forEach(function (step) { stepIO.observe(step); });
      if (lineFill) {
        var lineIO = new IntersectionObserver(function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              lineFill.style.transition = 'transform 1.2s ease-out';
              lineFill.style.transform = 'scaleX(1)';
              lineIO.unobserve(entry.target);
            }
          });
        }, { threshold: 0.3 });
        lineIO.observe(processTrack);
      }
    } else {
      processSteps.forEach(function (step) { step.classList.add('is-active'); });
      if (lineFill) lineFill.style.transform = 'scaleX(1)';
    }
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
        var target = parseFloat(el.getAttribute('data-count')) || 0;
        var suffix = el.getAttribute('data-suffix') || '';
        var decimals = parseInt(el.getAttribute('data-decimals'), 10) || 0;
        var duration = 1200;
        var start = null;
        function step(ts) {
          if (!start) start = ts;
          var progress = Math.min((ts - start) / duration, 1);
          var eased = 1 - Math.pow(1 - progress, 3);
          el.textContent = (eased * target).toFixed(decimals) + suffix;
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

  /* ---------- Aurora Grotesk: cursor, magnetics, flip-cards, carousels ---------- */
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canHover = window.matchMedia('(hover: hover)').matches;

  if (canHover && !reduceMotion) {
    var cursorDot = document.querySelector('.cursor-dot');
    var cursorRing = document.querySelector('.cursor-ring');
    if (cursorDot && cursorRing) {
      document.addEventListener('mousemove', function (e) {
        cursorDot.style.left = e.clientX + 'px';
        cursorDot.style.top = e.clientY + 'px';
        cursorRing.style.left = e.clientX + 'px';
        cursorRing.style.top = e.clientY + 'px';
      });
      document.body.classList.add('cursor-ready');

      document.addEventListener('mousemove', function (e) {
        var magnet = e.target.closest ? e.target.closest('.magnetic') : null;
        document.querySelectorAll('.magnetic').forEach(function (el) {
          if (el !== magnet) el.style.transform = '';
        });
        if (magnet) {
          var r = magnet.getBoundingClientRect();
          var x = (e.clientX - r.left - r.width / 2) * 0.3;
          var y = (e.clientY - r.top - r.height / 2) * 0.3;
          magnet.style.transform = 'translate(' + x + 'px,' + y + 'px)';
          cursorRing.classList.add('is-active');
        } else {
          cursorRing.classList.remove('is-active');
        }

        var face = e.target.closest ? e.target.closest('.flip-face') : null;
        if (face) {
          var fr = face.getBoundingClientRect();
          face.style.setProperty('--mx', ((e.clientX - fr.left) / fr.width * 100) + '%');
          face.style.setProperty('--my', ((e.clientY - fr.top) / fr.height * 100) + '%');
        }
      });

      document.documentElement.addEventListener('mouseleave', function () {
        document.querySelectorAll('.magnetic').forEach(function (el) { el.style.transform = ''; });
        cursorRing.classList.remove('is-active');
      });
    }

    var heroPreview = document.querySelector('.hero-preview');
    var codeWindow = document.querySelector('.code-window');
    if (heroPreview && codeWindow) {
      heroPreview.addEventListener('mousemove', function (e) {
        var r = heroPreview.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width - 0.5;
        var py = (e.clientY - r.top) / r.height - 0.5;
        codeWindow.style.transform = 'perspective(900px) rotateY(' + (px * 10) + 'deg) rotateX(' + (py * -10) + 'deg)';
      });
      heroPreview.addEventListener('mouseleave', function () { codeWindow.style.transform = ''; });
    }

    var auroraLayers = document.querySelectorAll('.aurora-parallax');
    if (auroraLayers.length) {
      window.addEventListener('scroll', function () {
        var y = window.scrollY;
        auroraLayers.forEach(function (el, i) {
          el.style.transform = 'translateY(' + (y * (0.08 + i * 0.05)) + 'px)';
        });
      }, { passive: true });
    }

    document.querySelectorAll('.tilt').forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5;
        var y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = 'perspective(700px) rotateY(' + (x * 8) + 'deg) rotateX(' + (y * -8) + 'deg) translateY(-3px)';
      });
      el.addEventListener('mouseleave', function () { el.style.transform = ''; });
    });
  }

  /* Flip-cards work without hover/JS-motion prefs — click is not a motion effect */
  document.querySelectorAll('.flip-outer').forEach(function (outer) {
    var card = outer.querySelector('.flip-card');
    if (!card) return;
    outer.addEventListener('click', function () {
      card.classList.toggle('is-flipped');
    });
  });

  /* ---------- "Why us" value carousel ---------- */
  var valueCard = document.querySelector('.value-carousel-card');
  var valueDots = document.querySelectorAll('.value-dots .value-dot');
  if (valueCard && valueDots.length) {
    var valueTitleEl = valueCard.querySelector('h4');
    var valueBodyEl = valueCard.querySelector('p');
    var valueIndex = 0;
    var valueTimer = null;
    function showValue(i) {
      valueIndex = (i + valueDots.length) % valueDots.length;
      var dot = valueDots[valueIndex];
      if (valueTitleEl) valueTitleEl.textContent = dot.getAttribute('data-title') || '';
      if (valueBodyEl) valueBodyEl.textContent = dot.getAttribute('data-body') || '';
      valueDots.forEach(function (d, di) { d.classList.toggle('is-active', di === valueIndex); });
    }
    function restartValueTimer() {
      if (valueTimer) clearInterval(valueTimer);
      valueTimer = setInterval(function () { showValue(valueIndex + 1); }, 4000);
    }
    valueDots.forEach(function (d, di) {
      d.addEventListener('click', function () { showValue(di); restartValueTimer(); });
    });
    restartValueTimer();
  }
})();
