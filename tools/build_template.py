#!/usr/bin/env python3
"""Build the Elementor template (and an approximate static preview) for the
Personal Fitness Trainer design.

    python3 tools/build_template.py

Outputs:
    elementor/personal-fitness-trainer.json  -> import in WordPress (Templates > Import)
    preview/index.html                       -> static approximation, for a quick look

Only free Elementor widgets are used (Heading, Text Editor, Button, Image,
Icon, Icon List, Toggle, HTML) with Flexbox Containers (Elementor >= 3.16).
Visual styling lives in elementor/custom.css, which is embedded in the
template through an HTML widget.
"""
import hashlib
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_RAW = ("https://raw.githubusercontent.com/mariemmejri23-create/"
            "Personal-fitness-ytainer/claude/wordpress-elementor-design-4l07jm/assets/images/")
BOXED = 1120

_counter = [0]


def uid():
    _counter[0] += 1
    return hashlib.md5(f"pft-{_counter[0]}".encode()).hexdigest()[:7]


def img(name):
    return {"url": REPO_RAW + name, "id": "", "alt": "", "source": "library", "_local": name}


def icon(value, library="fa-solid"):
    return {"value": value, "library": library}


def px(size, unit="px"):
    return {"unit": unit, "size": size, "sizes": []}


def box(t, r, b, l, unit="px"):
    return {"unit": unit, "top": str(t), "right": str(r), "bottom": str(b), "left": str(l), "isLinked": False}


def gapv(g):
    return {"unit": "px", "size": g, "column": str(g), "row": str(g), "isLinked": True}


# ---------------------------------------------------------------- elements
def con(children, cls="", top=False, direction="column", gap=0, width=None, pad=(0, 0, 0, 0),
        align=None, justify=None, wrap=None, min_h=None, bg=None, bg_image=None, overlay=False,
        anchor=None, grow=False, tablet=None, mobile=None, link=None, boxed=BOXED):
    s = {
        "flex_direction": direction,
        "flex_gap": gapv(gap),
        "padding": box(*pad),
    }
    if top:
        s["content_width"] = "boxed"
        s["boxed_width"] = px(boxed)
        cls = ("pft-section " + cls).strip()
    else:
        s["content_width"] = "full"
    if width is not None:
        # numbers are percentages, "278px" strings are fixed widths
        s["width"] = px(int(width[:-2])) if isinstance(width, str) else px(width, "%")
    if align:
        s["flex_align_items"] = align
    if justify:
        s["flex_justify_content"] = justify
    if wrap:
        s["flex_wrap"] = wrap
    if min_h:
        s["min_height"] = px(min_h)
    if bg:
        s["background_background"] = "classic"
        s["background_color"] = bg
    if bg_image:
        s["background_background"] = "classic"
        s["background_image"] = bg_image
        s["background_position"] = "center center"
        s["background_size"] = "cover"
        s["background_repeat"] = "no-repeat"
    if overlay:
        s.update({
            "background_overlay_background": "gradient",
            "background_overlay_color": "rgba(0,0,0,0)",
            "background_overlay_color_stop": px(45, "%"),
            "background_overlay_color_b": "rgba(0,0,0,0.78)",
            "background_overlay_color_b_stop": px(100, "%"),
            "background_overlay_gradient_type": "linear",
            "background_overlay_gradient_angle": px(180, "deg"),
        })
    if grow:
        s["_flex_size"] = "grow"
    if anchor:
        s["_element_id"] = anchor
    if link:
        s["html_tag"] = "a"
        s["link"] = {"url": link, "is_external": "", "nofollow": ""}
    for device, opts in (("tablet", tablet), ("mobile", mobile)):
        for k, v in (opts or {}).items():
            key = {"direction": "flex_direction", "width": "width", "pad": "padding", "gap": "flex_gap",
                   "align": "flex_align_items", "justify": "flex_justify_content", "min_h": "min_height",
                   "wrap": "flex_wrap"}[k]
            if k == "pad":
                v = box(*v)
            elif k == "gap":
                v = gapv(v)
            elif k == "width":
                v = px(v, "%")
            elif k == "min_h":
                v = px(v)
            s[f"{key}_{device}"] = v
    if cls:
        s["css_classes"] = cls
    return {"id": uid(), "elType": "container", "isInner": not top, "settings": s, "elements": children}


def widget(kind, cls="", grow=False, **settings):
    if cls:
        settings["_css_classes"] = cls
    if grow:
        settings["_flex_size"] = "grow"
    return {"id": uid(), "elType": "widget", "widgetType": kind, "settings": settings, "elements": []}


def heading(title, cls="", tag="h2", align=None):
    s = {"title": title, "header_size": tag}
    if align:
        s["align"] = align
    return widget("heading", cls, **s)


def text(htm, cls="", align=None, grow=False):
    s = {"editor": htm}
    if align:
        s["align"] = align
    return widget("text-editor", cls, grow=grow, **s)


