import sys
from playwright.sync_api import sync_playwright
B = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765/"
shots = [("home-desktop-1280.png", "", 1280), ("home-mobile-390.png", "", 390),
         ("article-desktop-1280.png", "courts/sample-federal-appeals-ruling/", 1280),
         ("article-mobile-390.png", "courts/sample-federal-appeals-ruling/", 390),
         ("desk-desktop-1280.png", "courts/", 1280), ("about-desktop-1280.png", "about/", 1280)]
with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    for name, path, w in shots:
        pg = br.new_page(viewport={"width": w, "height": 900}, device_scale_factor=1 if w > 600 else 2, is_mobile=w < 600, has_touch=w < 600)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
        pg.goto(B + path, wait_until="networkidle"); pg.evaluate("window.scrollTo(0, document.body.scrollHeight)"); pg.wait_for_timeout(600); pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300)
        pg.screenshot(path=f"screenshots/{name}", full_page=True)
        print(name, "errors:", errs)
        pg.close()
    br.close()
