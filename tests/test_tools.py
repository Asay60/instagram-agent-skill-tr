import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
# Keep Windows child-process streams deterministic even without -X utf8.
os.environ['PYTHONUTF8'] = '1'


def module(skill, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'skills' / skill / f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ToolTests(unittest.TestCase):
    def test_unicode_words_and_turkish_casing(self):
        hook = module('ig-reel', 'hookscore')
        hook.configure_locale(vars(hook), 'tr')
        for s in ('Müşteri görüşmesi üç gün sürdü', unicodedata.normalize('NFD', 'Müşteri görüşmesi üç gün sürdü')):
            self.assertEqual(len(hook.words(s)), 5)
        self.assertEqual(hook.lower('İŞ IŞIK'), 'iş ışık')
        self.assertGreater(hook.check_specificity('Üç müşteri beş bin lira ödedi.')[0], 70)

    def test_turkish_hooks_are_not_treated_as_english(self):
        hook = module('ig-reel', 'hookscore')
        hook.configure_locale(vars(hook), 'tr')
        self.assertTrue(hook.run('Merhaba arkadaşlar bugün bir şey anlatacağım')[3])
        self.assertEqual(hook.check_address('Siz bu üç hatayı yapıyor musunuz?')[0], 100)
        self.assertGreater(hook.check_stakes('Bu hata bize 5.000 TL kaybettirdi.')[0], 20)

    def test_language_configuration_can_be_reset(self):
        hook = module('ig-reel', 'hookscore')
        hook.configure_locale(vars(hook), 'tr')
        hook.configure_locale(vars(hook), 'en')
        self.assertEqual(hook.check_address('Your next three proposals')[0], 100)
        self.assertTrue(hook.run('Hey guys today I want to talk')[3])

    def test_turkish_timing_and_invalid_rates(self):
        beat = module('ig-reel', 'beats')
        beat.configure_locale(vars(beat), 'tr')
        result = beat.analyse('Müşteri görüşmesi üç gün sürdü', wpm=60)
        self.assertEqual(result['total_words'], 5)
        self.assertEqual(result['total_seconds'], 5)
        for speed in (0, -1):
            with self.assertRaises(ValueError):
                beat.analyse('Test metni', wpm=speed)

    def test_caption_turkish_hashtags_and_cta(self):
        cap = module('ig-caption', 'caption')
        cap.configure_locale(vars(cap), 'tr')
        result = cap.analyse('3 adımı inceleyin.\nYoruma TEKLİF yazın.\n#müşteri #satış')
        self.assertEqual(result['hashtags'], ['#müşteri', '#satış'])
        self.assertEqual(result['asks'], ['yorum yaz'])
        self.assertEqual(cap.analyse('Size WhatsApp üzerinden mesaj gönderin.')['asks'], ['mesaj gönder'])
        self.assertEqual(cap.analyse('İŞ AKIŞI', keywords=['iş akışı'])['checks'][-1]['status'], 'PASS')

    def test_caption_multiple_ctas_and_configurable_tag_budget(self):
        cap = module('ig-caption', 'caption')
        cap.configure_locale(vars(cap), 'tr')
        result = cap.analyse('Kaydedin ve paylaşın. #bir #iki #üç', hashtag_limit=2)
        self.assertEqual(len(result['asks']), 2)
        self.assertEqual(next(c for c in result['checks'] if c['check']=='HASHTAGS')['status'], 'FAIL')

    def test_cleaning_preserves_meaningful_unicode_urls_and_email(self):
        human = module('ig-human', 'humanize')
        human.configure_locale(vars(human), 'tr')
        lex = human.load_lexicon(human.LEX)
        text = 'İş süreçleri 👨‍👩‍👧‍👦 🏳️‍🌈 https://örnek.com/iş?x=1 a@örnek.com görün\u200bmez'
        cleaned, _ = human.humanize(text, lex)
        self.assertIn('👨‍👩‍👧‍👦', cleaned)
        self.assertIn('🏳️‍🌈', cleaned)
        self.assertIn('https://örnek.com/iş?x=1', cleaned)
        self.assertIn('a@örnek.com', cleaned)
        self.assertNotIn('görün\u200bmez', cleaned)
        self.assertIn('İş süreçleri', cleaned)

    def test_turkish_cleaning_and_style_do_not_require_contractions(self):
        human = module('ig-human', 'humanize')
        human.configure_locale(vars(human), 'tr')
        cleaned, report = human.humanize('Merhaba. günümüzün hızla değişen dünyasında işi inceleyin.', human.load_lexicon(human.LEX))
        self.assertIn('Bugün işi', cleaned)
        self.assertTrue(report['lexical'])
        detect = module('ig-human', 'detect')
        detect.configure_locale(vars(detect), 'tr')
        lex = json.loads(Path(detect.LEX).read_text(encoding="utf-8"))
        score, detail = detect.check_voice('Teklifleri listede tutuyoruz. Sonraki görüşmeyi tarihlendiriyoruz.', lex)
        self.assertEqual(score, 100)

    def test_swipe_math_provenance_and_turkish_classification(self):
        swipe = module('ig-viral', 'swipe')
        swipe.configure_locale(vars(swipe), 'tr')
        formulas = swipe.load_formulas(swipe.HOOKS)
        data = swipe.analyse([{'account':'@example','followers':4000,'median':1000,'views':5000,'hook':'Kimse bu hatayı söylemiyor.','url':'https://example.test/reel'}], formulas)
        row = data['reels'][0]
        self.assertEqual(row['outlier'], 5)
        self.assertEqual(row['baseline_kind'], 'account median')
        self.assertEqual(row['formula_id'], 3)
        self.assertEqual(row['url'], 'https://example.test/reel')

    def test_swipe_rejects_ambiguous_abbreviations(self):
        swipe = module('ig-viral', 'swipe')
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'data.tsv'
            p.write_text('account\tviews\thook\n@x\t4.5K\tTest',encoding='utf-8')
            with self.assertRaises(ValueError):
                swipe.read_rows(str(p))

    def test_all_json_and_skill_frontmatter(self):
        for p in ROOT.rglob('*.json'):
            if '.git' not in p.parts:
                json.loads(p.read_text(encoding="utf-8"))
        skills = sorted((ROOT/'skills').glob('ig-*'))
        self.assertEqual(len(skills), 13)
        for p in skills:
            text = (p/'SKILL.md').read_text(encoding="utf-8")
            self.assertTrue(text.startswith('---\nname: '+p.name+'\ndescription: >-\n'))
            for lang in ('tr','en'):
                self.assertTrue((p/'references'/f'workflow.{lang}.md').is_file())
            self.assertNotIn('~/.claude/instagram', text)
            ui = (p/'agents/openai.yaml').read_text(encoding="utf-8")
            self.assertIn('$'+p.name, ui)
        h = json.loads((ROOT/'skills/ig-reel/hooks.tr.json').read_text(encoding="utf-8"))
        self.assertEqual(len(h['hooks']), 26)
        for row in h['hooks']:
            re.compile(row['match'], re.I)
        rubric=json.loads((ROOT/'skills/ig-profile/rubric.tr.json').read_text(encoding="utf-8"))
        self.assertEqual(sum(row['points'] for row in rubric['items']), 100)

    def test_cli_from_other_cwd_both_languages(self):
        tools = [('ig-reel','hookscore','Siz üç müşteri kaybettiniz.','Your three clients lost $500.'),
                 ('ig-reel','beats','Üç müşteri sizi bekliyor.','Three clients are waiting.'),
                 ('ig-caption','caption','3 teklif. Kaydedin.','3 proposals. Save this.'),
                 ('ig-human','humanize','Türkçe metin.','English text.'),
                 ('ig-human','detect','Türkçe metin.','English text.'),
                 ('ig-viral','swipe','account\tmedian\tviews\thook\n@a\t100\t500\tKimse söylemiyor.', 'account\tmedian\tviews\thook\n@a\t100\t500\tNobody tells you this.')]
        with tempfile.TemporaryDirectory() as cwd:
            for skill, name, tr, en in tools:
                for lang, sample in [('tr',tr),('en',en)]:
                    result = subprocess.run([sys.executable, str(ROOT/'skills'/skill/f'{name}.py'), '-', '--lang',lang,'--json'], input=sample, text=True,encoding='utf-8', capture_output=True, cwd=cwd)
                    self.assertIn(result.returncode, (0,1), (name,lang,result.stderr))
                    json.loads(result.stdout)

    def test_swipe_can_write_local_filename(self):
        with tempfile.TemporaryDirectory() as cwd:
            result = subprocess.run([sys.executable,str(ROOT/'skills/ig-viral/swipe.py'),'-','--lang','tr','--out','swipe.md','--json'], input='account\tmedian\tviews\thook\n@a\t100\t500\tKimse söylemiyor.',text=True,encoding='utf-8',capture_output=True,cwd=cwd)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertTrue((Path(cwd)/'swipe.md').is_file())

    def test_installer_collision_backup_and_installed_tools(self):
        with tempfile.TemporaryDirectory() as d:
            dest=Path(d)/'skills'
            command=[sys.executable,str(ROOT/'scripts/install.py'),'--dest',str(dest)]
            first=subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(first.returncode,0,first.stderr)
            existing=dest/'ig-reel/SKILL.md'
            original=existing.read_text(encoding="utf-8")
            existing.write_text('custom',encoding='utf-8')
            self.assertEqual(subprocess.run(command,capture_output=True).returncode,2)
            self.assertEqual(existing.read_text(encoding="utf-8"),'custom')
            result=subprocess.run(command+['--overwrite'],capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(existing.read_text(encoding="utf-8"),original)
            self.assertEqual(len(list((Path(d)/'instagram-agent-backups').glob('*/ig-reel/SKILL.md'))),1)
            run=subprocess.run([sys.executable,str(dest/'ig-reel/hookscore.py'),'--lang','tr','--hook','Üç müşteri beş bin lira ödedi.','--json'],capture_output=True,text=True,encoding='utf-8',cwd=d)
            json.loads(run.stdout)


if __name__=='__main__':
    unittest.main()