def button(label, url, cls="pft-btn", align=None):
    s = {"text": label, "link": {"url": url, "is_external": "", "nofollow": ""},
         "selected_icon": icon("fas fa-arrow-right"), "icon_align": "right", "size": "sm"}
    if align:
        s["align"] = align
    return widget("button", cls, **s)


def arrow(url):
    return widget("button", "pft-arrow", text="", link={"url": url, "is_external": "", "nofollow": ""},
                  selected_icon=icon("fas fa-arrow-right"), icon_align="right", size="sm")


def image(name, cls="", align=None, alt=""):
    s = {"image": img(name), "image_size": "full"}
    s["image"]["alt"] = alt
    if align:
        s["align"] = align
    return widget("image", cls, **s)


def ico(value, cls="", library="fa-solid"):
    return widget("icon", cls, selected_icon=icon(value, library), align="left")


def icon_list(items, cls="", ic="fas fa-check", inline=False):
    s = {"icon_list": [{"_id": uid(), "text": t, "selected_icon": icon(i or ic)}
                       for t, i in [(x, None) if isinstance(x, str) else x for x in items]],
         "view": "traditional"}
    if inline:
        s["view"] = "inline"
    return widget("icon-list", cls, **s)


def html_w(code, cls=""):
    return widget("html", cls, html=code)


def toggle(items, cls=""):
    return widget("toggle", cls,
                  tabs=[{"_id": uid(), "tab_title": q, "tab_content": f"<p>{a}</p>"} for q, a in items],
                  selected_icon=icon("fas fa-plus"), selected_active_icon=icon("fas fa-minus"),
                  icon_align="right", title_html_tag="div")


# ---------------------------------------------------------------- content
ORANGE = "#f9652f"
SECTION_PAD = (96, 0, 96, 0)
T_PAD = (72, 24, 72, 24)
M_PAD = (56, 20, 56, 20)
STACK_T = {"direction": "column", "pad": T_PAD, "gap": 48}
STACK_M = {"direction": "column", "pad": M_PAD, "gap": 40}
FULL = {"width": 100}

with open(os.path.join(ROOT, "elementor", "custom.css")) as f:
    CSS = f.read()

styles = con([html_w("<style>\n" + CSS + "\n</style>")], cls="pft-section pft-styles", top=False)
styles["isInner"] = False
styles["settings"]["content_width"] = "full"

# 1. HERO --------------------------------------------------------------------
hero = con([
    con([
        icon_list([("30-Day Money-Back Guarantee", "fas fa-shield-alt")], cls="pft-badge", inline=True),
        con([
            image("hero-avatars.jpg", cls="pft-trust-avatars", alt="Happy clients"),
            text('<p>Trusted by 2,000+ clients worldwide</p><p><span class="pft-star">&#9733;</span> Rated 4.9 out of 5.0</p>',
                 cls="pft-trust-text"),
        ], direction="row", gap=10, align="center"),
        heading("Because your best self<br>isn&rsquo;t behind you, it&rsquo;s ahead", cls="pft-h1", tag="h1"),
    ], gap=24, width=62, align="flex-start", tablet=FULL, mobile=FULL),
    con([
        con([
            ico("far fa-calendar", library="fa-regular"),
            con([
                text("<p>30-min session<br>Book your call</p>", grow=True),
                arrow("#contact"),
            ], direction="row", gap=12, align="center", justify="space-between"),
        ], cls="pft-hero-card", gap=14, pad=(16, 16, 16, 16)),
        text("<p>No pressure. Just a clear path forward.</p>", cls="pft-hero-note"),
    ], gap=12, width="278px", mobile=FULL),
], cls="pft-hero", top=True, direction="row", align="flex-end", justify="space-between", wrap="wrap",
    min_h=900, pad=(160, 0, 40, 0), bg_image=img("hero-bg.jpg"), overlay=True, anchor="top",
    tablet={"direction": "column", "align": "flex-start", "justify": "flex-end", "pad": (160, 24, 40, 24), "gap": 32,
            "min_h": 820},
    mobile={"pad": (140, 20, 32, 20), "min_h": 720})
hero["settings"]["flex_gap"] = gapv(24)

# 2. STATS -------------------------------------------------------------------
stats_data = [
    ("+250", "Women Coached", "From postpartum recovery to full transformations"),
    ("98%", "Consistency Rate", "Clients report staying on track week after week"),
    ("5", "Average Feedback", "Based on client satisfaction and progress surveys"),
    ("3x", "Faster Progress", "From postpartum recovery to full transformations"),
]
stats = con([
    con([
        heading(n, cls="pft-stat-number", tag="div"),
        heading(t, cls="pft-stat-title", tag="h3"),
        text(f"<p>{d}</p>", cls="pft-muted"),
    ], gap=8, width=23, tablet={"width": 46}, mobile={"width": 100})
    for n, t, d in stats_data
], cls="pft-stats", top=True, direction="row", gap=24, wrap="wrap", justify="space-between",
    pad=(96, 0, 96, 0), boxed=1048, tablet={"pad": (72, 24, 72, 24), "gap": 40}, mobile={"pad": M_PAD, "gap": 32})

