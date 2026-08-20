/* PhaseSave — vanilla JS · 2026 refresh */
(function () {
  "use strict";

  const RM = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const canHover = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  /* ---------- Theme: dynamic theming + manual override ---------- */
  const themeToggle = document.getElementById("themeToggle");
  const applyTheme = (t) => {
    document.documentElement.setAttribute("data-theme", t);
    if (themeToggle) {
      themeToggle.setAttribute("aria-label", t === "dusk" ? "Switch to light theme" : "Switch to dark theme");
    }
  };
  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const next =
        document.documentElement.getAttribute("data-theme") === "dusk" ? "day" : "dusk";
      applyTheme(next);
      try { localStorage.setItem("ps-theme", next); } catch (e) {}
    });
  }
  // React to OS changes only when the visitor hasn't chosen explicitly.
  const sysDark = window.matchMedia("(prefers-color-scheme: dark)");
  const onSysChange = (e) => {
    let stored = null;
    try { stored = localStorage.getItem("ps-theme"); } catch (err) {}
    if (!stored) applyTheme(e.matches ? "dusk" : "day");
  };
  if (sysDark.addEventListener) sysDark.addEventListener("change", onSysChange);

  /* ---------- Light-touch personalization: returning visitors ---------- */
  try {
    const seen = localStorage.getItem("ps-seen");
    const eyebrow = document.getElementById("heroEyebrow");
    if (!seen) {
      localStorage.setItem("ps-seen", "1");
    } else if (eyebrow) {
      eyebrow.textContent = "Welcome back — clean energy, born of the desert.";
    }
  } catch (e) {}

  /* ---------- Sticky nav ---------- */
  const nav = document.getElementById("nav");
  const progress = document.getElementById("progress");
  const onScroll = () => {
    nav.classList.toggle("is-scrolled", window.scrollY > 40);
    if (progress) {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + "%";
    }
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
  if ("IntersectionObserver" in window && !RM) {
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

  /* ---------- Kinetic typography: split headline ---------- */
  const splitEls = document.querySelectorAll("[data-split]");
  splitEls.forEach((el) => {
    const words = el.textContent.trim().split(/\s+/);
    el.textContent = "";
    words.forEach((w, i) => {
      const outer = document.createElement("span");
      outer.className = "word";
      const inner = document.createElement("span");
      inner.textContent = w;
      inner.style.transitionDelay = i * 90 + "ms";
      outer.appendChild(inner);
      el.appendChild(outer);
      if (i < words.length - 1) el.appendChild(document.createTextNode(" "));
    });
    requestAnimationFrame(() => requestAnimationFrame(() => el.classList.add("is-in")));
  });

  /* ---------- Kinetic typography: rotating phrase ---------- */
  const rotators = document.querySelectorAll("[data-rotator]");
  rotators.forEach((rot) => {
    const phrases = rot.querySelectorAll(".hero__phrase");
    if (!phrases.length) return;
    if (RM) { phrases[0].classList.add("is-active"); return; }
    let idx = 0;
    phrases[0].classList.add("is-active");
    setInterval(() => {
      phrases[idx].classList.remove("is-active");
      idx = (idx + 1) % phrases.length;
      phrases[idx].classList.add("is-active");
    }, 3400);
  });

  /* ---------- Micro-interaction: hero arch tilt ---------- */
  const arch = document.getElementById("heroArch");
  if (arch && canHover && !RM) {
    let raf = null;
    arch.addEventListener("mousemove", (e) => {
      const r = arch.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - 0.5;
      const y = (e.clientY - r.top) / r.height - 0.5;
      if (raf) cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        arch.style.transform =
          "rotateY(" + (x * 8).toFixed(2) + "deg) rotateX(" + (-y * 8).toFixed(2) + "deg)";
      });
    });
    arch.addEventListener("mouseleave", () => {
      arch.style.transition = "transform 0.8s var(--ease)";
      arch.style.transform = "rotateY(0deg) rotateX(0deg)";
      setTimeout(() => (arch.style.transition = ""), 800);
    });
  }

  /* ---------- Animated counters ---------- */
  const counters = document.querySelectorAll(".count");
  const animateCount = (el) => {
    const to = parseFloat(el.dataset.to) || 0;
    const prefix = el.dataset.prefix || "";
    const suffix = el.dataset.suffix || "";
    const dur = RM ? 0 : 1600;
    const start = performance.now();
    const step = (now) => {
      const t = Math.min(1, dur ? (now - start) / dur : 1);
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
  }

  /* ---------- Savings estimator ---------- */
  const loadInput = document.getElementById("load");
  const hoursInput = document.getElementById("hours");
  const onPeakInput = document.getElementById("onPeak");
  const offPeakInput = document.getElementById("offPeak");
  const effInput = document.getElementById("eff");
  const daysInput = document.getElementById("days");

  const loadVal = document.getElementById("loadVal");
  const hoursVal = document.getElementById("hoursVal");
  const onPeakVal = document.getElementById("onPeakVal");
  const offPeakVal = document.getElementById("offPeakVal");
  const effVal = document.getElementById("effVal");
  const daysVal = document.getElementById("daysVal");

  const savings = document.getElementById("savings");
  const shiftedEnergyEl = document.getElementById("shiftedEnergy");
  const avoidedDemandEl = document.getElementById("avoidedDemand");
  const chargeEnergyEl = document.getElementById("chargeEnergy");
  const estimatorNote = document.getElementById("estimatorNote");

  // Fraction of peak-period cooling served by PhaseStore storage.
  const SHIFT = 0.7;
  const fmtUSD = (n) => "$" + Math.round(n).toLocaleString("en-US");

  const recalc = () => {
    const load = parseFloat(loadInput.value);        // kW of peak cooling load
    const hours = parseFloat(hoursInput.value);      // peak-window hours per day
    const onPeak = parseFloat(onPeakInput.value);    // $/kWh on-peak
    const offPeak = parseFloat(offPeakInput.value);  // $/kWh off-peak
    const eff = parseFloat(effInput.value) / 100;    // round-trip efficiency (0.7–1.0)
    const days = parseFloat(daysInput.value);        // operating days per year

    loadVal.textContent = load.toLocaleString("en-US") + " kW";
    hoursVal.textContent = hours + " h";
    onPeakVal.textContent = "$" + onPeak.toFixed(2) + " / kWh";
    offPeakVal.textContent = "$" + offPeak.toFixed(2) + " / kWh";
    effVal.textContent = Math.round(eff * 100) + "%";
    daysVal.textContent = days;

    // --- Energy model (per day) ---
    // Energy delivered during the peak window, before storage:
    const peakEnergy = load * hours;              // kWh/day
    // Portion of that energy now served from storage instead of the grid:
    const shiftedEnergy = peakEnergy * SHIFT;     // kWh/day
    // Energy drawn off-peak to recharge (accounts for storage losses):
    const chargeEnergy = shiftedEnergy / eff;     // kWh/day
    // On-peak grid demand removed (what the utility no longer sees):
    const avoidedDemand = load * SHIFT;           // kW

    // --- Cost model (per day) ---
    // Cost of the shifted energy if it ran on the grid during peak:
    const baselineCost = shiftedEnergy * onPeak;  // $/day
    // Cost of recharging that energy from storage off-peak:
    const storageCost = chargeEnergy * offPeak;   // $/day
    const dailySavings = baselineCost - storageCost; // $/day

    shiftedEnergyEl.textContent = Math.round(shiftedEnergy).toLocaleString("en-US");
    avoidedDemandEl.textContent = Math.round(avoidedDemand).toLocaleString("en-US");
    chargeEnergyEl.textContent = Math.round(chargeEnergy).toLocaleString("en-US");

    const assumptions =
      "Assumes " + Math.round(SHIFT * 100) + "% of peak-period cooling served by storage, " +
      Math.round(eff * 100) + "% round-trip efficiency, " + days + " operating days/yr.";

    if (dailySavings <= 0) {
      // Off-peak rate ÷ efficiency exceeds the on-peak rate → no arbitrage.
      savings.textContent = "$0 /yr";
      estimatorNote.textContent =
        "Not economical at these rates: off-peak $" + offPeak.toFixed(2) +
        " ÷ " + Math.round(eff * 100) + "% efficiency (≈ $" + (offPeak / eff).toFixed(3) +
        "/kWh delivered) meets or exceeds on-peak $" + onPeak.toFixed(2) + ". " + assumptions;
      estimatorNote.classList.add("is-warn");
    } else {
      const annualSavings = dailySavings * days;
      savings.textContent = fmtUSD(annualSavings) + " /yr";
      estimatorNote.textContent = assumptions;
      estimatorNote.classList.remove("is-warn");
    }
  };

  const estInputs = [loadInput, hoursInput, onPeakInput, offPeakInput, effInput, daysInput]
    .filter(Boolean);
  if (estInputs.length) {
    estInputs.forEach((el) => el.addEventListener("input", recalc));
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

      note.innerHTML =
        '<svg class="check" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12.5l5 5L20 6.5"/></svg>' +
        "<span>Thank you — your email client is opening. You can also call (760) 265-4209.</span>";
      note.classList.add("is-success");

      window.location.href =
        "mailto:Eugene@phasesave.com?subject=" + subject + "&body=" + body;
    });
  }
})();
