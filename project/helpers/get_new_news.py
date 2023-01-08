def get_new_articles_helper(new_articles, website) -> list[bool]:
    """A Incomplete but simpler Python implementation of 'get_rowstoupdate'
    SQL function.
    This function will return a mask with True value only in the component
    corresponding to a new item not existing in the database.
    """

    old_articles = website.articles
    old_urls = [old_news.url for old_news in old_articles]
    return [new_article["link"] not in old_urls for new_article in new_articles]