# 3. TESTIMONIAL ------------------------------------------------------------
testimonial = con([
    heading("&#9733;&#9733;&#9733;&#9733;&#9733;", cls="pft-stars", tag="div"),
    heading("&ldquo;After two kids, I never thought I&rsquo;d feel this strong again. Rachel Stone helped me "
            "rebuild my body and confidence.&rdquo;", cls="pft-quote", tag="blockquote"),
    con([
        image("avatar-sara.jpg", cls="pft-avatar", alt="Sara Chen"),
        con([
            heading("Sara Chen", cls="pft-author-name", tag="div"),
            text("<p>Postnatal Reboot - November 2025</p>", cls="pft-muted"),
        ], gap=2, grow=True),
    ], direction="row", gap=16, align="center"),
], cls="pft-testimonial", top=True, gap=18, pad=(96, 0, 96, 0), boxed=808,
    tablet={"pad": T_PAD}, mobile={"pad": M_PAD})

# 4. ABOUT -------------------------------------------------------------------
values = [("fas fa-fire-alt", "Strength Over<br>Comparison"), ("fas fa-bolt", "Balance Over<br>Extremes"),
          ("fas fa-crown", "Habits Over<br>Quick Fixes")]
about = con([
    con([], cls="pft-about-media", width=53.6, min_h=795, bg_image=img("coach-rachel.jpg"),
        tablet={"width": 100, "min_h": 620}, mobile={"width": 100, "min_h": 440}),
    con([
        con([
            heading("Meet your coach", cls="pft-label", tag="div"),
            heading("Hi, I&rsquo;m Rachel Stone", cls="pft-h2", tag="h2"),
            text("<p>For years, I thought strength meant doing more &mdash; training harder, eating cleaner, sleeping "
                 "less. I pushed through exhaustion, believing discipline would bring freedom. It didn&rsquo;t.</p>"
                 "<p>When burnout finally forced me to slow down, I started listening. I studied how movement, "
                 "hormones, rest, and mindset work together &mdash; and rebuilt my strength through awareness, not "
                 "pressure.</p>"
                 "<p>Now I help women do the same: feel capable and confident again without sacrificing themselves "
                 "to get there. My approach blends science and empathy &mdash; habit-based, psychology-first, and "
                 "built for lasting balance</p>"),
            image("signature.png", cls="pft-signature", align="right", alt="Rachel Stone signature"),
        ], gap=16),
        con([
            heading("My Philosophy", cls="pft-h3", tag="h3"),
            con([
                con([ico(i), text(f"<p>{t}</p>")], cls="pft-value", gap=10, pad=(16, 16, 16, 16), grow=True,
                    mobile={"width": 100})
                for i, t in values
            ], direction="row", gap=16, mobile={"direction": "column", "gap": 12}),
        ], gap=24),
    ], width=42.9, justify="space-between", gap=48, tablet=FULL, mobile=FULL),
], cls="pft-about", anchor="about", top=True, direction="row", gap=40, justify="space-between",
    pad=(96, 0, 64, 0), tablet=STACK_T, mobile=STACK_M)

logos = con([
    image(n, alt=a) for n, a in (("logo-issa.png", "ISSA"), ("logo-nasm.png", "NASM"),
                                  ("logo-ace.png", "ACE"), ("logo-afaa.png", "AFAA"))
], cls="pft-logos", top=True, direction="row", gap=120, justify="center", align="center", wrap="wrap",
    pad=(0, 0, 130, 0), tablet={"gap": 64, "pad": (0, 24, 96, 24)}, mobile={"gap": 32, "pad": (0, 20, 72, 20)})

# 5. SERVICES (dark) -----------------------------------------------------------
def svc_card(ic, title, desc, extra_top=None, **kw):
    top_w = extra_top or ico(ic)
    return con([top_w, con([heading(title, cls="pft-h3", tag="h3"),
                            text(f"<p>{desc}</p>", cls="pft-card-text")], gap=6)],
               cls="pft-card", justify="space-between", gap=24, pad=(24, 24, 24, 24), **kw)


