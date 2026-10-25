---
name: ig-profile
description: >-
  Instagram profilini, biyografisini, isim alanını ve sabit gönderilerini değerlendir. Use for profile audits, bios and profile optimization.
---

# Profil Değerlendirmesi / Instagram Agent

Türkçe isteklerde `references/workflow.tr.md` dosyasını oku. For English requests, read `references/workflow.en.md`. İki dosyayı birden yüklemek gerekmez.

## Ortak çalışma kuralları

- Kullanıcının dilinde yaz; varsayılan Türkçedir. Türkçe metin için araçlara `--lang tr` geçir. İngilizce metinde `--lang en` kullan.
- Bu skill'in gerçek klasörünü belirle. Aşağıdaki Python komutlarını o klasörde çalıştır veya betiğin mutlak yolunu kullan. Windows'ta `python3` yerine mevcutsa `py -3` ya da `python` kullan. Python 3.10+ gerekir.
- Marka verileri için `IG_AGENT_HOME` ortam değişkenini kullan; ayarlı değilse kullanıcı ana klasöründeki `.instagram-agent` dizinini kullan. Var olan `voice.md`, `swipe.md`, `plan.md`, `log.md` dosyalarından yalnızca gerekenleri oku. Kişisel verileri bu Git deposuna kaydetme.
- `voice.md` yoksa depodaki `templates/voice.md` şablonunu öner; mevcut kullanıcı bağlamıyla ilerle. Yalnızca sonucu değiştiren eksik bilgiyi sor. Kullanıcıya tekrar onay soruları yöneltme; verilmiş yetkiyi kullan.
- Diğer becerilere Codex'te `$ig-reel` gibi başvur; Claude'da `/ig-reel` kullanılabilir. Ayrı beceri çağırma aracı yoksa ilgili `SKILL.md` dosyasını oku ve iş akışını uygula.
- Müşteri, sonuç, gelir, başarı oranı ve alıntı uydurma. Bilinmeyen bilgiye `{{doğrulanacak bilgi}}` yaz. Örneklerdeki rakamlar kurgusal örneklerdir; kullanıcının sonucu gibi sunma.
- Platform sınırları ve algoritma iddiaları değişebilir. Sayıları düzenleme önerisi olarak ele al; güncel bir platform kuralı olduğunu iddia edeceksen resmî kaynaktan doğrula.
- Bu paket içerik ve yanıt taslağı üretir. Instagram'a gönderi, yorum veya DM göndermez; zamanlayıcı kurmaz. Hesap verisi isteyen işler için kullanıcının sağladığı veri veya ayrıca yetkilendirilmiş bir okuma aracı gerekir.
- Puanları editoryal kontrol olarak açıkla. Türkçe puanlar gerçek bir Reels veri kümesiyle kalibre edilmemiştir; viral olma veya AI yazarlığı olasılığı değildir. Araç çıktısındaki teknik İngilizce ayrıntıları Türkçe yorumla.
