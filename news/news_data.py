from news.bing_api import Bing
from news.gpt_author import story_writer, opinnion_id
from news.reader import Reader
import keys
import pandas as pd


def news_dataframe():
    # Get bing api key from keys file
    api_key = keys.bing_api_key

    # Start Bing API class
    bapi = Bing(api_key)

    # Get the 5 top trending topics right now
    topics = bapi.get_topics(n=5)

    # Iterate through each topic
    # Call reader
    read = Reader()

    # Instantiate variables
    headline, article, urls, img, dte, scrape_clean, scrape_errors, opinnions = [], [], [], [], [], [], [], []

    

    # Begin iterataions
    for i in topics:

        # Crete a dataframe for topic i
        df_topic_i = bapi.get_stories(i)

        if df_topic_i is None:
            pass

        else:

            # Collect urls, dates, and media
            headline.append(df_topic_i['name'].to_list())
            urls.append(df_topic_i['url'].to_list())
            img.append(df_topic_i['image_contentUrl'].to_list())
            dte.append(df_topic_i['datePublished'].to_list())

            # Collect scraped articles: _clean- "" for errors, _errors- includes error numbers
            fullStory_clean, fullStory_errors = [], []

            # Iterate through each url
            if df_topic_i is not None:
                for ii, r in df_topic_i.iterrows():

                    # Attempt scrape on article
                    out = read.choose_reader(r.url)

                    # Store stories and errors in varialbe
                    fullStory_errors.append(out)

                    # Remove errors for clean data
                    error1, error2 = "ERROR 01:", "ERROR 02:"
                    if error1 in out or error2 in out:
                        out = None
                    fullStory_clean.append(out)

                # Returns both clean and non clean scrape attempts
                scrape_clean.append(fullStory_clean), scrape_errors.append(fullStory_errors),

                # Tell ChatGPT to create a story based on the description
                gptStory_i = story_writer(df_topic_i['description'].to_list())
                article.append(gptStory_i)

                # Compare the non-opinnionated chatGPT story to scrapped stories
                opinnion = []

                for i in fullStory_clean:

                    # If the article scrapes correctly, get the opinnion
                    if i is not None:
                        out = opinnion_id(gptStory_i, i)
                        opinnion.append(out)

                    # If not give none
                    else:
                        out = None
                        opinnion.append(out)

                # Aggregate the opinion for the dataframe
                opinnions.append(opinnion)

            else:
                fullStory_clean.append(None)
                fullStory_errors.append(None)
                opinnions.append(None)

        # End the selenium session
        read.kill()


    # Create dataframe
    data = {'headlines': headline,
            'article': article,
            'urls': urls,
            'img': img,
            'dates': dte,
            'scrape_clean': scrape_clean,
            'scape_errors': scrape_errors,
            'opnnions_by_source': opinnions}

    # Deliver as a dataframe
    df = pd.DataFrame(data)
    return df