services = con([
    con([
        heading("Services", cls="pft-label", tag="div"),
        heading("Choose the support<br>that fits your life", cls="pft-h2", tag="h2"),
        text("<p>Flexible options to fit every budget and lifestyle, all packages includes nutrition guidance and "
             "on-going weekly support</p>", cls="pft-intro"),
        button("Get Started with Rachel", "#programs"),
    ], cls="pft-services-intro", width=40, gap=16, justify="center", align="flex-start", tablet=FULL, mobile=FULL),
    con([
        con([
            svc_card(None, "In-Person Training",
                     "Train face-to-face with personalized coaching and real-time feedback.",
                     extra_top=heading("NYC", cls="pft-city", tag="div"), width=48.7, min_h=362,
                     mobile={"width": 100, "min_h": 280}),
            con([
                svc_card("fas fa-video", "Online Coaching",
                         "Flexible sessions from anywhere &mdash; your program, your schedule.", grow=True),
                svc_card("fas fa-tasks", "Nutrition plans",
                         "Tailored guidance to support your training and daily routine.", grow=True),
            ], gap=14, width=48.7, mobile={"width": 100}),
        ], direction="row", gap=14, justify="space-between", mobile={"direction": "column"}),
        con([
            con([
                ico("fas fa-user-friends"),
                con([heading("Business or Group Training", cls="pft-h3", tag="h3"),
                     text("<p>Designed for teams or partners who want shared motivation and accountability.</p>",
                          cls="pft-card-text")], gap=6),
            ], justify="space-between", gap=24, grow=True, width=50, mobile={"width": 100}),
            con([image("service-group.jpg", cls="pft-card-img", alt="Group training")], width=45.9,
                mobile={"width": 100}),
        ], cls="pft-card", direction="row", gap=24, pad=(24, 24, 24, 24), min_h=415,
            mobile={"direction": "column"}),
    ], width=48.2, gap=14, tablet=FULL, mobile=FULL),
], cls="pft-services", anchor="services", top=True, direction="row", justify="space-between", align="center",
    gap=40, bg="#121212", pad=(124, 0, 124, 0), tablet=STACK_T, mobile=STACK_M)

# 6. PROCESS -----------------------------------------------------------------
steps = [
    ("01", "Discovery call", "We&rsquo;ll explore your goals, challenges, and lifestyle to create the right approach."),
    ("02", "Personalized Plan", "Training and nutrition tailored to your lifestyle &mdash; realistic, flexible, and sustainable."),
    ("03", "Weekly Coaching", "Weekly check-ins, form reviews and adjustments so you always know your next step."),
    ("04", "Lifestyle Integration", "We adapt your plan as your schedule, cycle, and needs shift"),
    ("05", "Long-Term Balance", "Progress doesn&rsquo;t end here &mdash; we&rsquo;ll refine, celebrate, and keep building together"),
]
process = con([
    con([
        con([
            heading("How it works", cls="pft-label", tag="div"),
            heading("Your path to<br>lasting results", cls="pft-h2", tag="h2"),
            text("<p>Every transformation starts with structure. Here&rsquo;s how we turn goals into real progress "
                 "&mdash; one step at a time.</p>"),
            button("Book Your Free Call", "#contact"),
        ], gap=16, align="flex-start"),
        image("process.jpg", cls="pft-img", alt="Coaching session"),
    ], width=48.2, gap=24, tablet=FULL, mobile=FULL),
    con([
        con([
            heading(n, cls="pft-step-num", tag="div"),
            heading(t, cls="pft-step-title", tag="h3"),
            text(f"<p>{d}</p>", cls="pft-muted"),
        ], gap=6)
        for n, t, d in steps
    ], width=48.2, gap=40, pad=(0, 0, 0, 0), tablet=FULL, mobile={"width": 100, "gap": 32}),
], cls="pft-process", anchor="how-it-works", top=True, direction="row", justify="space-between", gap=40,
    pad=SECTION_PAD, tablet=STACK_T, mobile=STACK_M)

# 7. PROGRAMS ----------------------------------------------------------------
programs_data = [
    (False, "12-Week Transformation", "$249",
     "Step-by-step coaching to rebuild strength, improve energy, and see real, lasting results.",
     ["Personalized workouts", "Weekly Progress tracking", "Nutrition fundamentals", "Chat &amp; email support"]),
    (True, "Postnatal Reboot", "$329",
     "Gentle, structured recovery for new mothers to help them get confidence and balance again.",
     ["Tailored postpartum training plan", "Nutrition &amp; recovery coaching", "Weekly 1-on-1 check-ins",
      "Ongoing support between sessions"]),
    (False, "Tone with Hormone Balance", "$449",
     "Workouts + nutrition designed around your cycle, energy, and hormonal needs",
     ["Custom periodized training cycles", "Ready made cooked meals", "Bi-weekly performance reviews",
      "Priority messaging access"]),
]


def price_card(featured, title, price, desc, items):
    kids = [ico("fas fa-chart-bar", cls="pft-price-icon")]
    if featured:
        kids.append(heading("Most Popular", cls="pft-popular", tag="div"))
    kids += [
        con([
            heading(title, cls="pft-h3", tag="h3"),
            heading(f"{price}<span>/month</span>", cls="pft-price", tag="div"),
            text(f"<p>{desc}</p>", cls="pft-price-desc"),
        ], gap=12),
        con([heading("What&rsquo;s included", cls="pft-included", tag="div"),
             icon_list(items, cls="pft-checks")], gap=8),
        button("Join the Program", "#contact", cls="pft-btn pft-btn--outline pft-btn--block"),
    ]
    return con(kids, cls="pft-price-card" + (" pft-price-card--featured" if featured else ""),
               gap=24, pad=(20, 20, 20, 20), grow=True, width=31.8,
               tablet={"width": 100}, mobile={"width": 100})


