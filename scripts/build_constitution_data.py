import json
import os
import re
import requests
from bs4 import BeautifulSoup

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
DOCS_DIR = os.path.join(os.path.dirname(__file__), '../docs')

def get_constitution_html():
    url = "https://www.anayasa.gov.tr/tr/mevzuat/anayasa/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    import urllib3
    urllib3.disable_warnings()
    response = requests.get(url, headers=headers, verify=False)
    response.encoding = 'utf-8' # Force utf-8
    return response.text

def parse_html_to_json(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    
    # anayasa.gov.tr'de madde metinleri genelde class="text-justify" veya benzeri p taglerinde bulunur.
    # Ancak daha garantili olan yol, tm metni alip dzenli ifadeler ile paralamaktir.
    
    text = soup.get_text('\n', strip=True)
    
    # Btn maddeleri bulalim: "MADDE X-" veya "MADDE X -" veya "Madde X-" seklinde.
    # Burada biraz daha gl bir regex olusturuyoruz
    article_pattern = re.compile(r'MADDE\s+(\d+)\s*[-]\s*(.*?\n)(?=MADDE\s+\d+\s*-|GEÇİCİ MADDE|Ek Madde|$)', re.IGNORECASE | re.DOTALL)
    
    # Gecici maddeler
    temp_article_pattern = re.compile(r'(GEÇİCİ MADDE\s+\d+)\s*[-]\s*(.*?\n)(?=GEÇİCİ MADDE|MADDE\s+\d+|Ek Madde|$)', re.IGNORECASE | re.DOTALL)
    
    articles = []
    
    # Normal maddeler
    for match in article_pattern.finditer(text):
        num_str = match.group(1).strip()
        content = match.group(2).strip()
        
        # Titli yakalamak - genelde maddenin icinden onceki satirda baslik olabilir ama
        # metin o kadar duzenli degildir, dogrudan metin olarak alalim
        
        articles.append({
            "id": int(num_str),
            "title": f"Madde {num_str}",
            "content": content
        })
        
    # Gecici maddeler
    for match in temp_article_pattern.finditer(text):
        title = match.group(1).strip()
        content = match.group(2).strip()
        
        # ID'yi string tutacagiz
        articles.append({
            "id": title,
            "title": title,
            "content": content
        })

    # Son bir kez siralayalim (sadece normal maddeleri; geciciler sona)
    norm_arts = sorted([a for a in articles if isinstance(a["id"], int)], key=lambda x: x["id"])
    temp_arts = [a for a in articles if isinstance(a["id"], str)]
    
    structured_data = {
        "title": "Türkiye Cumhuriyeti Anayasası",
        "last_updated": "2026-03-31",
        "structure": {
            "parts": [
                {
                    "title": "Tam Metin",
                    "articles": norm_arts + temp_arts
                }
            ]
        }
    }
    return structured_data

def chunk_markdown(structured_data):
    # Madde araliklarina gore md dosyalarini uretecegiz
    parts = {
        "part_1": (1, 11, "Başlangıç ve Genel Esaslar"),
        "part_2": (12, 74, "Temel Haklar ve Ödevler"),
        "part_3": (75, 160, "Cumhuriyetin Temel Organları"),
        "part_4": (161, 173, "Mali ve Ekonomik Hükümler"),
        "part_5": (174, 177, "Çeşitli ve Son Hükümler")
    }
    
    # Temizle ve olustur
    for p_file in parts.keys():
        path = os.path.join(DOCS_DIR, f"{p_file}.md")
        start, end, title = parts[p_file]
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"# Türkiye Cumhuriyeti Anayasası: {title}\n\n")
            
            for art in structured_data["structure"]["parts"][0]["articles"]:
                if isinstance(art["id"], int) and start <= art["id"] <= end:
                    f.write(f"**{art['title']}**\n\n{art['content']}\n\n---\n\n")

    # Gecici maddeler
    path = os.path.join(DOCS_DIR, "part_6_gecici.md")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"# Türkiye Cumhuriyeti Anayasası: Geçici Hükümler\n\n")
        for art in structured_data["structure"]["parts"][0]["articles"]:
            if isinstance(art["id"], str):
                 f.write(f"**{art['title']}**\n\n{art['content']}\n\n---\n\n")


def build():
    print("Scraping Anayasa...")
    html = get_constitution_html()
    data = parse_html_to_json(html)
    
    print(f"Parsed {len(data['structure']['parts'][0]['articles'])} articles.")
    
    # Write JSON
    json_path = os.path.join(DATA_DIR, 'constitution.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    # Write MDs
    chunk_markdown(data)
    print("DONE!")

if __name__ == "__main__":
    build()
