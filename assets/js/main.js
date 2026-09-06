/* EBSB — ebsb.de
   Shared behaviour for every page. No dependencies, no build step. */

/* ---------------------------------------------------------------------------
   Contact form endpoint.
   Paste the Web3Forms access key here (https://web3forms.com — free, no account
   needed; the key is public by design and is safe to commit).
   Until it is set, the form falls back to opening the visitor's mail client.
   --------------------------------------------------------------------------- */
const WEB3FORMS_KEY = "REPLACE_WITH_YOUR_WEB3FORMS_ACCESS_KEY";
const CONTACT_EMAIL = "info@ebsb.de";

document.addEventListener("DOMContentLoaded", () => {
  /* --- Mobile navigation ------------------------------------------------- */
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".main-nav");

  if (toggle && nav) {
    const setOpen = (open) => {
      nav.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", String(open));
    };

    toggle.addEventListener("click", () => {
      setOpen(!nav.classList.contains("open"));
    });

    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => setOpen(false));
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        setOpen(false);
        toggle.focus();
      }
    });

    // Reset the panel when the layout crosses back to the desktop breakpoint,
    // otherwise it stays stuck open behind the desktop nav.
    const wide = window.matchMedia("(min-width: 1001px)");
    wide.addEventListener("change", (e) => {
      if (e.matches) setOpen(false);
    });
  }

  /* --- Header shadow once the page is scrolled --------------------------- */
  const header = document.querySelector(".site-header");
  if (header) {
    const onScroll = () => header.classList.toggle("is-stuck", window.scrollY > 8);
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* --- Reveal sections as they enter the viewport ------------------------
     The .reveal elements are only hidden while <html> carries the "js" class
     (see style.css).  Dropping that class is therefore a complete escape
     hatch: everything becomes visible immediately. */
  const showEverything = () => document.documentElement.classList.remove("js");

  try {
    const revealables = document.querySelectorAll(".reveal");
    if (!revealables.length || !("IntersectionObserver" in window)) {
      showEverything();
    } else {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("visible");
              observer.unobserve(entry.target);
            }
          });
        },
        { rootMargin: "0px 0px -10% 0px", threshold: 0.08 }
      );
      revealables.forEach((el) => observer.observe(el));

      // Safety net: if the observer stalls (some headless and print contexts
      // never deliver the first callback), reveal anything that is already
      // scrolled into view. Content below the fold keeps its animation.
      const sweep = () => {
        revealables.forEach((el) => {
          if (el.classList.contains("visible")) return;
          if (el.getBoundingClientRect().top < window.innerHeight) {
            el.classList.add("visible");
          }
        });
      };
      window.addEventListener("load", () => setTimeout(sweep, 1000));
    }
  } catch (err) {
    showEverything();
  }

  /* --- Table of contents highlighting on the legal pages ----------------- */
  const toc = document.querySelector(".toc");
  if (toc && "IntersectionObserver" in window) {
    const links = [...toc.querySelectorAll("a[href^='#']")];
    const targets = links
      .map((link) => ({ link, el: document.getElementById(link.hash.slice(1)) }))
      .filter((entry) => entry.el);

    if (targets.length) {
      const spy = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            targets.forEach(({ link, el }) =>
              link.classList.toggle("active", el === entry.target)
            );
          });
        },
        { rootMargin: "-25% 0px -70% 0px" }
      );
      targets.forEach(({ el }) => spy.observe(el));
    }
  }

  /* --- Contact form ------------------------------------------------------ */
  const form = document.querySelector("#kontakt-form");
  if (form) initContactForm(form);
});

/* ---------------------------------------------------------------------------
   Contact form: German validation messages, honeypot, AJAX submit.
   Without JS the form still posts normally to Web3Forms.
   --------------------------------------------------------------------------- */
function initContactForm(form) {
  const status = form.querySelector(".form-status");
  const submit = form.querySelector("button[type='submit']");
  const submitLabel = submit ? submit.textContent : "Senden";
  const keyIsSet = WEB3FORMS_KEY && !WEB3FORMS_KEY.startsWith("REPLACE_WITH");

  const fieldOf = (input) => input.closest(".field, .field-consent");

  const validate = (input) => {
    const wrap = fieldOf(input);
    if (!wrap) return true;
    const ok = input.checkValidity();
    wrap.classList.toggle("invalid", !ok);
    return ok;
  };

  form.querySelectorAll("input, textarea").forEach((input) => {
    if (input.type === "hidden" || input.closest(".hp")) return;
    input.addEventListener("blur", () => validate(input));
    input.addEventListener("input", () => {
      const wrap = fieldOf(input);
      if (wrap && wrap.classList.contains("invalid")) validate(input);
    });
  });

  const say = (kind, html) => {
    if (!status) return;
    status.className = "form-status " + kind;
    status.innerHTML = html;
    status.hidden = false;
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Honeypot: bots fill every field they find.
    if (form.querySelector("input[name='botcheck']")?.value) return;

    const inputs = [...form.querySelectorAll("input, textarea")].filter(
      (i) => i.type !== "hidden" && !i.closest(".hp")
    );
    const allValid = inputs.map(validate).every(Boolean);
    if (!allValid) {
      say("err", "Bitte prüfen Sie die markierten Felder.");
      form.querySelector(".invalid input, .invalid textarea")?.focus();
      return;
    }

    const data = new FormData(form);

    // No key configured yet — hand off to the visitor's mail client so the
    // form is never a dead end.
    if (!keyIsSet) {
      const body =
        `Name: ${data.get("Vorname")} ${data.get("Nachname")}\n` +
        `E-Mail: ${data.get("Email")}\n\n${data.get("Nachricht")}`;
      window.location.href =
        `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent("Anfrage über ebsb.de")}` +
        `&body=${encodeURIComponent(body)}`;
      say(
        "ok",
        "<strong>Fast geschafft.</strong>Ihre E-Mail wurde in Ihrem Mailprogramm vorbereitet — " +
          "bitte dort noch absenden."
      );
      return;
    }

    if (submit) {
      submit.disabled = true;
      submit.textContent = "Wird gesendet …";
    }
    if (status) status.hidden = true;

    try {
      const res = await fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { Accept: "application/json" },
        body: data,
      });
      const out = await res.json();

      if (res.ok && out.success) {
        form.reset();
        say("ok", "<strong>Vielen Dank für ihre Anfrage!</strong>Unser Team meldet sich schnellstmöglich bei Ihnen.");
      } else {
        throw new Error(out.message || "submit failed");
      }
    } catch (err) {
      say(
        "err",
        "<strong>Das hat leider nicht geklappt.</strong>Bitte versuchen Sie es erneut oder " +
          `schreiben Sie uns direkt an <a href="mailto:${CONTACT_EMAIL}">${CONTACT_EMAIL}</a>.`
      );
    } finally {
      if (submit) {
        submit.disabled = false;
        submit.textContent = submitLabel;
      }
    }
  });
}