programs = con([
    con([
        heading("For you", cls="pft-label", tag="div", align="center"),
        heading("Signature Programs!", cls="pft-h2", tag="h2", align="center"),
        text("<p>Choose the program that fits your goals, lifestyle, and pace. Every plan includes personalized "
             "workouts, nutrition guidance, and weekly support.</p>", align="center"),
    ], gap=12, align="center", pad=(0, 280, 0, 280), tablet={"pad": (0, 40, 0, 40)}, mobile={"pad": (0, 0, 0, 0)}),
    con([price_card(*p) for p in programs_data], direction="row", gap=24, align="stretch",
        tablet={"direction": "column"}, mobile={"direction": "column"}),
], cls="pft-programs", anchor="programs", top=True, gap=40, pad=SECTION_PAD, tablet={"pad": T_PAD},
    mobile={"pad": M_PAD})

# 8. RESULTS -----------------------------------------------------------------
results = con([
    con([
        con([
            heading("Results", cls="pft-label", tag="div"),
            heading("Progress you can see", cls="pft-h2", tag="h2"),
            text("<p>Every transformation tells a story. These programs are built to help you move better, feel "
                 "stronger, and see steady progress, without extremes, burnout, or quick fixes.</p>"),
        ], gap=12),
        con([
            image("avatar-sophie.jpg", cls="pft-avatar pft-avatar--lg", alt="Sophie Lammers"),
            con([heading("Sophie Lammers", cls="pft-author-name", tag="div"),
                 text("<p>12-Week Transformation Program</p>", cls="pft-muted")], gap=2),
            heading("&#9733;&#9733;&#9733;&#9733;&#9733;", cls="pft-stars", tag="div"),
            text("<p>&ldquo;I used to feel drained and frustrated no matter how much I tried. Rachel helped me "
                 "reconnect with my body and rebuild strength without burnout. For the first time, I actually enjoy "
                 "moving again &mdash; and the changes haven&rsquo;t just been physical, they&rsquo;ve been mental "
                 "too.&rdquo;</p>"),
        ], gap=12),
    ], width=45, gap=56, justify="center", tablet=FULL, mobile=FULL),
    con([image("before-after.jpg", cls="pft-img", alt="Before and after")], width=48.6, tablet=FULL, mobile=FULL),
], cls="pft-results", anchor="results", top=True, direction="row", justify="space-between", align="center",
    gap=40, pad=SECTION_PAD, tablet=STACK_T, mobile=STACK_M)

# 9. FAQ ---------------------------------------------------------------------
faq_items = [
    ("What should I expect during my first session?",
     "We start with a relaxed conversation about your goals, history and schedule, followed by a short movement "
     "assessment. You leave with clear first steps &mdash; no pressure, no judgement."),
    ("Do I need a gym membership?",
     "No. Programs can be built for a gym, a home setup with minimal equipment, or a mix of both."),
    ("How often should I train each week?",
     "Most clients train 3&ndash;4 times per week. Your plan is adapted to your energy, recovery and lifestyle."),
    ("Is nutrition coaching included?",
     "Yes. Every package includes nutrition guidance, from simple fundamentals to fully personalised plans."),
    ("Can I cancel or pause my plan anytime?",
     "Yes, you can pause or cancel at any time. Life happens &mdash; your plan should flex with it."),
    ("How long will it take to see results?",
     "Most clients feel more energy within 2&ndash;3 weeks and see visible changes within 6&ndash;8 weeks of "
     "consistent training."),
]
faq = con([
    con([
        heading("FAQ", cls="pft-label", tag="div"),
        heading("Frequently<br>Asked Questions", cls="pft-h2", tag="h2"),
        text("<p>If you&rsquo;re new here or wondering what to expect, these answers will guide you through how "
             "coaching works, what&rsquo;s included, and how we tailor every plan to your needs.</p>"),
        button("Send e-mail", "mailto:hello@example.com", cls="pft-btn pft-btn--outline"),
    ], width=46, gap=16, align="flex-start", pad=(0, 0, 0, 8), tablet=FULL, mobile=FULL),
    con([toggle(faq_items)], width=48.6, tablet=FULL, mobile=FULL),
], cls="pft-faq", anchor="faq", top=True, direction="row", justify="space-between", gap=40,
    pad=(96, 0, 64, 0), tablet=STACK_T, mobile=STACK_M)

