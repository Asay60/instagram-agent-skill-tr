# Instagram Agent TR — Codex ve Claude

[English](README.en.md) · [Kaynak ve lisans](UPSTREAM.md)

Instagram için **13 Türkçe/İngilizce içerik becerisi** ve **7 yerel Python aracı**. Reels senaryosu, açıklama, carousel, Story, profil değerlendirmesi ve içerik planı hazırlar.

Jake Schincariol'un [instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) projesinin **ASAYTECH tarafından Türkçe ve Codex için uyarlanmış sürümüdür**. Kaynak proje ve MIT telif bildirimi korunur. Resmî OpenAI, Anthropic veya Meta ürünü değildir.

## Bu sürümde ne var?

- Türkçe iş akışları; ayrı referanslarda korunan İngilizce iş akışları.
- Codex ve Claude için kullanıcı/proje kapsamlı kurulum.
- Türkçe karakterleri bölmeyen sözcük sayımı; Türkçe sayılar, hitaplar, CTA ve hashtag desteği.
- 26 Türkçe açılış kalıbı, Türkçe metin düzenleme sözlüğü ve profil rubriği.
- İngilizce kısaltmaları Türkçe metinden beklemeyen üslup kontrolü.
- Ortak `IG_AGENT_HOME` marka veri yolu; farklı çalışma klasörlerinden betik çağrısı.
- Emoji birleşimlerini koruyan temizleme ve kurulum çakışmalarına karşı yedekleme.

**Bu paket taslak üretir.** Instagram'a giriş yapmaz; gönderi, yorum veya DM yayınlamaz; otomatik veri toplamaz ve video render motoru içermez. Carousel görselleri ve canlı araştırma için ayrıca uygun araç gerekir. Skill kurmak Instagram hesabına erişim yeteneği kazandırmaz.

## Hızlı kurulum

Git ve Python 3.10+ gerekir. Yerel Python araçları için üçüncü taraf paket veya API anahtarı gerekmez. Ajan/model kullanımı kendi hesabınızın koşullarına tabidir.

```bash
git clone https://github.com/Asay60/instagram-agent-skill-tr.git
cd instagram-agent-skill-tr
python3 scripts/install.py --agent codex
```

Windows PowerShell'de son komut:

```powershell
py -3 -X utf8 scripts/install.py --agent codex
```

Codex'te kullanım:

```text
$ig-reel Teklif gönderdikten sonra takip etmeyi unutan işletmeler için
30 saniyelik Türkçe Reels hazırla. Sonuç veya müşteri rakamı uydurma.
Tek CTA: WhatsApp üzerinden 15 dk ücretsiz süreç analizi.
```

