from html.parser import HTMLParser
from pathlib import Path
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,s):self.parts.append(s)
for p in Path('sources').glob('*.html'):
 t=Text();t.feed(p.read_text());p.with_suffix('.txt').write_text(' '.join(' '.join(t.parts).split()))