# 10. CONTACT ----------------------------------------------------------------
FORM = """<div class="pft-form-wrap">
<form class="pft-form" action="mailto:hello@example.com" method="post" enctype="text/plain">
  <div><label for="pft-name">Full name</label>
    <input id="pft-name" name="name" type="text" placeholder="Enter your full name" required></div>
  <div><label for="pft-email">Email</label>
    <input id="pft-email" name="email" type="email" placeholder="hello@example.com" required></div>
  <div><label for="pft-message">Message</label>
    <textarea id="pft-message" name="message" placeholder="Tell me about your goals or what you&rsquo;d like help with..."></textarea></div>
  <button type="submit">Send Message <span class="pft-form-arrow">&rarr;</span></button>
</form>
</div>"""


def contact_card(ic, title, sub, url, library="fa-solid"):
    return con([
        ico(ic, library=library),
        con([
            con([heading(title, cls="pft-h3", tag="h3"), text(f"<p>{sub}</p>", cls="pft-muted")], gap=4,
                grow=True),
            arrow(url),
        ], direction="row", align="flex-end", justify="space-between", gap=16),
    ], cls="pft-contact-card", justify="space-between", gap=24, pad=(24, 24, 24, 24), min_h=228, grow=True)


contact = con([
    con([
        heading("Contact", cls="pft-label", tag="div"),
        heading("Let&rsquo;s build your<br>plan together!", cls="pft-h2", tag="h2"),
        text("<p>Have a question about training, nutrition, or which program fits you best?<br>Reach out &mdash; "
             "we&rsquo;ll help you find your next step forward.</p>"),
    ], gap=12),
    con([
        con([
            contact_card("far fa-comments", "Chat", "Chat directly with coach Rachel", "#", library="fa-regular"),
            contact_card("fas fa-phone-alt", "Call us", "Mon - Fri, 8:00 - 17:00 (CET)", "tel:+10000000000"),
        ], width=48.6, gap=16, tablet=FULL, mobile=FULL),
        con([
            heading("Send a Message", cls="pft-form-title", tag="h3"),
            html_w(FORM),
        ], width=48.6, gap=20, tablet=FULL, mobile=FULL),
    ], direction="row", justify="space-between", gap=32, tablet={"direction": "column"},
        mobile={"direction": "column"}),
], cls="pft-contact", anchor="contact", top=True, gap=40, pad=SECTION_PAD, tablet={"pad": T_PAD},
    mobile={"pad": M_PAD})

CONTENT = [styles, hero, stats, testimonial, about, logos, services, process, programs, results, faq, contact]


# ---------------------------------------------------------------- export
def strip_private(node):
    if isinstance(node, dict):
        return {k: strip_private(v) for k, v in node.items() if not k.startswith("_local")}
    if isinstance(node, list):
        return [strip_private(v) for v in node]
    return node


template = {
    "version": "0.4",
    "title": "Personal Fitness Trainer",
    "type": "page",
    "page_settings": {"template": "elementor_header_footer", "hide_title": "yes"},
    "content": strip_private(CONTENT),
}

os.makedirs(os.path.join(ROOT, "elementor"), exist_ok=True)
with open(os.path.join(ROOT, "elementor", "personal-fitness-trainer.json"), "w") as f:
    json.dump(template, f, indent=1, ensure_ascii=False)


# ---------------------------------------------------------------- preview
# A rough HTML imitation of Elementor's front-end markup, so the CSS can be
# checked in a browser without WordPress. Not pixel-identical to Elementor.
def css_box(b):
    return f"{b['top']}px {b['right']}px {b['bottom']}px {b['left']}px"


def fa(i):
    return f'<i class="{i["value"]}" aria-hidden="true"></i>'


def r_widget(w):
    s, t = w["settings"], w["widgetType"]
    cls = f'elementor-element elementor-widget elementor-widget-{t} {s.get("_css_classes", "")}'
    style = "flex-grow:1;" if s.get("_flex_size") == "grow" else ""
    align = s.get("align")
    if align:
        style += f"text-align:{align};"
    if t == "heading":
        tag = s["header_size"]
        inner = f'<{tag} class="elementor-heading-title">{s["title"]}</{tag}>'
    elif t == "text-editor":
        inner = s["editor"]
    elif t == "button":
        inner = (f'<div class="elementor-button-wrapper"><a class="elementor-button" href="{s["link"]["url"]}">'
                 f'<span class="elementor-button-content-wrapper"><span class="elementor-button-icon">'
                 f'{fa(s["selected_icon"])}</span><span class="elementor-button-text">{s["text"]}</span></span></a></div>')
        if "pft-btn--block" in s.get("_css_classes", ""):
            style += "width:100%;"
    elif t == "image":
        local = s["image"]["url"].split("/")[-1]
        inner = f'<img src="../assets/images/{local}" alt="{html.escape(s["image"]["alt"])}">'
    elif t == "icon":
        inner = f'<div class="elementor-icon-wrapper"><div class="elementor-icon">{fa(s["selected_icon"])}</div></div>'
    elif t == "icon-list":
        lis = "".join(f'<li class="elementor-icon-list-item"><span class="elementor-icon-list-icon">'
                      f'{fa(i["selected_icon"])}</span><span class="elementor-icon-list-text">{i["text"]}</span></li>'
                      for i in s["icon_list"])
        inner = f'<ul class="elementor-icon-list-items">{lis}</ul>'
    elif t == "toggle":
        inner = '<div class="elementor-toggle">' + "".join(
            f'<div class="elementor-toggle-item"><div class="elementor-tab-title">'
            f'<span class="elementor-toggle-icon">{fa(s["selected_icon"])}</span>'
            f'<a class="elementor-toggle-title">{i["tab_title"]}</a></div>'
            f'<div class="elementor-tab-content" hidden>{i["tab_content"]}</div></div>'
            for i in s["tabs"]) + "</div>"
    elif t == "html":
        inner = s["html"]
    return f'<div class="{cls}" style="{style}"><div class="elementor-widget-container">{inner}</div></div>'


