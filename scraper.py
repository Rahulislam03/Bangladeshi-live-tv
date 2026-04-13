import requests
import re

# সচল এবং নতুন সোর্স লিস্ট
SOURCES = [
    "https://raw.githubusercontent.com/tuhinbd88/TV/main/BD.m3u",
    "https://raw.githubusercontent.com/byte-capsule/Fanatix-IPTV-List/main/IPTV.m3u",
    "https://iptv-org.github.io/iptv/countries/bd.m3u"
]

def check_link(url):
    """লিঙ্কটি বর্তমানে লাইভ আছে কি না তা চেক করে"""
    try:
        # শুধু হেডার রিকোয়েস্ট পাঠিয়ে চেক করা হচ্ছে (সময় বাঁচাতে)
        r = requests.head(url, timeout=5, allow_redirects=True)
        return r.status_code == 200
    except:
        return False

def generate_playlist():
    playlist = "#EXTM3U\n"
    print("লিঙ্ক সংগ্রহের কাজ শুরু হচ্ছে...")
    
    unique_links = set() # একই চ্যানেল বারবার আসা বন্ধ করতে

    for url in SOURCES:
        try:
            print(f"স্ক্যান করা হচ্ছে: {url}")
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                # নাম এবং লিঙ্ক আলাদা করার প্যাটার্ন
                matches = re.findall(r'(#EXTINF.*?,(.*?)\n(http.*?))', r.text)
                
                for full_info, name, link in matches:
                    clean_link = link.strip()
                    clean_name = name.strip()
                    
                    # যদি লিঙ্কটি আগে না এসে থাকে এবং সচল হয়
                    if clean_link not in unique_links:
                        if check_link(clean_link):
                            playlist += f"{full_info.strip()}\n{clean_link}\n"
                            unique_links.add(clean_link)
                            print(f"সচল পাওয়া গেছে: {clean_name}")
                        else:
                            print(f"বাদ দেওয়া হলো (Dead): {clean_name}")
            else:
                print(f"সোর্স কাজ করছে না: {url}")
        except Exception as e:
            print(f"ত্রুটি: {e}")

    # আপডেট হওয়া ফাইলটি সেভ করা
    with open("live_tv.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)
    
    print(f"\nমোট {len(unique_links)}টি সচল চ্যানেল পাওয়া গেছে!")
    print("অভিনন্দন! live_tv.m3u ফাইলটি পুরোপুরি আপডেট হয়ে গেছে।")

if __name__ == "__main__":
    generate_playlist()
                
