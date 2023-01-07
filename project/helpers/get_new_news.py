def get_new_articles_helper(session, new_articles, website) -> list[bool]:
    """A Incomplete but simpler Python implementation of 'get_rowstoupdate'
       SQL function.
       This function will return a mask with True value only in the component
       corresponding to a new item not existing in the database.
    """

    old_articles = website.articles
    old_urls = [old_news.url for old_news in old_articles]
    return [True if new_article["link"] not in old_urls else False for new_article in new_articles]
