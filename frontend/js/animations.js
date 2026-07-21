/**
 * Smart Campus — animations.js
 * Auto-initialises page animations for all dashboard pages.
 * Drop this script at the bottom of any page and it just works.
 * ================================================================
 */
(function SmartCampusAnimations() {
    'use strict';

    /* ─── helpers ─────────────────────────────────────── */

    /** Add class after a delay (ms) */
    function addClassAfter(el, cls, delay) {
        setTimeout(() => el && el.classList.add(cls), delay);
    }

    /** Stagger-add a class to a NodeList */
    function staggerClass(nodes, cls, baseDelay, step) {
        nodes.forEach((el, i) => addClassAfter(el, cls, baseDelay + i * step));
    }

    /** Create a ripple inside a button */
    function createRipple(e) {
        const btn = e.currentTarget;
        const r   = btn.getBoundingClientRect();
        const rp  = document.createElement('span');
        rp.className = 'sc-ripple';
        const size = Math.max(r.width, r.height);
        Object.assign(rp.style, {
            width:  size + 'px',
            height: size + 'px',
            left:   (e.clientX - r.left - size / 2) + 'px',
            top:    (e.clientY - r.top  - size / 2) + 'px',
        });
        btn.appendChild(rp);
        rp.addEventListener('animationend', () => rp.remove());
    }

    /** Intersection Observer for scroll-reveal */
    function makeRevealObserver() {
        return new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('sc-in');
                }
            });
        }, { threshold: 0.1 });
    }

    /* ─── Toast ──────────────────────────────────────── */
    function injectToast() {
        if (document.getElementById('sc-toast')) return;
        const el = document.createElement('div');
        el.id = 'sc-toast';
        el.setAttribute('role', 'alert');
        el.setAttribute('aria-live', 'polite');
        document.body.appendChild(el);
    }

    let _toastTimer;
    window.scToast = function(msg, type = 'success') {
        const el = document.getElementById('sc-toast');
        if (!el) return;
        clearTimeout(_toastTimer);
        el.textContent = msg;
        el.className = type + ' show';
        _toastTimer = setTimeout(() => el.classList.remove('show'), 3500);
    };

    /* ─── Count-up animation for KPI numbers ─────────── */
    function countUp(el, target, duration) {
        const start = Date.now();
        const isFloat = String(target).includes('.');
        const decimals = isFloat ? (String(target).split('.')[1] || '').length : 0;
        let suffix = '';
        if (typeof target === 'string') {
            suffix = target.replace(/[\d.]/g, '');
            target = parseFloat(target) || 0;
        }
        (function tick() {
            const elapsed  = Date.now() - start;
            const progress = Math.min(elapsed / duration, 1);
            const eased    = 1 - Math.pow(1 - progress, 3);
            const current  = eased * target;
            el.textContent = (isFloat ? current.toFixed(decimals) : Math.round(current)) + suffix;
            if (progress < 1) requestAnimationFrame(tick);
            else {
                el.textContent = target + suffix;
                el.classList.add('sc-count-flash');
                el.addEventListener('animationend', () => el.classList.remove('sc-count-flash'), { once: true });
            }
        })();
    }

    /* ─── Apply ripple to all buttons ────────────────── */
    function initButtonRipples() {
        document.querySelectorAll('button, [role="button"], a.sc-btn, .sc-btn').forEach(btn => {
            if (!btn.classList.contains('sc-btn')) btn.classList.add('sc-btn');
            if (!btn._scRipple) {
                btn.addEventListener('click', createRipple);
                btn._scRipple = true;
            }
        });
    }

    /* ─── Notification bell ──────────────────────────── */
    function initBell() {
        const bell = document.getElementById('bellNotify');
        if (!bell) return;
        bell.addEventListener('mouseenter', () => {
            const icon = bell.querySelector('span, svg, i') || bell;
            icon.classList.remove('sc-bell-ring');
            // force reflow
            void icon.offsetWidth;
            icon.classList.add('sc-bell-ring');
            icon.addEventListener('animationend', () => icon.classList.remove('sc-bell-ring'), { once: true });
        });
    }


    /* ─── Modal pop-in for any modal elements ─────────── */
    function initModals() {
        document.querySelectorAll('[id$="Modal"], [id$="-modal"], .sc-modal').forEach(modal => {
            if (modal._scModalObserved) return;
            // Watch for display change
            const obs = new MutationObserver(() => {
                const inner = modal.querySelector('.relative, .modal-inner, [role="dialog"]');
                const el = inner || modal.firstElementChild;
                if (el && !modal.classList.contains('hidden') && modal.style.display !== 'none') {
                    el.classList.add('sc-modal-anim');
                    setTimeout(() => el.classList.remove('sc-modal-anim'), 400);
                }
            });
            obs.observe(modal, { attributes: true, attributeFilter: ['class', 'style'] });
            modal._scModalObserved = true;
        });
    }

    /* ─── Scroll-reveal observer ─────────────────────── */
    function initScrollReveal() {
        const observer = makeRevealObserver();
        document.querySelectorAll('.sc-reveal, .sc-kpi, .sc-content').forEach(el => {
            observer.observe(el);
        });
    }

    /* ─── Auto-tag common selectors ──────────────────── */
    function autoTag() {
        // Topbar
        const topbar = document.querySelector('#topNavbar, nav[id*="top"], header');
        if (topbar) topbar.classList.add('sc-topbar');

        // KPI cards — elements that look like stats cards
        document.querySelectorAll('.kpi-card, [id^="kpi-"], .stat-card').forEach(el => {
            el.classList.add('sc-kpi');
            // Remove existing opacity-0 since sc-kpi handles entrance
            el.style.opacity = '';
        });

        // Content blocks
        document.querySelectorAll('.content-block, .sc-content-block, .glass-card').forEach(el => {
            if (!el.classList.contains('sc-kpi')) {
                el.classList.add('sc-content');
                el.style.opacity = '';
            }
        });

        // Table rows — mark for scroll reveal
        document.querySelectorAll('tbody tr').forEach(tr => {
            tr.classList.add('sc-table-row', 'sc-reveal');
        });
    }


    /* ─── Entrance animation sequence ───────────────── */
    function runEntrance() {
        // Topbar slides down
        const topbar = document.querySelector('.sc-topbar');
        addClassAfter(topbar, 'sc-in', 0);

        // 3. KPI cards stagger
        const kpis = document.querySelectorAll('.sc-kpi');
        staggerClass(kpis, 'sc-in', 0, 30);

        // 4. Content blocks stagger
        const contents = document.querySelectorAll('.sc-content');
        staggerClass(contents, 'sc-in', 0, 40);

        // 5. Count-up KPI numbers
        setTimeout(() => {
            document.querySelectorAll('[id^="kpi-"]').forEach(el => {
                const raw = el.textContent.trim();
                if (raw && raw !== '—' && raw !== '-') {
                    el.textContent = '0';
                    countUp(el, raw, 900);
                }
            });
        }, 450);
    }

    /* ─── MutationObserver: auto-animate dynamically added rows ── */
    function watchDOMForRows() {
        const observer = makeRevealObserver();
        const mutObs = new MutationObserver((mutations) => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType !== 1) return;
                    // Animate new table rows
                    if (node.tagName === 'TR') {
                        node.classList.add('sc-table-row', 'sc-reveal');
                        requestAnimationFrame(() => observer.observe(node));
                    }
                    node.querySelectorAll && node.querySelectorAll('tr').forEach(tr => {
                        tr.classList.add('sc-table-row', 'sc-reveal');
                        requestAnimationFrame(() => observer.observe(tr));
                    });
                    // Re-init ripples on new buttons
                    node.querySelectorAll && node.querySelectorAll('button, [role="button"]').forEach(btn => {
                        if (!btn._scRipple) {
                            btn.classList.add('sc-btn');
                            btn.addEventListener('click', createRipple);
                            btn._scRipple = true;
                        }
                    });
                });
            });
        });
        mutObs.observe(document.body, { childList: true, subtree: true });
    }







    /* ─── INIT ──────────────────────────── */
    function init() {
        injectToast();
        autoTag();
        initButtonRipples();
        initBell();
        initModals();
        initScrollReveal();
        runEntrance();
        watchDOMForRows();

    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();