RESPONSIVE = {"tablet": [], "mobile": []}


def responsive_rules(c):
    s, boxed = c["settings"], c["settings"]["content_width"] == "boxed"
    for dev in RESPONSIVE:
        outer, inner = [], []
        for key, val in s.items():
            if not key.endswith("_" + dev):
                continue
            base = key[: -len(dev) - 1]
            if base == "padding":
                outer.append(f"padding:{css_box(val)}")
            elif base == "width":
                outer.append(f"width:{val['size']}{val['unit']}")
            elif base == "min_height":
                outer.append(f"min-height:{val['size']}px")
            else:
                prop = {"flex_direction": "flex-direction", "flex_gap": "gap", "flex_align_items": "align-items",
                        "flex_justify_content": "justify-content", "flex_wrap": "flex-wrap"}[base]
                v = f"{val['size']}px" if base == "flex_gap" else val
                (inner if boxed else outer).append(f"{prop}:{v}")
        sel = f".pv-{c['id']}"
        if outer:
            RESPONSIVE[dev].append(f"{sel}{{{';'.join(x + ' !important' for x in outer)}}}")
        if inner:
            RESPONSIVE[dev].append(f"{sel}>.e-con-inner{{{';'.join(x + ' !important' for x in inner)}}}")


def r_con(c):
    s = c["settings"]
    responsive_rules(c)
    flex = (f"display:flex;flex-direction:{s['flex_direction']};gap:{s['flex_gap']['size']}px;"
            f"align-items:{s.get('flex_align_items', 'stretch' if s['flex_direction'] == 'column' else 'normal')};"
            f"justify-content:{s.get('flex_justify_content', 'flex-start')};flex-wrap:{s.get('flex_wrap', 'nowrap')};")
    outer = f"padding:{css_box(s['padding'])};position:relative;"
    if "width" in s:
        w = s["width"]
        outer += f"width:{w['size']}{w['unit']};max-width:100%;flex-shrink:0;"
    if s.get("_flex_size") == "grow":
        outer += "flex-grow:1;flex-shrink:1;"
    if "min_height" in s:
        outer += f"min-height:{s['min_height']['size']}px;"
    if "background_color" in s:
        outer += f"background-color:{s['background_color']};"
    if "background_image" in s:
        local = s["background_image"]["url"].split("/")[-1]
        outer += f"background:url(../assets/images/{local}) center/cover no-repeat;"
    kids = "".join(r_con(k) if k["elType"] == "container" else r_widget(k) for k in c["elements"])
    tag = "a" if s.get("html_tag") == "a" else "div"
    href = f' href="{s["link"]["url"]}" style="text-decoration:none;color:inherit;' if tag == "a" else ' style="'
    idattr = f' id="{s["_element_id"]}"' if "_element_id" in s else ""
    cls = f'e-con pv-{c["id"]} {s.get("css_classes", "")}'
    over = ('<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 45%,'
            'rgba(0,0,0,.78) 100%);pointer-events:none"></div>') if "background_overlay_background" in s else ""
    if s["content_width"] == "boxed":
        return (f'<{tag}{idattr} class="{cls}"{href}{outer}display:flex;">{over}'
                f'<div class="e-con-inner" style="{flex}width:100%;max-width:{s['boxed_width']['size']}px;margin:0 auto;position:relative">'
                f'{kids}</div></{tag}>')
    return f'<{tag}{idattr} class="{cls}"{href}{outer}{flex}">{kids}</{tag}>'


BODY = "".join(r_con(c) for c in CONTENT)
MEDIA = ("@media(max-width:1024px){" + "".join(RESPONSIVE["tablet"]) + "}"
         "@media(max-width:767px){" + "".join(RESPONSIVE["mobile"]) + "}")
