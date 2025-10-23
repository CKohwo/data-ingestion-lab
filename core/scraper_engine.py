import requests
from bs4 import BeautifulSoup
import random
import time
import traceback

# ===== SAFE REQUEST WRAPPER ===== #
def safe_request(url, headers, retries=3, timeout=15):
    """Handles transient network issues, SSL, and slow responses gracefully."""
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout, verify=True)
            if response.status_code == 200:
                return response
            else:
                print(f"⚠️ Non-200 response ({response.status_code}) for {url}")
        except requests.exceptions.SSLError:
            print("⚠️ SSL error encountered — retrying with verify=False")
            try:
                response = requests.get(url, headers=headers, timeout=timeout, verify=False)
                if response.status_code == 200:
                    return response
            except Exception as e:
                print(f"⚠️ Retry {attempt+1}/{retries} failed (SSL): {e}")
        except Exception as e:
            print(f"⚠️ Retry {attempt+1}/{retries} failed: {e}")
        time.sleep(random.uniform(2, 5))
    print(f"❌ Max retries exceeded for {url}")
    return None


# ===== PRODUCT EXTRACTION LOGIC ===== #
def fetch_product_from_page(soup, selector):
    """Extracts structured data from a single HTML page."""
    results = []

    try:
        item_info = soup.select(selector["id"])
        if not item_info:
            print("⚠️ No items found on this page.")
            return results

        for item in item_info:
            try:
                name = item.select_one(selector["name"]).text.strip()
                price = item.select_one(selector["price"]).text.strip()
                ratings = (
                    item.select_one(selector["ratings"]).text.strip()
                    if item.select_one(selector["ratings"])
                    else "No ratings"
                )
                link = item.find("a", href=True)
                link = f"https://www.jumia.com.ng{link['href']}" if link else "No link available"

                results.append({
                    "Name": name,
                    "Price": price,
                    "Ratings": ratings,
                    "Description Link": link,
                })
            except Exception as e:
                print(f"⚠️ Error parsing one product: {e}")
                continue

    except Exception as e:
        print(f"❌ Error in fetch_product_from_page: {traceback.format_exc()}")

    return results


# ===== MAIN PAGINATION FUNCTION ===== #
def fetch_all_products(base_url, headers, selector, max_pages=20):
    """Fetches all products across pages with resilience for Render."""
    page = 1
    final_results = []

    while page <= max_pages:
        print(f"\n🔄 Scraping page {page}...")

        url = f"{base_url}?page={page}"
        response = safe_request(url, headers)
        if not response:
            print("❌ Request failed — moving to next category.")
            break

        try:
            soup = BeautifulSoup(response.text, "lxml")
            product_batch = fetch_product_from_page(soup, selector)

            if not product_batch:
                print(f"⚠️ No more products found (page {page}). Stopping pagination.")
                break

            final_results.extend(product_batch)
            print(f"✅ Page {page} done — {len(product_batch)} items found.")

            next_page = soup.select_one(selector.get("page_next"))
            if not next_page:
                print("📘 End of pagination reached.")
                break

            # Human-like delay
            sleep_time = random.uniform(4, 8)
            print(f"⏳ Sleeping {sleep_time:.1f}s before next page...")
            time.sleep(sleep_time)

            page += 1

        except Exception as e:
            print(f"❌ Error parsing page {page}: {e}")
            break

    print(f"\n📦 Total products scraped: {len(final_results)}\n")
    return final_results
