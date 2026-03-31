import json
import os
import sys

# Dosya yolu
DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/constitution.json')

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Hata: {DATA_FILE} dosyası bulunamadı.")
        return None

def find_article(data, article_id):
    """Madde numarasına göre arama yapar."""
    all_articles = []
    
    # JSON yapısını tarayarak tüm maddeleri topla
    for part in data.get('structure', {}).get('parts', []):
        if 'articles' in part:
            all_articles.extend(part['articles'])
        if 'sections' in part:
            for section in part['sections']:
                if 'articles' in section:
                    all_articles.extend(section['articles'])
    
    # ID'ye göre filtrele
    for art in all_articles:
        if art.get('id') == article_id:
            return art
    return None

def main():
    if len(sys.argv) < 2:
        print("Kullanım: python search_article.py <madde_no>")
        sys.exit(1)
    
    try:
        target_id = int(sys.argv[1])
    except ValueError:
        print("Hata: Lütfen bir sayı girin.")
        sys.exit(1)
    
    data = load_data()
    if not data:
        return
    
    article = find_article(data, target_id)
    
    if article:
        print(f"\n--- MADDE {article['id']}: {article['title']} ---")
        print(f"\n{article['content']}\n")
    else:
        print(f"\nMadde {target_id} bulunamadı veya henüz veritabanına eklenmedi.\n")

if __name__ == "__main__":
    main()
