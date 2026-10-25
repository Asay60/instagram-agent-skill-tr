"""Dependency-free English/Turkish support shared by the seven upstream tools.

JSON keys remain stable. Scores are editorial heuristics, never AI authorship
or virality probabilities. Call configure_locale before analysing Turkish text.
"""
import re
import unicodedata
from pathlib import Path

LANG = "en"
EMOJI_RE = re.compile(r"[\U0001F000-\U0001FAFF\u2600-\u27BF](?:[\uFE0F\U0001F3FB-\U0001F3FF\U000E0020-\U000E007F]|\u200D[\U0001F000-\U0001FAFF\u2600-\u27BF])*")
WORD_RE = re.compile(r"(?:[$₺€£]\s*)?\d+(?:[.,]\d+)*(?:%|₺|[$€£])?|[^\W\d_]+(?:['’][^\W\d_]+)*|\d+", re.UNICODE)
PROPER_RE = re.compile(r"(?<!^)\b[A-ZÇĞİÖŞÜ][a-zçğıöşü]{2,}\b")
NUMBER_RE = re.compile(r"(?:[$₺€£]\s*)?\d[\d.,]*(?:\s*(?:%|TL|tl|₺|lira|saat|dakika|gün|hafta|ay|yıl))?")
CONCRETE_RE = re.compile(r"[$₺€£]\s?\d|\b\d[\d,.]*\b|(?<!^)\b[A-ZÇĞİÖŞÜ][a-zçğıöşü]{2,}\b", re.MULTILINE)


def lower(text):
    text = unicodedata.normalize("NFC", text)
    return text.translate(str.maketrans({"I": "ı", "İ": "i"})).lower() if LANG == "tr" else text.lower()


def protect_emoji(text):
    found = []
    def stash(match):
        found.append(match.group(0))
        return f"\x00EMOJI{len(found)-1}\x00"
    return EMOJI_RE.sub(stash, text), found


def configure_locale(namespace, lang):
    """Configure one standalone tool; the default English behavior is retained."""
    global LANG
    keys = ("WORD_RE", "PROPER_RE", "PROPER", "NUMBER_RE", "CONCRETE_RE", "NUMBERS",
            "SPOKEN_NUMBERS", "MONEY_WORDS", "STAKES", "IMPERATIVES", "STOPWORDS",
            "WEAK_OPENERS", "DEALBREAKERS", "check_address", "ASKS", "HASHTAG_RE",
            "FILLER_TAGS", "PRONOUNS", "check_voice", "LEX", "HOOKS")
    if "_LOCALE_BASELINE" not in namespace:
        namespace["_LOCALE_BASELINE"] = {key: namespace[key] for key in keys if key in namespace}
    namespace.update(namespace["_LOCALE_BASELINE"])
    LANG = lang
    namespace["LANG"] = lang
    # All languages benefit from intact Unicode tokens (also decomposed input).
    if "WORD_RE" in namespace:
        namespace["WORD_RE"] = WORD_RE
    if lang != "tr":
        return
    for name, pattern in (("PROPER_RE", PROPER_RE), ("PROPER", PROPER_RE),
                          ("NUMBER_RE", NUMBER_RE), ("CONCRETE_RE", CONCRETE_RE),
                          ("NUMBERS", NUMBER_RE)):
        if name in namespace:
            namespace[name] = pattern
    vocab = {
        "SPOKEN_NUMBERS": "sıfır iki üç dört beş altı yedi sekiz dokuz on yirmi otuz kırk elli altmış yetmiş seksen doksan yüz bin milyon milyar yarım çeyrek ikiye üçe",
        "MONEY_WORDS": "lira tl kuruş dolar euro avro yüzde gelir kâr kar maaş kira bütçe ücret maliyet",
        "STAKES": "dur bırak bırakın asla yanlış hata hatalar kayıp kaybettim kaybettik kaybetmek kaybediyorsunuz kaybediyorsun kaybediyor maliyet boşa başarısız kimse değil yok hayır olmadan sorun risk tehlike uyarı pişman gizli gerçek ücretsiz ücretli ödedim ödedik kurtardım kazandım kazandık tasarruf önce sonra ama sadece tek bırakmayın beklemeyin",
        "IMPERATIVES": "dur bırak bırakın kullan kullanın kaydet kaydedin dene deneyin oku okuyun yaz yazın gönder gönderin başla başlayın kontrol durdur durdurun asla",
        "STOPWORDS": "ve veya ama bir bu şu o ile için de da mi mı mu mü ben sen siz biz onlar benim senin sizin bizim gibi kadar daha çok en olan olarak ise ki hem her tüm ne neden nasıl",
    }
    for name, words in vocab.items():
        if name in namespace:
            namespace[name] = set(words.split())
    if "WEAK_OPENERS" in namespace:
        namespace["WEAK_OPENERS"] = ["merhaba", "selam", "arkadaşlar", "bugün", "şey", "yani", "bu videoda", "bu videomda", "öncelikle", "sizlere"]
    if "DEALBREAKERS" in namespace:
        namespace["DEALBREAKERS"] = [
            (re.compile(r"(?i)^\s*(?:kaydırmayı bırak|dur kaydırma)"), "Dikkat istemek yerine somut konuyla başlayın."),
            (re.compile(r"(?i)\b(?:bu videoda|bugünkü videoda|sizlere anlatacağım)\b"), "Video girişini çıkarıp doğrudan konuya girin."),
            (re.compile(r"(?i)^\s*(?:merhaba|selam|arkadaşlar)\b"), "Selamlaşmayı çıkarıp konuya girin."),
            (namespace["HASHTAG_RE"], "Açılışta hashtag kullanmayın."),
            (namespace["EMOJI_RE"], "Açılış metninde emoji yerine sözcük kullanın."),
        ]
        def address(text):
            low = lower(text)
            if re.search(r"\b(?:sen|siz|sana|size|senin|sizin|işletmeniz|müşteriniz)\b", low):
                return 100.0, "Doğrudan izleyiciye sesleniyor."
            tokens = WORD_RE.findall(low)
            if tokens and tokens[0] in namespace["IMPERATIVES"]:
                return 90.0, "Bir eylemle başlıyor."
            if re.search(r"\b(?:ben|biz|bana|bize|benim|bizim)\b", low):
                return 70.0, "Birinci kişi anlatımı."
            return 35.0, "Açık bir izleyici hitabı bulunamadı; Türkçe özne düşebilir."
        namespace["check_address"] = address
    if "ASKS" in namespace:
        namespace["ASKS"] = [(re.compile(p, re.I), label) for p, label in [
            (r"\b(?:yoruma|yorumlara)\s+[\wÇĞİÖŞÜçğıöşü]+\s+yaz\w*|\byorum\s+(?:yaz|yap|bırak)\w*", "yorum yaz"),
            (r"\b(?:dm|mesaj|whatsapp)\b.{0,35}\b(?:yaz|gönder|ulaş)\w*", "mesaj gönder"),
            (r"\bkayde[td]\w*", "kaydet"), (r"\bpaylaş\w*", "paylaş"),
            (r"\btakip\s+et\w*", "takip et"), (r"\b(?:bio|biyografi|profil)\w*\s+(?:link|bağlantı)\w*", "profil bağlantısı"),
            (r"\b(?:kaydır|dokun|tıkla)\w*", "kaydır veya dokun"),
            (r"\b(?:sizce|sence|hangisi|ne düşünüyorsun|ne düşünüyorsunuz)\b", "soruyu yanıtla"),
        ]]
        namespace["HASHTAG_RE"] = re.compile(r"(?:^|\s)(#\w+)", re.UNICODE)
        namespace["FILLER_TAGS"] = namespace["FILLER_TAGS"] | {"#keşfet", "#kesfet", "#takip", "#beğeni", "#beğen"}
    if "PRONOUNS" in namespace:
        namespace["PRONOUNS"] = re.compile(r"\b(?:ben|biz|sen|siz|benim|bizim|senin|sizin|bana|bize|sana|size)\b", re.I)
        def voice(text, lex):
            # Turkish does not use English contractions; omit that English check.
            tells = sum(len(re.findall(s["regex"], text, re.MULTILINE)) for s in lex["structures"])
            return max(0.0, 100.0 - tells * 22), f"{tells} kalıp yapı; Türkçe ekler ve düşen özneler nedeniyle zamir/kısaltma puanı kullanılmadı."
        namespace["check_voice"] = voice
    if "LEX" in namespace:
        namespace["LEX"] = str(Path(namespace["HERE"]) / "slop.tr.json")
    if "HOOKS" in namespace:
        namespace["HOOKS"] = str(Path(namespace["HERE"]).parent / "ig-reel" / "hooks.tr.json")