Beceri görünmezse Codex oturumunu yeniden açın. [Resmî Codex skills belgesi](https://developers.openai.com/codex/skills) yerel beceri keşfini açıklar.

Claude için:

```bash
python3 scripts/install.py --agent claude
```

Ardından `/ig-reel` kullanın. Alternatif marketplace kurulumu:

```text
/plugin marketplace add Asay60/instagram-agent-skill-tr
/plugin install instagram-agent-tr@instagram-agent-skill-tr
```

Marketplace kurulumu canlı istemcide denenmedi; Python kurucusu otomatik testlerle doğrulandı. Codex için bu sürüm bir marketplace manifesti içermez; yerel skills kurulumu kullanılır.

## Kurulum seçenekleri

| Seçenek | Hedef |
| --- | --- |
| `--agent codex` | `~/.agents/skills` |
| `--agent claude` | `~/.claude/skills` |
| `--scope project` | Çalışma klasöründe `.agents/skills` veya `.claude/skills` |
| `--dest /tam/yol` | Belirtilen beceri dizini |
| `--overwrite` | Mevcut paket klasörlerini keşif dizini dışına yedekleyip değiştirir |

Kurucu çakışmada varsayılan olarak durur. Mevcut `ig-*` becerilerinizi incelemeden `--overwrite` kullanmayın. Tüm paketi birlikte kurun; `_instagram_agent_shared` klasörü ve beceriler arası bağlantılar gereklidir. Kurucu marka dosyalarını ve kimlik bilgilerini değiştirmez.

## Marka sesini tanımlayın

`templates/voice.md` dosyasını ana klasörünüzde `.instagram-agent/voice.md` olarak kopyalayıp doldurun. İngilizce şablon: `templates/voice.en.md`.

İsterseniz `IG_AGENT_HOME` değişkenini ayrı bir marka dizinine ayarlayın. `voice.md`, `swipe.md`, `plan.md` ve `log.md` burada tutulur. Betiklerde `--out` yolunu açıkça belirtin; değişkeni ajan iş akışları çözümler. Kişisel/müşteri dosyalarını herkese açık depoya eklemeyin.

## 13 beceri

| Codex | Görevi |
| --- | --- |
| `$ig-reel` | Açılış seçenekleri, senaryo, ekran metni ve tahmini süre |
| `$ig-viral` | Sağlanan/yetkili örneklerden hesap tabanına göre karşılaştırma |
| `$ig-caption` | Açıklama, yaklaşık ilk görünüm ve CTA kontrolü |
| `$ig-carousel` | Slayt metinleri ve mevcut araçlarla görsel üretim planı |
| `$ig-story` | Kare akışı ve çıkartma önerileri |
| `$ig-profile` | 12 ölçütle gözlenebilir profil değerlendirmesi |
| `$ig-plan` | Haftalık içerik planı |
| `$ig-human` | Sadeleştirme ve editoryal üslup kontrolü |
| `$ig-comment` | Başka gönderiler için yorum taslakları |
| `$ig-reply` | Kendi yorumlarına yanıt taslakları |
| `$ig-dm` | Mesaj, kaynak teslimi ve takip taslakları |
| `$ig-repurpose` | Uzun kaynaktan bağımsız kısa içerikler |
| `$ig-audit` | Verilen performans verilerinden bulgular ve denemeler |

Claude'da `$ig-reel` yerine `/ig-reel` kullanılır. Ayrı beceri çağırma aracı yoksa ajan ilgili `SKILL.md` dosyasını okuyabilir.

## Python araçları

Komutları depo kökünde çalıştırın; başka klasörde betiğin tam yolunu kullanın. Windows'ta `python3` yerine `py -3 -X utf8` kullanılabilir.

```bash
python3 skills/ig-reel/hookscore.py hooks.txt --lang tr --json
python3 skills/ig-reel/beats.py script.txt --lang tr --target 30 --wpm 165 --json
python3 skills/ig-caption/caption.py caption.txt --lang tr --keywords "satış otomasyonu,teklif takibi" --json
python3 skills/ig-human/humanize.py draft.txt --lang tr -o clean.txt --report
python3 skills/ig-human/detect.py draft.txt clean.txt --lang tr --json
python3 skills/ig-viral/swipe.py captured.tsv --lang tr --out swipe.md --json
```

Dil belirtilmezse `en` kullanılır. `--lang tr` analiz sözlüklerini de değiştirir. JSON alan adları ve bazı teknik tanı mesajları İngilizce kalır; bu sürüm CLI'nin her satırının birebir çevirisini vaat etmez. Türkçe iş akışları sonuçların Türkçe açıklanmasını ister.

`hookscore`, `caption` ve `detect` editoryal puan/uyarı nedeniyle **1** dönebilir. Bu tek başına çalıştırma çökmesi değildir. Başarılı analizde JSON üretilir; girdi ve kurulum hatalarını ayrıca inceleyin.

## Ölçüm sınırları

- Türkçe puanlar **gerçek Türkçe Reels veri kümesiyle kalibre edilmedi**. Testler yazılımı denetler; pazarlama başarısını kanıtlamaz.
- Açılış puanı viral olma tahmini değildir. Kaynak projenin İngilizce/YouTube Shorts ölçümleri Türkçe sürümün doğrulaması sayılmaz.
- `detect.py` **AI yazarlığı tespit etmez**. Puanlar editoryal sinyallerdir. Görünmez karakter veya düzgün noktalama AI kanıtı değildir.
- Süreler sözcük sayısından tahmin edilir; Türkçede heceler ve duraklarla değişir. Kayıtla ölçün.
- 125 karakter önizlemesi yaklaşık; beş hashtag yapılandırılabilir öneridir (`--truncate`, `--hashtag-limit`). Canlı platform limiti değildir.
- `swipe.py` için tam tamsayı kullanın (4500). K/M/bin kısaltmaları reddedilir. `median` boşsa takipçi tabanı kullanılır; farklı `baseline_kind` değerlerini eşdeğer yorumlamayın.
- Yerel araçlar veri yüklemez. Bir AI hizmetine verdiğiniz içerik seçtiğiniz sağlayıcının veri işlemesine tabidir.

## Test

```bash
python3 -m unittest discover -s tests -v
```

Testler iki dilde CLI, Türkçe karakterler, CTA/hashtagler, emoji/URL koruması, süre hesabı, formüller ve kurucu çakışma/yedek davranışını denetler. Gerçek Codex/Claude istemcisi ve Instagram üzerinde uçtan uca çalışma ayrıca doğrulanmalıdır.

## Katkı ve lisans

MIT. Kaynak: **Jake Schincariol / opusjake.ai**. Türkçe ve Codex uyarlaması: **ASAYTECH / Asay60**. Kaynak commit ve değişiklik kapsamı [UPSTREAM.md](UPSTREAM.md) içinde; telif bildirimi [LICENSE](LICENSE) dosyasındadır.
