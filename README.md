This is just some demo code for learning and testing.

Source of code is documented at the top of each source file.

This was just something I whipped together in a weekend and is very rough.

Go to smart_scrapy/smart_scrapy/spiders/smart_spider.py and add in the allowed_domains and start_urls.

```bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
scrapy crawl Smart
python main.py
python whoost_tutorial.py
```
## What does all of this do?

* Scrape data from a website domain.
* Sanitizes each page for content only using dragnet.
* Summarizes each article.
* Grab the top 10 topics of each article using gensim/nltk/spacy.
* Create a processed output csv using pandas.
* Use whoosh to index and search the processed csv.

## What do I hope from this?
Maybe I can eventually turn it into a personalized rss feed for myself and others.
It's also good practice for me to keep up with modern tutorials for ML stuff as ML work for me has been slow.
All while kubernetes/devops work has been up. 