def print_tr_report(tool, data, out=None):
    """Turkish summaries, preserving stable JSON fields and source text verbatim.

    Upstream detail strings intentionally remain in English for compatibility;
    Turkish workflows interpret them. No undocumented automatic translation.
    """
    import sys
    out = out or sys.stdout
    if tool == "hookscore":
        print("AÇILIŞ DEĞERLENDİRMESİ (sezgisel; izlenme tahmini değildir)", file=out)
        for row in data:
            print(f"{row['score']:.1f}/100 | {row['hook']}", file=out)
            print(f"  En düşük ölçüt: {row['weakest']}", file=out)
            for flag in row["flags"]:
                print(f"  - {flag}", file=out)
    elif tool == "beats":
        print(f"SAHNE SÜRELERİ | {data['total_words']} sözcük | yaklaşık {data['total_seconds']} sn | {data['wpm']} sözcük/dk", file=out)
        for row in data["beats"]:
            print(f"{row['start']:5.1f} - {row['start']+row['dur']:5.1f} sn | {row['text']}", file=out)
            if row["flags"]:
                print("  Süre uyarısı: satırı veya görseli bölün.", file=out)
        print("Süreler tahminidir. Ayrıntılı teknik notlar: --json", file=out)
    elif tool == "caption":
        print(f"AÇIKLAMA KONTROLÜ | {data['characters']} karakter | {len(data['hashtags'])} hashtag | {len(data['asks'])} çağrı", file=out)
        print(f"Yaklaşık görünen bölüm ({data['truncate_at']} karakter):\n{data['visible']}", file=out)
        for row in data["checks"]:
            print(f"{row['status']} | {row['check']} | {row['detail']}", file=out)
    elif tool == "detect":
        print("METİN ÜSLUBU KONTROLÜ (yazarın insan/AI olduğunu kanıtlamaz)", file=out)
        for row in data:
            print(f"{row['source']}: {row['human_score']:.1f}/100 | {row['verdict']}", file=out)
            for name, check in row["checks"].items():
                print(f"  {name}: {check['score']:.1f}", file=out)
    elif tool == "swipe":
        print(f"ÖRNEK ANALİZİ | {data['n']} Reels | {data['accounts']} hesap", file=out)
        for row in data["reels"]:
            mult = f"{row['outlier']:.1f}x" if row["outlier"] is not None else "?"
            print(f"{mult} | {row.get('account', '')} | {row['formula']} | {row['hook']}", file=out)
        print("Örneklem bulguları genellenemez; her satırın baseline_kind alanına bakın.", file=out)
