import requests
import os
import re
from bs4 import BeautifulSoup


class Podcast:
    def __init__(self, name, rss_feed_url, custom_download_dir=None):
        self.name = name
        self.rss_feed_url = rss_feed_url

        # Use the custom download directory if provided, otherwise use the "Downloads" folder.
        if custom_download_dir:
            self.download_directory = custom_download_dir
        else:
            self.download_directory = os.path.join(os.path.expanduser("~"), name)

        print("Attempting to create directory:", self.download_directory)
        if not os.path.exists(self.download_directory):
            os.makedirs(self.download_directory)
            print("Directory successfully created!")
        else:
            print("Successfully created directory!")

    def retrieve_items(self, limit=None):
        podcast_page = requests.get(self.rss_feed_url)
        soup = BeautifulSoup(podcast_page.text, 'xml')
        return soup.find_all('item')[:limit]

    def search_items(self, search_term, limit=None):
        matched_podcasts_list = []
        items = self.retrieve_items()
        for podcast in items:
            if re.search(search_term, podcast.find('description').text, re.I):
                matched_podcasts_list.append(podcast)

        return matched_podcasts_list[:limit]
