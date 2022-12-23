import feedparser
from bs4 import BeautifulSoup


def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    # p_tags = soup.find_all("p")
    # p_tags = soup
    # p_text = ' '.join([ptag.get_text() for ptag in p_tags])
    # return p_text.replace("\n", "")
    return soup.get_text(" ", strip=True, types=("p")).strip()[:256]


def get_news_rss(url: str):
    d = feedparser.parse(url)
    print(d.version)
    channel = d.feed
    entries = d.entries
    data = {
        "title_feed": channel["title"],
        "language": (channel["language"] if channel.has_key("language") else None),
        "link": channel["link"],
    }

    content_str = "content"
    if (entries[0]).has_key("content"):
        pass
    elif (entries[0]).has_key("dc_content"):
        content_str = "dc_content"
    elif (entries[0]).has_key("description"):
        content_str = "description"
    elif (entries[0]).has_key("summary"):
        content_str = "summary"
    else:
        raise Exception("no tiene ninguna de las keys disponibles")

    # if isinstance(entries[0][content_str], str):
    #    data.update({'entries': [{'title': entri['title'], 'link': entri['link'], "published": entri['published'], 'content': remove_tags(entri[content_str])} for entri in entries]})
    # elif isinstance(entries[0][content_str], list):
    #    data.update({'entries': [{'title': entri['title'], 'link': entri['link'], "published": entri['published'], 'content': remove_tags(entri[content_str][0]["value"])} for entri in entries]})

    data.update(
        {
            "entries": [
                {
                    "title": entri["title"],
                    "link": entri["link"],
                    "published": entri["published"],
                    "content": 0,
                }
                for entri in entries
            ]
        }
    )

    return data


if __name__ == "__main__":
    myurl = "https://www.tomshardware.com/feeds/all"
    myurl = "https://elchapuzasinformatico.com/feed/"
    myurl = "https://www.phoronix.com/rss.php"
    myurl = "https://feeds.feedburner.com/Hardwaresfera"
    myurl = "https://www.genbeta.com/feedburner.xml"
    myurl = "https://wccftech.com/feed/"
    myurl = "https://www.popsci.com/feed"
    print(get_news_rss(myurl))


# d.get(key, "empty")
# d.has_key("key")
