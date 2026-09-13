#!/usr/bin/env python3
"""forge-bespoke / The Groundwork Collective / scripts/render.py
Renders every page from content/data.json + per-page templates.
Single source of truth: change content/data.json to update the site.
"""
from __future__ import annotations
import json
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "content" / "data.json").read_text())


def wa_url(intent: str = "") -> str:
    base = DATA["whatsapp_base_url"]
    if not intent:
        return base
    msg = {
        "drawing_course": "Hi - I'd like to know more about the 6-month drawing course.",
        "open_studio": "Hi - I'd like to drop in for an art / music / expression session.",
        "custom": "Hi - I want to discuss a custom learning track.",
        "discovery": "Hi - I'd like to set up a discovery call.",
    }.get(intent, "Hi, I would like to know more about The Groundwork Collective.")
    return f"{base}?text={urllib.parse.quote(msg)}"


def header(active: str = "") -> str:
    nav_items = [
        ("Services", "/services.html"),
        ("Reviews", "/reviews.html"),
        ("Contact", "/contact.html"),
        ("About", "/about.html"),
    ]
    current_attr = ' aria-current="page"'
    nav_parts = []
    for label, href in nav_items:
        attr = current_attr if active == label else ""
        nav_parts.append(f'      <a href="{href}"{attr}>{label}</a>')
    nav = "\n".join(nav_parts)
    wa_discovery = wa_url("discovery")
    return ('<header class="site-header" role="banner">\n'
            '  <div class="site-header__inner">\n'
            f'    <a class="site-header__brand" href="/">{DATA["business_name"]}</a>\n'
            '    <nav class="site-nav" aria-label="Primary">\n'
            f'{nav}\n'
            '    </nav>\n'
            f'    <a class="btn btn--primary site-header__cta" href="{wa_discovery}">WhatsApp us</a>\n'
            '  </div>\n'
            '</header>')


def footer() -> str:
    return f'''<footer class="site-footer" role="contentinfo">
  <div class="site-footer__inner">
    <div class="site-footer__brand">
      <p class="site-footer__wordmark">{DATA["business_name"]}</p>
      <p class="site-footer__tagline">A studio for serious creative practice.</p>
    </div>
    <div class="site-footer__cols">
      <div class="site-footer__col">
        <p class="site-footer__col-label">Visit</p>
        <p>Shop no G-27<br>Cosmos Square, Global City<br>Virar West, {DATA["address_postal"]}<br>India</p>
        <p><a class="site-footer__link" href="{DATA["gbp_share_url"]}" target="_blank" rel="noopener">Open in Google Maps</a></p>
      </div>
      <div class="site-footer__col">
        <p class="site-footer__col-label">Studio</p>
        <p><a class="site-footer__link" href="{wa_url("discovery")}">WhatsApp us</a></p>
        <p><a class="site-footer__link" href="tel:{DATA["phone_intl"]}">{DATA["phone_display"]}</a></p>
        <p><a class="site-footer__link" href="mailto:{DATA["email"]}">{DATA["email"]}</a></p>
        <p><a class="site-footer__link" href="{DATA["instagram_url"]}" target="_blank" rel="noopener">Instagram</a></p>
      </div>
      <div class="site-footer__col">
        <p class="site-footer__col-label">Hours</p>
        <p>Confirm by WhatsApp.<br>We don't publish hours yet.</p>
        <p class="site-footer__col-mark">Made in Vasai-Vihar.</p>
      </div>
    </div>
    <div class="site-footer__legal">
      <p>© {DATA["year"]} {DATA["business_name"]}. Hand-built with care by <a href="https://forge.bruuhh.com" target="_blank" rel="noopener">Forge</a>.</p>
    </div>
  </div>
</footer>'''


