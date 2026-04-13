import requests
import re

# এখানে তুমি সোর্স লিঙ্কগুলো যোগ করবে
SOURCES = [
    "https://iptv-org.github.io/iptv/countries/bd.m3u"
]

def generate_playlist():
    playlist = "#EXTM3U\n"
    print("লিঙ্ক সংগ্রহের কাজ শুরু হচ্ছে...")

    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                # নাম এবং ভিডিও লিঙ্ক আলাদা করার কোড
                matches = re.findall(r'(#EXTINF.*?,(.*?)\n(http.*?))', r.text)
                for full_info, name, link in matches:
                    playlist += f"{full_info.strip()}\n{link.strip()}\n"
            else:
                print(f"লিঙ্কটি কাজ করছে না: {url}")
        except Exception as e:
            print(f"ত্রুটি: {e}")

    # আপডেট হওয়া ফাইলটি সেভ করা
    with open("live_tv.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)
    print("অভিনন্দন! live_tv.m3u ফাইলটি তৈরি হয়ে গেছে।")

if __name__ == "__main__":
    generate_playlist()
    
