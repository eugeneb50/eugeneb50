/* PhaseSave — vanilla JS */
(function () {
  "use strict";

  /* ---------- Sticky nav ---------- */
  const nav = document.getElementById("nav");
  const onScroll = () => {
    nav.classList.toggle("is-scrolled", window.scrollY > 40);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile drawer ---------- */
  const toggle = document.getElementById("navToggle");
  const drawer = document.getElementById("navDrawer");
  if (toggle && drawer) {
    toggle.addEventListener("click", () => {
      const open = drawer.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    drawer.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => {
        drawer.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      })
    );
  }

  /* ---------- Scroll reveal ---------- */
  const revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("is-visible");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -60px 0px" }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("is-visible"));
  }

  /* ---------- Animated counters ---------- */
  const counters = document.querySelectorAll(".count");
  const animateCount = (el) => {
    const to = parseFloat(el.dataset.to) || 0;
    const prefix = el.dataset.prefix || "";
    const suffix = el.dataset.suffix || "";
    const dur = 1600;
    const start = performance.now();
    const step = (now) => {
      const t = Math.min(1, (now - start) / dur);
      const eased = 1 - Math.pow(1 - t, 3);
      const val = Math.round(to * eased);
      el.textContent = prefix + val.toLocaleString("en-US") + suffix;
      if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  if ("IntersectionObserver" in window) {
    const cio = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            animateCount(e.target);
            cio.unobserve(e.target);
          }
        });
      },
      { threshold: 0.6 }
    );
    counters.forEach((el) => cio.observe(el));
  } else {
    counters.forEach((el) => {
      const to = parseFloat(el.dataset.to) || 0;
      el.textContent = (el.dataset.prefix || "") + to.toLocaleString("en-US") + (el.dataset.suffix || "");
    });
  }

  /* ---------- Savings estimator ---------- */
  const loadInput = document.getElementById("load");
  const hoursInput = document.getElementById("hours");
  const rateInput = document.getElementById("rate");
  const loadVal = document.getElementById("loadVal");
  const hoursVal = document.getElementById("hoursVal");
  const rateVal = document.getElementById("rateVal");
  const savings = document.getElementById("savings");
  const shifted = document.getElementById("shifted");

  const OFF_PEAK = 0.08; // $/kWh
  const SHIFT = 0.7; // fraction of load that shifts off-peak
  const fmtUSD = (n) =>
    "$" + Math.round(n).toLocaleString("en-US");

  const recalc = () => {
    const load = parseFloat(loadInput.value);
    const hours = parseFloat(hoursInput.value);
    const rate = parseFloat(rateInput.value);

    loadVal.textContent = load.toLocaleString("en-US") + " kW";
    hoursVal.textContent = hours + " h";
    rateVal.textContent = "$" + rate.toFixed(2) + " / kWh";

    const annual = load * hours * (rate - OFF_PEAK) * 365 * SHIFT;
    savings.textContent = fmtUSD(annual) + " /yr";
    shifted.textContent = Math.round(load * SHIFT).toLocaleString("en-US");
  };

  if (loadInput && hoursInput && rateInput) {
    [loadInput, hoursInput, rateInput].forEach((el) =>
      el.addEventListener("input", recalc)
    );
    recalc();
  }

  /* ---------- Contact form (static fallback → email) ---------- */
  const form = document.getElementById("contactForm");
  const note = document.getElementById("formNote");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const data = new FormData(form);
      const name = (data.get("name") || "").trim();
      const email = (data.get("email") || "").trim();
      const interest = data.get("interest") || "";
      const message = (data.get("message") || "").trim();

      if (!name || !email) {
        note.textContent = "Please add your name and email so we can reply.";
        note.classList.remove("is-success");
        return;
      }

      const subject = encodeURIComponent(
        "Consultation request — " + name + (interest ? " · " + interest : "")
      );
      const body = encodeURIComponent(
        "Name: " + name + "\nEmail: " + email +
        (interest ? "\nInterest: " + interest : "") +
        (message ? "\n\nMessage:\n" + message : "")
      );
      window.location.href =
        "mailto:Eugene@phasesave.com?subject=" + subject + "&body=" + body;

      note.textContent =
        "Thank you — your email client is opening. You can also call (760) 265-4209.";
      note.classList.add("is-success");
    });
  }
})();
