import requests
import re

# আরও শক্তিশালী এবং নতুন সোর্স লিস্ট
SOURCES = [
    "https://raw.githubusercontent.com/tuhinbd88/TV/main/BD.m3u",
    "https://iptv-org.github.io/iptv/countries/bd.m3u",
    "https://raw.githubusercontent.com/m-reza/BDIX-IPTV/main/playlist.m3u",
    "https://raw.githubusercontent.com/TidbitsJS/Live-TV-IPL/master/bangladesh.m3u"
]

def check_link(url):
    try:
        # head এর বদলে get ব্যবহার করছি ছোট চাঙ্ক নিয়ে, এটি আরও নির্ভুল
        r = requests.get(url, timeout=5, stream=True)
        return r.status_code == 200
    except:
        return False

def generate_playlist():
    playlist = "#EXTM3U\n"
    found_count = 0
    unique_links = set()

    print("লিঙ্ক সংগ্রহের কাজ শুরু হচ্ছে...")

    for url in SOURCES:
        try:
            print(f"চেক করা হচ্ছে: {url}")
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                # উন্নত রেগুলার এক্সপ্রেশন
                matches = re.findall(r'(#EXTINF.*?,(.*?)\n(http.*?))', r.text)
                
                for full_info, name, link in matches:
                    clean_link = link.strip()
                    if clean_link not in unique_links:
                        # শুরুতে আমরা সব লিঙ্ক সেভ করব (চেকিং ছাড়া), পরে আস্তে আস্তে ফিল্টার শিখব
                        playlist += f"{full_info.strip()}\n{clean_link}\n"
                        unique_links.add(clean_link)
                        found_count += 1
            else:
                print(f"সোর্স কাজ করছে না: {url}")
        except Exception as e:
            print(f"ত্রুটি: {e}")

    with open("live_tv.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)
    
    print(f"\nমোট {found_count}টি চ্যানেল পাওয়া গেছে!")

if __name__ == "__main__":
    generate_playlist()
    