PREVIEW = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Personal Fitness Trainer — preview</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
<style>
*,*:before,*:after{{box-sizing:border-box}} body{{margin:0;background:#fff}}
.elementor-heading-title{{margin:0;padding:0;line-height:1}} .elementor-widget{{position:relative;min-width:0}}
.elementor-widget-image img{{max-width:100%;height:auto;vertical-align:middle}}
.elementor-button{{display:inline-block;text-decoration:none;cursor:pointer}}
.elementor-icon{{display:inline-block;line-height:1}} .elementor-icon i{{width:1em;height:1em;position:relative;display:block}}
.elementor-icon-list-items{{list-style:none;margin:0;padding:0}} .elementor-icon-list-item{{display:flex;align-items:center}}
.elementor-icon-list-icon{{display:flex}}
.e-con{{max-width:100%}} .elementor-tab-title{{cursor:pointer;outline:0}} .elementor-toggle-icon{{float:right;width:1em}} .elementor-toggle-title{{color:inherit}}
</style>
</head><body>
{BODY}
<style>{MEDIA}</style>
<script>document.querySelectorAll('.elementor-tab-title').forEach(function(t){{t.addEventListener('click',function(){{var c=t.nextElementSibling;c.hidden=!c.hidden;}});}});</script>
</body></html>
"""
os.makedirs(os.path.join(ROOT, "preview"), exist_ok=True)
with open(os.path.join(ROOT, "preview", "index.html"), "w") as f:
    f.write(PREVIEW)

print("Elements:", sum(1 for _ in json.dumps(template).split('"elType"')) - 1)
print("Wrote elementor/personal-fitness-trainer.json and preview/index.html")


# ---------------------------------------------------------------- copy/paste fallback
# The whole page as one HTML snippet, for an Elementor "HTML" widget or a
# Gutenberg "Custom HTML" block, when importing the JSON is not possible.
# Classes are renamed (elementor-* -> pfe-*, e-con -> pft-con) so Elementor's
# own stylesheets do not interfere, and images point to the GitHub copies.
import re


def standalone(s):
    s = s.replace("elementor-", "pfe-")
    s = re.sub(r"\be-con", "pft-con", s)
    return s.replace("../assets/images/", REPO_RAW)


base_css = re.search(r"<style>\n(.*?)</style>", PREVIEW, re.S).group(1).replace("{{", "{").replace("}}", "}")
base_css = re.sub(r"\*,\*:before,\*:after\{box-sizing:border-box\} body\{margin:0;background:#fff\}",
                  ".pft-page,.pft-page *,.pft-page *:before,.pft-page *:after{box-sizing:border-box}"
                  ".pft-page{width:100%;overflow:hidden;background:#fff}", base_css)


def snippet(containers, title):
    """Self-contained HTML (styles included) for the given top-level containers."""
    return standalone(f"""<!-- Personal Fitness Trainer — {title} -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
<style>
{base_css}
{re.sub(r"@import[^;]+;", "", CSS)}
{MEDIA}
.pft-page a{{text-decoration:none}}
.pft-page h1,.pft-page h2,.pft-page h3,.pft-page blockquote,.pft-page ul,.pft-page figure{{margin:0;padding:0}}
.pft-page blockquote{{border:0;quotes:none;font-style:normal;background:none}} .pft-page blockquote:before,.pft-page blockquote:after{{content:none}}
.pft-page img{{max-width:100%;border:0;box-shadow:none}}
</style>
<div class="pft-page">
{"".join(r_con(c) for c in containers)}
</div>
<script>document.querySelectorAll('.pft-page .pfe-tab-title').forEach(function(t){{if(t.dataset.pft)return;t.dataset.pft=1;t.addEventListener('click',function(){{var c=t.nextElementSibling;c.hidden=!c.hidden;}});}});</script>
""")


with open(os.path.join(ROOT, "elementor", "page-html-a-coller.html"), "w") as f:
    f.write(snippet(CONTENT[1:], "page complete a coller dans un widget HTML"))
print("Wrote elementor/page-html-a-coller.html")

# One block per section, each self-contained, to paste in separate HTML widgets.
BLOCKS = [
    ("01-hero", "Hero", [hero]),
    ("02-chiffres", "Chiffres cles", [stats]),
    ("03-temoignage", "Temoignage", [testimonial]),
    ("04-a-propos", "A propos + logos", [about, logos]),
    ("05-services", "Services", [services]),
    ("06-etapes", "How it works (etapes)", [process]),
    ("07-programmes", "Programmes / tarifs", [programs]),
    ("08-resultats", "Resultats", [results]),
    ("09-faq", "FAQ", [faq]),
    ("10-contact", "Contact", [contact]),
]
bdir = os.path.join(ROOT, "elementor", "blocs")
os.makedirs(bdir, exist_ok=True)
for slug, title, cons in BLOCKS:
    with open(os.path.join(bdir, slug + ".html"), "w") as f:
        f.write(snippet(cons, f"bloc {title}"))
print("Wrote", len(BLOCKS), "blocks in elementor/blocs/")