def head(title: str, desc: str) -> str:
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{DATA["canonical_url"]}">
  <meta name="theme-color" content="#faf7f1">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="canonical" href="{DATA["canonical_url"]}">
  <link rel="stylesheet" href="/assets/styles.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "EducationalOrganization",
    "name": "{DATA["business_name"]}",
    "description": "{desc}",
    "url": "{DATA["canonical_url"]}",
    "telephone": "{DATA["phone_intl"]}",
    "address": {{
      "@type": "PostalAddress",
      "streetAddress": "{DATA["address_street"]}",
      "addressLocality": "{DATA["address_city"]}",
      "addressRegion": "{DATA["address_state"]}",
      "postalCode": "{DATA["address_postal"]}",
      "addressCountry": "IN"
    }},
    "sameAs": ["{DATA["instagram_url"]}"]
  }}
  </script>
</head>
<body class="theme-light">
<a class="skip-link" href="#main">Skip to content</a>
{header()}
<main id="main">'''


def close_main() -> str:
    return f'</main>\n{footer()}\n<script src="/cro/quote-builder.js" defer></script>\n<script src="/cro/sticky-cta.js" defer></script>\n<a class="sticky-cta" href="{wa_url("discovery")}" id="sticky-cta" aria-label="WhatsApp The Groundwork Collective">\n  <svg class="sticky-cta__icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>\n  <span>WhatsApp us</span>\n</a>\n</body>\n</html>\n'


def render_index() -> str:
    seed_to_path = {
        DATA["hero_photo_seed"]: "/assets/photos/hero.jpg",
    }
    for sid, seed in DATA["service_photo_seeds"].items():
        seed_to_path[seed] = f"/assets/photos/{sid}.jpg"

    def local_or_fallback(seed):
        return seed_to_path.get(seed, "/assets/monogram.svg")

    hero_photo = local_or_fallback(DATA["hero_photo_seed"])
    faq_items = [
        ("Do I need prior experience to join?", "No. We work with complete beginners through intermediate. Tell us where you are in the form above and we'll match you to a cohort."),
        ("Is there a free trial class?", "Confirm by WhatsApp. We run short intro sessions when a new cohort opens."),
        ("What if I miss a session in the 6-month track?", "Confirm by WhatsApp. We can talk you through the catch-up policy before you commit."),
        ("What's the cohort size?", "Small. 8-12 learners per cohort so each person gets real attention from the working artists who run the studio."),
        ("Do you offer payment plans?", "Confirm by WhatsApp. We do, for the 6-month track. Ask when you reach out."),
        ("Is there a refund policy?", "Confirm by WhatsApp. Yes - we put it in writing before any payment. Ask for the policy doc when you enquire."),
    ]
    faq_html = "\n".join(
        f'''        <details class="faq-item">
          <summary class="faq-item__q"><span>{q}</span><span class="faq-item__icon" aria-hidden="true">+</span></summary>
          <p class="faq-item__a">{a}</p>
        </details>''' for q, a in faq_items
    )
    return (
        head(DATA["business_name"] + "  -  " + DATA["tagline"], DATA["meta_description"])
        + f'''
  <section class="hero" aria-labelledby="hero-heading">
    <div class="hero__mesh" aria-hidden="true">
      <span class="hero__mesh-blob hero__mesh-blob--1"></span>
      <span class="hero__mesh-blob hero__mesh-blob--2"></span>
      <span class="hero__mesh-blob hero__mesh-blob--3"></span>
    </div>
    <div class="hero__grid">
      <div class="hero__copy fade-in">
        <p class="hero__eyebrow"><span class="hero__eyebrow-mark">*</span> Vasai-Vihar, Maharashtra</p>
        <h1 id="hero-heading" class="hero__heading">A studio for <em>serious</em> creative practice.</h1>
        <p class="hero__subtext">{DATA["services"][0]["description"]}</p>
        <div class="hero__ctas">
          <a class="btn btn--primary btn--fill" href="{wa_url("discovery")}">WhatsApp us</a>
          <a class="btn btn--ghost btn--underline" href="/services.html">See how we work</a>
        </div>
        <p class="hero__promise">Replies within 4 working hours. No forms, no callbacks - one WhatsApp thread.</p>
        <p class="hero__since">Est. in Vasai-Vihar, since the studio opened its doors.</p>
      </div>
      <figure class="hero__media fade-in">
        <div class="hero__media-frame">
          <img src="{hero_photo}" alt="" width="800" height="1000" loading="eager" onerror="this.onerror=null;this.src='/assets/monogram.svg';">
        </div>
        <figcaption class="hero__media-caption">
          <span class="hero__media-caption-mark">No. 01</span>
          The studio, G-27 Cosmos Square, Virar West.
        </figcaption>
      </figure>
    </div>
  </section>

  <div class="marquee" aria-hidden="true">
    <div class="marquee__track">
      <span class="marquee__item">drawing</span><span class="marquee__dot">*</span>
      <span class="marquee__item">music</span><span class="marquee__dot">*</span>
      <span class="marquee__item">expression</span><span class="marquee__dot">*</span>
      <span class="marquee__item">6-month cohort</span><span class="marquee__dot">*</span>
      <span class="marquee__item">Vasai-Vihar</span><span class="marquee__dot">*</span>
      <span class="marquee__item">studio practice</span><span class="marquee__dot">*</span>
      <span class="marquee__item">drawing</span><span class="marquee__dot">*</span>
      <span class="marquee__item">music</span><span class="marquee__dot">*</span>
      <span class="marquee__item">expression</span><span class="marquee__dot">*</span>
      <span class="marquee__item">6-month cohort</span><span class="marquee__dot">*</span>
      <span class="marquee__item">Vasai-Vihar</span><span class="marquee__dot">*</span>
      <span class="marquee__item">studio practice</span><span class="marquee__dot">*</span>
    </div>
  </div>

  <section class="trust-bar" aria-label="Studio facts">
    <div class="trust-bar__inner">
      <span class="trust-bar__item"><span class="trust-bar__dot"></span> <span class="trust-bar__label">Founded</span> by working artists</span>
      <span class="trust-bar__sep" aria-hidden="true"></span>
      <span class="trust-bar__item"><span class="trust-bar__dot"></span> <span class="trust-bar__label">Track</span> 6-month immersive</span>
      <span class="trust-bar__sep" aria-hidden="true"></span>
      <span class="trust-bar__item"><span class="trust-bar__dot"></span> <span class="trust-bar__label">Cohorts</span> 8 to 12 learners</span>
      <span class="trust-bar__sep" aria-hidden="true"></span>
      <span class="trust-bar__item"><span class="trust-bar__dot"></span> <span class="trust-bar__label">Studio</span> Virar West, 401303</span>
    </div>
  </section>

  <section class="section" aria-labelledby="cro-heading">
    <div class="container">
      <div class="cro-engine" data-engine="quote-builder">
        <h2 id="cro-heading" class="cro-engine__heading">Tell us what you want to learn.</h2>
        <p class="cro-engine__lede">Four questions. Takes a minute. We'll reply within 4 working hours with whether we're a fit.</p>
        <form class="cro-engine__form" id="quote-builder-form" novalidate>
          <div class="cro-engine__questions">
            <div class="cro-question">
              <label class="cro-question__label" for="qb-q1">What do you want to learn?</label>
              <select class="cro-question__select" id="qb-q1" name="learn" required>
                <option value="">Choose one</option>
                <option value="drawing">Drawing</option>
                <option value="visual-art">Visual art (painting, mixed media)</option>
                <option value="music">Music</option>
                <option value="expression">Personal expression / creative direction</option>
                <option value="other">Something else</option>
              </select>
            </div>
            <div class="cro-question">
              <label class="cro-question__label" for="qb-q2">Where are you now?</label>
              <select class="cro-question__select" id="qb-q2" name="level" required>
                <option value="">Choose one</option>
                <option value="beginner">Complete beginner</option>
                <option value="some-practice">Some practice</option>
                <option value="returning">Returning after a break</option>
                <option value="intermediate">Intermediate</option>
              </select>
            </div>
            <div class="cro-question">
              <label class="cro-question__label" for="qb-q3">What's your goal?</label>
              <select class="cro-question__select" id="qb-q3" name="goal" required>
                <option value="">Choose one</option>
                <option value="personal">Personal practice</option>
                <option value="portfolio">Portfolio</option>
                <option value="career">Career change</option>
                <option value="healing">Healing / expression</option>
                <option value="explore">Just exploring</option>
              </select>
            </div>
            <div class="cro-question">
              <label class="cro-question__label" for="qb-q4">When do you want to start?</label>
              <select class="cro-question__select" id="qb-q4" name="start" required>
                <option value="">Choose one</option>
                <option value="this-month">This month</option>
                <option value="3-months">Next 3 months</option>
                <option value="just-looking">Just looking</option>
              </select>
            </div>
          </div>
          <div class="cro-engine__cta-wrap">
            <button type="submit" class="btn btn--primary">WhatsApp me this scope</button>
            <button type="button" class="btn btn--ghost" id="qb-copy">Copy message instead</button>
          </div>
          <p class="cro-engine__copy-status" id="qb-copy-status" role="status" aria-live="polite" hidden>Copied. Paste it into WhatsApp.</p>
        </form>
        <ol class="cro-next" aria-label="What happens after you send">
          <li class="cro-next__step">
            <span class="cro-next__num">1</span>
            <div><strong>We read it.</strong><span>Usually within an hour during the day.</span></div>
          </li>
          <li class="cro-next__step">
            <span class="cro-next__num">2</span>
            <div><strong>We reply with availability.</strong><span>Honest fit call - if we're not right for you, we say so.</span></div>
          </li>
          <li class="cro-next__step">
            <span class="cro-next__num">3</span>
            <div><strong>You decide.</strong><span>No follow-up pressure. One thread, you control it.</span></div>
          </li>
        </ol>
      </div>
    </div>
  </section>

  <section class="section cohort-section" aria-labelledby="cohort-heading">
    <div class="container">
      <p class="cohort-eyebrow">The 6-month arc</p>
      <h2 id="cohort-heading" class="section-heading">How a cohort moves through the studio.</h2>
      <ol class="cohort-timeline">
        <li class="cohort-step">
          <span class="cohort-step__month">Month 01</span>
          <h3 class="cohort-step__title">Foundation</h3>
          <p class="cohort-step__desc">Mark-making, line weight, observing before drawing. Weekly studio sessions plus a personal practice prompt.</p>
        </li>
        <li class="cohort-step">
          <span class="cohort-step__month">Month 02</span>
          <h3 class="cohort-step__title">Seeing</h3>
          <p class="cohort-step__desc">Light, shadow, proportion. You start drawing what you actually see instead of what you think is there.</p>
        </li>
        <li class="cohort-step">
          <span class="cohort-step__month">Month 03</span>
          <h3 class="cohort-step__title">Materials</h3>
          <p class="cohort-step__desc">Charcoal, graphite, ink, conté. Finding which medium your hand wants to speak through.</p>
        </li>
        <li class="cohort-step">
          <span class="cohort-step__month">Month 04</span>
          <h3 class="cohort-step__title">Composition</h3>
          <p class="cohort-step__desc">How a drawing holds the eye. Negative space, weight, framing - the rules a working artist knows by feel.</p>
        </li>
        <li class="cohort-step">
          <span class="cohort-step__month">Month 05</span>
          <h3 class="cohort-step__title">Series</h3>
          <p class="cohort-step__desc">You start a body of work - one idea across multiple drawings. The shift from exercises to a personal voice.</p>
        </li>
        <li class="cohort-step">
          <span class="cohort-step__month">Month 06</span>
          <h3 class="cohort-step__title">Show + share</h3>
          <p class="cohort-step__desc">End-of-cohort studio showing. Family and friends invited. Optional portfolio submission for portfolio-track learners.</p>
        </li>
      </ol>
      <p class="cohort-foot">
        Looking for a different shape? <a href="{wa_url("custom")}">Tell us what you want to learn</a> - we design custom tracks around real goals.
      </p>
    </div>
  </section>

  <section class="section services-featured" aria-labelledby="services-heading">
    <div class="container">
      <p class="services-eyebrow">Three ways to work with us</p>
      <h2 id="services-heading" class="section-heading">How the work is structured.</h2>
      <ul class="services__grid services__grid--featured">
        <li class="service-card service-card--featured">
          <div class="service-card__media">
            <img class="service-card__photo" src="{local_or_fallback(DATA["service_photo_seeds"]["drawing-course"])}" alt="" loading="lazy" onerror="this.onerror=null;this.src='/assets/monogram.svg';">
            <span class="service-card__flag">Flagship</span>
          </div>
          <div class="service-card__body">
            <h3 class="service-card__title">{DATA["services"][0]["title"]}</h3>
            <p class="service-card__desc">{DATA["services"][0]["description"]}</p>
            <div class="service-card__meta">
              <span class="service-card__price">{DATA["services"][0]["pricing_label"]}</span>
              <a class="btn btn--primary btn--fill" href="{wa_url(DATA["services"][0]["whatsapp_intent"])}">WhatsApp about this</a>
            </div>
          </div>
        </li>
        <li class="service-card">
          <img class="service-card__photo" src="{local_or_fallback(DATA["service_photo_seeds"][DATA["services"][1]["id"]])}" alt="" loading="lazy" onerror="this.onerror=null;this.src='/assets/monogram.svg';">
          <h3 class="service-card__title">{DATA["services"][1]["title"]}</h3>
          <p class="service-card__desc">{DATA["services"][1]["description"]}</p>
          <div class="service-card__meta">
            <span class="service-card__price">{DATA["services"][1]["pricing_label"]}</span>
            <a class="btn btn--ghost" href="{wa_url(DATA["services"][1]["whatsapp_intent"])}">Enquire</a>
          </div>
        </li>
        <li class="service-card">
          <img class="service-card__photo" src="{local_or_fallback(DATA["service_photo_seeds"][DATA["services"][2]["id"]])}" alt="" loading="lazy" onerror="this.onerror=null;this.src='/assets/monogram.svg';">
          <h3 class="service-card__title">{DATA["services"][2]["title"]}</h3>
          <p class="service-card__desc">{DATA["services"][2]["description"]}</p>
          <div class="service-card__meta">
            <span class="service-card__price">{DATA["services"][2]["pricing_label"]}</span>
            <a class="btn btn--ghost" href="{wa_url(DATA["services"][2]["whatsapp_intent"])}">Enquire</a>
          </div>
        </li>
      </ul>
    </div>
  </section>

  <section class="section reviews-section" aria-labelledby="reviews-block-heading">
    <div class="container">
      <div class="reviews-block reviews-block--positioned">
        <div class="reviews-block__top">
          <p class="reviews-block__count">0</p>
          <div class="reviews-block__meta">
            <p class="reviews-block__stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</p>
            <p class="reviews-block__label">Google reviews so far.</p>
            <p class="reviews-block__why">If you've worked with us, your review is the most valuable thing you can leave behind.</p>
          </div>
        </div>
        <div class="reviews-block__cta">
          <a class="btn btn--primary btn--fill" href="{DATA["gbp_write_review_url"]}" target="_blank" rel="noopener">Write a Google review</a>
          <a class="btn btn--ghost btn--underline" href="{DATA["gbp_share_url"]}" target="_blank" rel="noopener">See us on Google Maps</a>
        </div>
      </div>
    </div>
  </section>

  <section class="section faq-section" aria-labelledby="faq-heading">
    <div class="container">
      <p class="faq-eyebrow">Before you WhatsApp</p>
      <h2 id="faq-heading" class="section-heading">Six questions every prospect asks.</h2>
      <div class="faq-list">
{faq_html}
      </div>
      <p class="faq-foot">
        Didn't see your question? <a href="{wa_url("discovery")}">WhatsApp us</a> - we read everything.
      </p>
    </div>
  </section>

  <section class="section" aria-labelledby="contact-block-heading">
    <div class="container">
      <h2 id="contact-block-heading" class="section-heading">Reach us.</h2>
      <div class="contact-cards">
        <a class="contact-card" href="{wa_url("discovery")}">
          <span class="contact-card__label">WhatsApp</span>
          <span class="contact-card__value">{DATA["whatsapp_display"]}</span>
          <span class="contact-card__hint">Replies in 4 working hours</span>
        </a>
        <a class="contact-card" href="tel:{DATA["phone_intl"]}">
          <span class="contact-card__label">Call</span>
          <span class="contact-card__value">{DATA["phone_display"]}</span>
          <span class="contact-card__hint">For longer enquiries</span>
        </a>
        <a class="contact-card" href="{DATA["gbp_share_url"]}" target="_blank" rel="noopener">
          <span class="contact-card__label">Directions</span>
          <span class="contact-card__value">Virar West, 401303</span>
          <span class="contact-card__hint">Open in Google Maps</span>
        </a>
      </div>
    </div>
  </section>
