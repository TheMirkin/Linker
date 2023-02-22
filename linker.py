# -*- coding: utf-8 -*
# ======================== #
#       Linker V1.0        #
#       @TheMirkin         #
#    www.themirkin.org     #
# ======================== #
import requests
from bs4 import BeautifulSoup
import json
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='bs4') # hataları gizleyelim

# Url'den iç bağlantıları alır
def get_internal_links(url, depth=1):
    print("Url'den iç bağlantıları alıyor")
    visited_links = set()
    internal_links = set() # Alınan iç bağlantıları saklamak için   
    def _get_internal_links(url, depth):
        if depth == 0 or url in visited_links:
            return
        visited_links.add(url) # Bu url'yi ziyaret edildi olarak kaydedin.
        try:
            response = requests.get(url)
        except:    
            return
        if response.status_code != 200:
            return
        soup = BeautifulSoup(response.content, "html.parser")        
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and href.startswith("/") and not href.startswith("//"):
                internal_link = url + href
                if internal_link not in visited_links:# Daha önce ziyaret edilmediyse iç bağlantı olarak kabul edin
                    internal_links.add(internal_link) # İç bağlantıları sakla
                    _get_internal_links(internal_link, depth= - 1)
    _get_internal_links(url, depth)
    return list(internal_links)

# İç bağlantıları dosyaya kaydeder

def save_internal_links(url, depth=1):
    links = get_internal_links(url, depth)
    file_extension = "json"
    output_formatter = json.dumps
    file_name = f"{url.strip('/').replace('https://', '').replace('http://', '')}.internal-links.{file_extension}"
    with open(file_name, "w") as f:
        f.write(output_formatter(links))
        print("Kayıt İşlemi tamamlandı")
        print(f"Toplam {len(links)} Link {file_name} dosyasına yazıldı")

# input al
domain = input("Domain girin: ")
depth_input = input("Depth girin: ")
# depth boşsa
if not depth_input:
    save_internal_links(domain)
    print("Derinlik Düzeyi 1 olarak işlenicektir")
# depth doluysa
else:
    try:
        depth = int(depth_input)
    except ValueError:
        print("Lütfen geçerli bir depth değeri girin!")
    else:
        print(f"Taranan {domain} derinlik Düzeyi {depth_input}.")
        save_internal_links(domain, depth=depth_input)


