# Türkiye Cumhuriyeti Anayasası (2026 Güncel)

Bu depo, Türkiye Cumhuriyeti Anayasası'nın (1982) tüm değişiklikleri içeren en güncel metnini yapılandırılmış bir formatta sunar. 

## Proje Amacı

Bu çalışma, anayasa metninin hem insanlar tarafından rahatça okunabilmesini hem de veri bilimciler, hukuk teknolojileri (LegalTech) geliştiricileri ve yapay zeka (AI) ajanları tarafından kolayca işlenebilmesini amaçlamaktadır.

## Depo Yapısı

- `docs/`: Anayasanın bölümlere ayrılmış Markdown (.md) formatındaki metinleri.
- `data/`: Anayasa maddelerinin hiyerarşik JSON formatındaki veri seti.
- `scripts/`: Anayasa üzerinde arama yapmaya ve madde çekmeye yarayan yardımcı araçlar.

## Güncellik Notu

Metin, **31 Mart 2026** tarihi itibarıyla yürürlükte olan resmi mevzuat esas alınarak derlenmiştir. 2017 Anayasa değişikliği ile gelen Cumhurbaşkanlığı Hükümet Sistemi ve sonrasındaki tüm idari düzenlemeler metne işlenmiştir.

## Kullanım Koşulları

Türkiye Cumhuriyeti kanunları ve resmi metinleri üzerindeki telif hakları, *Fikir ve Sanat Eserleri Kanunu Madde 31* uyarınca kamuya aittir. Bu veri seti herhangi bir kısıtlama olmaksızın (AI eğitimi, akademik çalışma, ticari projeler vb.) kullanılabilir.

## Kurulum ve Kullanım (Geliştiriciler İçin)

Depodaki Markdown ve JSON dosyaları kullanıma hazırdır. Ancak verileri doğrudan kaynağından **yeniden çekmek** veya CLI üzerinden **arama yapmak** isterseniz:

1. Gereksinimleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
2. Güncel anayasayı yeniden ayrıştırmak ve dosyaları üretmek için:
   ```bash
   python scripts/build_constitution_data.py
   ```
3. Terminal üzerinden belirli bir maddeyi okumak için:
   ```bash
   python scripts/search_article.py 177
   ```

---
*Not: Bu depo resmi bir devlet organı tarafından değil, açık veri prensipleriyle oluşturulmuştur. Olası değişiklikler anında Pushlanamayabilir, her sorguda güncelliğini teyid etmeniz şiddetle tavsiye edilir*
