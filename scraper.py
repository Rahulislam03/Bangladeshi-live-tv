import requests
import re

SOURCES = [
    "https://raw.githubusercontent.com/tuhinbd88/TV/main/BD.m3u",
    "https://iptv-org.github.io/iptv/countries/bd.m3u",
    "https://raw.githubusercontent.com/m-reza/BDIX-IPTV/main/playlist.m3u"
]

def generate_playlist():
    playlist = "#EXTM3U\n"
    unique_links = set()
    print("লিঙ্ক সংগ্রহের কাজ শুরু হচ্ছে...")

    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                # লাইন বাই লাইন প্রসেসিং যাতে এরর না হয়
                lines = r.text.split('\n')
                for i in range(len(lines)):
                    if lines[i].startswith('#EXTINF'):
                        info_line = lines[i].strip()
                        # এর ঠিক পরের লাইনেই সাধারণত লিঙ্ক থাকে
                        if i + 1 < len(lines):
                            link_line = lines[i+1].strip()
                            if link_line.startswith('http') and link_line not in unique_links:
                                playlist += f"{info_line}\n{link_line}\n"
                                unique_links.add(link_line)
            else:
                print(f"সোর্স কাজ করছে না: {url}")
        except Exception as e:
            print(f"এরর: {e}")

    with open("live_tv.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)
    
    print(f"মোট {len(unique_links)}টি চ্যানেল লিস্টে যোগ হয়েছে!")

if __name__ == "__main__":
    generate_playlist()
    