'''
        + close_main()
    )


def render_services() -> str:
    def local_or_fallback(seed):
        for sid, s in DATA["service_photo_seeds"].items():
            if s == seed:
                return f"/assets/photos/{sid}.jpg"
        return "/assets/monogram.svg"
    cards = "\n".join(
        f'''        <li class="service-card">
          <img class="service-card__photo" src="{local_or_fallback(DATA["service_photo_seeds"][s["id"]])}" alt="" loading="lazy" onerror="this.onerror=null;this.src='/assets/monogram.svg';">
          <h3 class="service-card__title">{s["title"]}</h3>
          <p class="service-card__desc">{s["description"]}</p>
          <div class="service-card__meta">
            <span class="service-card__price">{s["pricing_label"]}</span>
            <a class="btn btn--ghost" href="{wa_url(s["whatsapp_intent"])}">Enquire</a>
          </div>
        </li>''' for s in DATA["services"]
    )
    return (
        head("Services  -  " + DATA["business_name"], "How the work is structured at The Groundwork Collective: 6-month drawing course, open studio, custom tracks. Vasai-Vihar, Maharashtra.")
        + f'''
  <section class="page-hero">
    <div class="page-hero__inner">
      <h1 class="page-hero__heading">How the work is structured.</h1>
      <p class="page-hero__subtext">Three ways to work with us. Pricing isn't published  -  send a WhatsApp and we'll tell you what fits.</p>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <ul class="services__grid">
{cards}
      </ul>
    </div>
  </section>
