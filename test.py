from pytube import Search
s = Search('Жалолиддин Ахмадалиев')

keys = s.results[0].__dict__
print(keys['watch_url'])
print(keys['_title'])
