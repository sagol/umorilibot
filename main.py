from sources import Sources
from stories import Stories

src = Sources('http://umorili.herokuapp.com')
stories = Stories(src)
stories.load()
#story = stories.get()[0]
#print(story.get().get('story'))

names = stories.get_names()
sites = list(set(names.values()))
site_names = list(names.keys())
print(sites)
print(site_names)
print(list([(x.get().get('site'), x.get().get('site_name')) for x in
    stories.get(num=1, sites=sites, site_names=site_names, random=True)]))

#print(list(set(names.values())))
