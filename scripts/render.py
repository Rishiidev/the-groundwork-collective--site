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
    <p class="site-footer__brand">{DATA["business_name"]}</p>
    <p class="site-footer__links">
      <a href="{wa_url("discovery")}">WhatsApp</a>
      <a href="tel:{DATA["phone_intl"]}">{DATA["phone_display"]}</a>
      <a href="mailto:{DATA["email"]}">{DATA["email"]}</a>
      <a href="{DATA["instagram_url"]}" target="_blank" rel="noopener">Instagram</a>
      <a href="{DATA["gbp_share_url"]}" target="_blank" rel="noopener">Google Maps</a>
    </p>
    <p>Shop no G-27, Cosmos Square, Global City, Virar West, Vasai-Vihar {DATA["address_postal"]}, India.</p>
    <p>© {DATA["year"]} {DATA["business_name"]}. Made with care by <a href="https://forge.bruuhh.com" target="_blank" rel="noopener">{DATA["site_built_by"]}</a>.</p>
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
    return f'</main>\n{footer()}\n<script src="/cro/quote-builder.js" defer></script>\n</body>\n</html>\n'


def render_index() -> str:
    seed_to_path = {
        DATA["hero_photo_seed"]: "/assets/photos/hero.jpg",
    }
    for sid, seed in DATA["service_photo_seeds"].items():
        seed_to_path[seed] = f"/assets/photos/{sid}.jpg"

    def local_or_fallback(seed):
        return seed_to_path.get(seed, "/assets/monogram.svg")

    hero_photo = local_or_fallback(DATA["hero_photo_seed"])
    services_html = "\n".join(
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
        head(DATA["business_name"] + "  -  " + DATA["tagline"], DATA["meta_description"])
        + f'''
  <section class="hero fade-in" aria-labelledby="hero-heading">
    <div class="hero__inner">
      <p class="hero__eyebrow">Vasai-Vihar, Maharashtra</p>
      <h1 id="hero-heading" class="hero__heading">{DATA["tagline"]}.</h1>
      <p class="hero__subtext">{DATA["services"][0]["description"]}</p>
      <div class="hero__ctas">
        <a class="btn btn--primary" href="{wa_url("discovery")}">WhatsApp us</a>
        <a class="btn btn--ghost" href="/services.html">See how we work</a>
      </div>
    </div>
    <figure class="hero__media">
      <img src="{hero_photo}" alt="" width="1280" height="720" loading="eager" onerror="this.onerror=null;this.src='/assets/monogram.svg';">
    </figure>
  </section>

  <section class="trust-bar" aria-label="Studio facts">
    <div class="trust-bar__inner">
      <span class="trust-bar__item"><span class="trust-bar__dot"></span> Founded by working artists</span>
      <span class="trust-bar__item"><span class="trust-bar__dot"></span> 6-month immersive track</span>
      <span class="trust-bar__item"><span class="trust-bar__dot"></span> Small cohorts</span>
      <span class="trust-bar__item"><span class="trust-bar__dot"></span> Studio in Virar West</span>
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
          </div>
        </form>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="services-heading">
    <div class="container">
      <h2 id="services-heading" class="section-heading">How the work is structured.</h2>
      <ul class="services__grid">
{services_html}
      </ul>
    </div>
  </section>

  <section class="section" aria-labelledby="reviews-block-heading">
    <div class="container">
      <h2 id="reviews-block-heading" class="section-heading">Reviews.</h2>
      <div class="reviews-block">
        <p class="reviews-block__count">0</p>
        <p class="reviews-block__label">Google reviews so far. Be the first to write one.</p>
        <a class="btn btn--primary" href="{DATA["gbp_write_review_url"]}" target="_blank" rel="noopener">Write a Google review</a>
      </div>
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