'''
        + close_main()
    )


def render_reviews() -> str:
    return (
        head("Reviews  -  " + DATA["business_name"], "Reviews and testimonials for The Groundwork Collective, Virar West.")
        + f'''
  <section class="page-hero">
    <div class="page-hero__inner">
      <h1 class="page-hero__heading">Reviews.</h1>
      <p class="page-hero__subtext">We're new on Google. Be the first to write a review.</p>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <div class="reviews-block">
        <p class="reviews-block__count">0</p>
        <p class="reviews-block__label">Google reviews so far.</p>
        <p>We don't invent testimonials. When we have real ones, you'll see them here. For now, if you've worked with us, a Google review helps more than anything.</p>
        <a class="btn btn--primary" href="{DATA["gbp_write_review_url"]}" target="_blank" rel="noopener">Write a Google review</a>
      </div>
    </div>
  </section>
'''
        + close_main()
    )


def render_contact() -> str:
    return (
        head("Contact  -  " + DATA["business_name"], "Contact The Groundwork Collective, Virar West. WhatsApp, call, or visit.")
        + f'''
  <section class="page-hero">
    <div class="page-hero__inner">
      <h1 class="page-hero__heading">Reach us.</h1>
      <p class="page-hero__subtext">WhatsApp is fastest. Phone works. The studio is in Virar West  -  directions below.</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="contact-cards">
        <a class="contact-card" href="{wa_url("discovery")}">
          <span class="contact-card__label">WhatsApp</span>
          <span class="contact-card__value">{DATA["whatsapp_display"]}</span>
          <span class="contact-card__hint">Replies in 4 working hours</span>
        </a>
        <a class="contact-card" href="tel:{DATA["phone_intl"]}">
          <span class="contact-card__label">Call</span>
          <span class="contact-card__value">{DATA["phone_display"]}</span>
          <span class="contact-card__hint">For longer enquiries</span>
        </a>
        <a class="contact-card" href="mailto:{DATA["email"]}">
          <span class="contact-card__label">Email</span>
          <span class="contact-card__value">{DATA["email"]}</span>
          <span class="contact-card__hint">Async, replies within a day</span>
        </a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2 class="section-heading">Visit the studio.</h2>
      <p>{DATA["address_street"]}, {DATA["address_city"]}, {DATA["address_state"]} {DATA["address_postal"]}, India.</p>
      <div class="map">
        <iframe
          title="Map to The Groundwork Collective"
          loading="lazy"
          src="https://www.google.com/maps?q={urllib.parse.quote(DATA['address_street'] + ', ' + DATA['address_city'] + ', ' + DATA['address_state'] + ' ' + DATA['address_postal'])}&output=embed">
        </iframe>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2 class="section-heading">Hours.</h2>
      <p>Hours aren't published on our Google listing yet. WhatsApp us to confirm before you visit.</p>
      <table class="hours-table">
        <tbody>
          <tr><th>Mon</th><td>{DATA["hours_status"]}</td></tr>
          <tr><th>Tue</th><td>{DATA["hours_status"]}</td></tr>
          <tr><th>Wed</th><td>{DATA["hours_status"]}</td></tr>
          <tr><th>Thu</th><td>{DATA["hours_status"]}</td></tr>
          <tr><th>Fri</th><td>{DATA["hours_status"]}</td></tr>
          <tr><th>Sat</th><td>{DATA["hours_status"]}</td></tr>
          <tr><th>Sun</th><td>{DATA["hours_status"]}</td></tr>
        </tbody>
      </table>
    </div>
  </section>
