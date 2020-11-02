from bs4 import BeautifulSoup
import requests
from colorama import Fore
from collections import defaultdict

# Official source names are:
# attackontitanmanga.com -> AoT
# mangelo.com -> Mangelo
# zeroscans.com & leviatanscans.com -> ZeroLeviatan
# mangaeffect.com -> Effect
# manhuaplus.com -> Plus
# readmng.com -> ReadMng
# mangadex.org -> MangaDex


# Each list within the mangas list has the following parameters: Name, Link, Source, Latest Chapter Read
mangas = [['Attack on Titan', 'https://attackontitanmanga.com/', 'AoT', 134],
          ['Solo Leveling', 'https://manganelo.com/manga/pn918005', 'Mangelo', 125],
          ['Tales of Demons and Gods', 'https://manganelo.com/manga/hyer5231574354229', 'Mangelo', 299.1],
          ['The Great Mage Returns After 4000 Years', 'https://manganelo.com/manga/go922760', 'Mangelo', 55],
          ['Second Life Ranker', 'https://zeroscans.com/comics/188504-second-life-ranker', 'ZeroLeviatan', 68],
          ['I am the Sorcerer King', 'https://leviatanscans.com/comics/i-am-the-sorcerer-king', 'ZeroLeviatan', 114],
          ['Descent of the Demonic Master', 'https://mangaeffect.com/manga/the-descent-of-the-demonic-master/', 'Effect', 71],
          ['Chronicles of Heavenly Demon', 'https://www.readmng.com/chronicles-of-heavenly-demon-3', 'ReadMng', 119],
          ['Iruma-Kun', 'https://www.readmng.com/mairimashita-iruma-kun', 'ReadMng', 166],
          ['Kingdom', 'https://www.readmng.com/kingdom', 'ReadMng', 659],
          ['Solo Auto Hunting', 'https://mangaeffect.com/manga/solo-auto-hunting/', 'Effect', 48],
          ["The Scholar's Reincarnation", 'https://www.readmng.com/the-scholars-reincarnation', 'ReadMng', 10],
          ["Demon Magic Emperor", 'https://manhuaplus.com/manga/demon-magic-emperor/', 'Plus', 1],
          ["Leveling Up, by Only Eating!", 'https://mangadex.org/title/48217/leveling-up-by-only-eating', 'MangaDex', 1],
          ]

# On most sites the desired element will be an anchor 'a' tag. However, this default dict allows us to specify exceptions
source_elements = defaultdict(lambda: 'a')
source_elements['ZeroLeviatan'] = 'span'
source_elements['ReadMng'] = 'span'

# Now the i_or_cls parameter of finder comes from this neat dictionary
# Now the i_or_cls parameter of finder comes from this neat dictionary
source_methods = {'AoT': 9, 'Mangelo': 'chapter-name text-nowrap', 'ZeroLeviatan': 'text-muted text-sm',
                  'Effect': 113, 'ReadMng': 'val', 'Plus': 104, 'MangaDex': 'text-truncate'}


# The i_or_cls parameter defined in source_methods will decide whether to find by index or class
# This process will use the typing of that same item to do so
def finder(parsed, el, i_or_cls):
    typ = type(i_or_cls)
    # If the source_methods dictionary a class, typ will have str type.
    # If the same dictionary holds index, typ will have int type
    if typ is str:
        tag = parsed.find(el, {'class': i_or_cls})
    elif typ is int:
        tag = parsed.findAll(el)[i_or_cls]
    else:
        tag = 'Error'
    output = tag.text.split()[-1].strip()
    try:
        float(output)
    except ValueError:
        output = tag.text.split()[-2].strip()
        try:
            float(output)
        except ValueError:
            output = tag.text.split()[-3].strip()
            try:
                float(output)
            except ValueError or IndexError:
                # Returns 0 if the tag it found does not hold the chapter number
                return "0"
    if el == 'a':
        return output, tag.attrs['href']
    return output


def a():
    for manga in mangas:
        webpage = requests.get(manga[1])
        soup = BeautifulSoup(webpage.content, 'html.parser')
        # Finder function enables one line to check any new properly defined list item (see line 7 comment)
        element = source_elements[manga[2]]
        if element != 'a':
            latest_chapter, link = finder(soup, element, source_methods[manga[2]]), manga[1]
        else:
            latest_chapter, link = finder(soup, element, source_methods[manga[2]])
            if link[:8] != "https://":
                link = manga[1] + link
        # The below if-else statement changes the color of the output when the latest chapter is greater than the latest read
        # If intending to access file through CLI, change color to "NEW " for the ~if~ and "" for the ~else~
        if float(latest_chapter) > manga[3]:
            color = Fore.LIGHTYELLOW_EX
            link_placeholder = link
        else:
            color = Fore.LIGHTBLUE_EX
            link_placeholder = ""
        print(color + f"{manga[0]}: {manga[3]} -> {latest_chapter} {Fore.CYAN} {link_placeholder}")


def n():
    for manga in mangas:
        soup = BeautifulSoup(requests.get(manga[1]).content, 'html.parser')
        # Finder function enables one line to check any new properly defined list item (see line 6 comment)
        element = source_elements[manga[2]]
        if element != 'a':
            latest_chapter, link = finder(soup, element, source_methods[manga[2]]), manga[1]
        else:
            latest_chapter, link = finder(soup, element, source_methods[manga[2]])
            if link[:8] != "https://":
                link = manga[1] + link
        # Only renders if there is a new chapter
        if float(latest_chapter) > manga[3]:
            print(Fore.LIGHTMAGENTA_EX + f"{manga[0]}: {manga[3]} -> {latest_chapter} Copy to see it:{Fore.CYAN} {link}")
