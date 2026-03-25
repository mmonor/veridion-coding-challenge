import pandas as pd
from playwright.sync_api import sync_playwright


def getStack(page):
    return page.evaluate("""
        () => {
            const techs = [];
            const doc = document.documentElement.innerHTML;

            if (window.Shopify || doc.includes('cdn.shopify.com')) techs.push('Shopify');
            if (window.bigcommerce_config || window.BC) techs.push('BigCommerce');
            if (window.WooCommerce || document.querySelector('.woocommerce')) techs.push('WooCommerce');
            if (window.Mage || window.Magento) techs.push('Magento');
            if (window.wixEmbedsAPI || window.Wix) techs.push('Wix');
            if (doc.includes('static1.squarespace.com')) techs.push('Squarespace');
            if (window.PrestaShop) techs.push('PrestaShop');
            if (window.Joomla) techs.push('Joomla');
            if (window.Drupal) techs.push('Drupal');
            if (doc.includes('hubspot.com')) techs.push('HubSpot');

            if (window.React || !!document.querySelector('[data-reactroot]')) techs.push('React');
            if (window.Vue || !!document.querySelector('[data-v-')) techs.push('Vue');
            if (window.next) techs.push('Next.js');
            if (window.jQuery) techs.push('jQuery');
            if (window.angular || !!document.querySelector('[ng-version]')) techs.push('Angular');
            if (window.Alpine) techs.push('Alpine.js');
            if (window.Svelte) techs.push('Svelte');
            if (doc.includes('data-astro-cid')) techs.push('Astro');

            if (window.google_tag_manager || window.ga || window.gtag) techs.push('Google Analytics/GTM');
            if (window.fbq) techs.push('Facebook Pixel');
            if (window.ttq) techs.push('TikTok Pixel');
            if (window.hj) techs.push('Hotjar');
            if (window.klaviyo) techs.push('Klaviyo');
            if (window.pintrk) techs.push('Pinterest Tag');
            if (window.snaptrid) techs.push('Snap Pixel');
            if (window.reCharge) techs.push('Recharge');
            if (window.Intercom) techs.push('Intercom');
            if (window.Gorgias) techs.push('Gorgias');

            if (window.bootstrap || !!document.querySelector('[class*="bootstrap"]')) techs.push('Bootstrap');
            if (doc.includes('tw-') || doc.includes('tailwind')) techs.push('Tailwind CSS');
            if (doc.includes('cloudflare')) techs.push('Cloudflare');
            if (doc.includes('s3.amazonaws.com')) techs.push('Amazon S3');
            if (doc.includes('wp-content')) techs.push('WordPress');
            if (doc.includes('fonts.googleapis.com')) techs.push('Google Fonts');
            if (doc.includes('font-awesome')) techs.push('Font Awesome');
            if (window.grecaptcha) techs.push('reCAPTCHA');
            if (window.hcaptcha) techs.push('hCaptcha');
            if (window.OneTrust) techs.push('OneTrust');
            if (window.Cookiebot) techs.push('Cookiebot');
            if (doc.includes('stripe.com')) techs.push('Stripe');
            if (doc.includes('paypal.com')) techs.push('PayPal');

            return [...new Set(techs)]; 
        }
    """)


results = []
df = pd.read_csv("clean_data.csv", names=['domain'])

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # Added viewport - some sites require a visual area to render
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        ignore_https_errors=True,
        viewport={'width': 1280, 'height': 720}
    )
    page = context.new_page()

    for domain in df['domain']:
        clean_domain = domain.strip()
        # Try HTTPS first
        protocols = [f"https://{clean_domain}", f"http://{clean_domain}"]
        success = False

        for url in protocols:
            if success: break
            print(f"Analyzing {url}")
            try:
                
                page.goto(url, timeout=20000, wait_until="load")
                page.wait_for_timeout(2000)

                js_stack = getStack(page)
                content = page.content().lower()

                html_stack = []
                if "wp-content" in content: html_stack.append("WordPress")
                if "cloudflare" in content: html_stack.append("Cloudflare")
                if "vimeo.com" in content: html_stack.append("Vimeo")
                if "youtube.com" in content: html_stack.append("YouTube")

                final_stack = list(set(js_stack + html_stack))
                results.append({
                    "domain": clean_domain,
                    "techs": ", ".join(final_stack),
                    "count": len(final_stack)
                })
                success = True
            except Exception as e:
                if url == protocols[-1]:
                    results.append({"domain": clean_domain, "techs": "Unreachable", "count": 0})
                    print(f"Failed all protocols for {clean_domain}")

    browser.close()

output_df = pd.DataFrame(results)
output_df.to_csv("output.csv", index=False)