'''
        + close_main()
    )


def render_about() -> str:
    return (
        head("About  -  " + DATA["business_name"], "About The Groundwork Collective: a studio for serious creative practice in Virar West.")
        + f'''
  <section class="page-hero">
    <div class="page-hero__inner">
      <h1 class="page-hero__heading">A studio, not a school.</h1>
      <p class="page-hero__subtext">We're working artists running a structured space for serious learners. Not a hobby shop. Not a franchise.</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <p>The Groundwork Collective is run by founders in {DATA["address_city"]}, {DATA["address_state"]}. We built it because we wanted a place for adults who want a real creative practice  -  drawing, visual art, music, expression  -  without the noise of short courses and "creative wellness" branding.</p>
      <p>Our 6-month immersive drawing course is the flagship. Cohort-based, small groups, led by working artists. If that's not what you want, tell us anyway  -  we design custom tracks for portfolio prep, creative re-direction, or specific skills.</p>
      <p>Tell us your goal. We'll tell you within 4 working hours whether we're a fit.</p>
      <div class="cro-engine__cta-wrap">
        <a class="btn btn--primary" href="{wa_url("discovery")}">WhatsApp us</a>
        <a class="btn btn--ghost" href="{DATA["instagram_url"]}" target="_blank" rel="noopener">Follow on Instagram</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2 class="section-heading">Hours.</h2>
      <p>Hours aren't published on our Google listing yet. WhatsApp us to confirm before you visit.</p>
      <table class="hours-table">
        <tbody>
          <tr><th>Mon</th><td>{DATA["hours_status"]}</td></tr>
          <tr><th>Tue</th><td>{DATA["hours_status"]}</td></tr>
          <tr><th>Wed</th><td>{DATA["hours_status"]}</td></tr>
          <tr><th>Thu</th><td>{DATA["hours_status"]}</td></tr>
          <tr><th>Fri</th><td>{DATA["hours_status"]}</td></tr>
          <tr><th>Sat</th><td>{DATA["hours_status"]}</td></tr>
          <tr><th>Sun</th><td>{DATA["hours_status"]}</td></tr>
        </tbody>
      </table>
    </div>
  </section>
'''
        + close_main()
    )


def write_all() -> None:
    pages = {
        "index.html": render_index(),
        "services.html": render_services(),
        "reviews.html": render_reviews(),
        "contact.html": render_contact(),
        "about.html": render_about(),
    }
    for name, content in pages.items():
        path = ROOT / name
        path.write_text(content, encoding="utf-8")
        print(f"wrote {path.name}: {path.stat().st_size:,} bytes")


if __name__ == "__main__":
    write_all()
    print("done")
