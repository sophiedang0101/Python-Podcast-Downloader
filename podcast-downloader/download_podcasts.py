from podcast import Podcast
import dateutil.parser
import requests
import re
import os


def get_episodes_metadata(podcast_items):
    episode_links = [podcast.find('enclosure')['url'] for podcast in podcast_items]
    episode_titles = [podcast.find('title').text for podcast in podcast_items]
    episode_release_dates = [parse_date(podcast.find('pubDate').text) for podcast in podcast_items]
    return list(zip(episode_links, episode_titles, episode_release_dates))


def parse_date(date):
    return dateutil.parser.parse(date).strftime('%b-%d-%Y')


def get_mp3_file(url):
    # It redirects the url before you get the actual file
    redirect_url = requests.get(url).url
    file = requests.get(redirect_url)
    return file


def save_mp3_file(file, file_path):
    with open(file_path, 'wb') as f:
        f.write(file.content)


def simplify_title(title):
    file_name = re.sub(r'[%/&!@#\*\$\?\+\^\\.\\\\]', '', title)[:100]
    return file_name


if __name__ == '__main__':
    podcast_list = []
    ongoing = True

    print("\n--- Downloading podcasts... ---\n")
    while ongoing:
        podcast_name = input("Please enter the podcast name:")
        rss_feed_link = input("Please enter the podcast's rss feed link:")
        download_dir = input("Please enter a directory you want to download the podcasts into:")

        if download_dir:
            # If a custom download directory is specified, use it
            podcast_list.append(Podcast(podcast_name, rss_feed_link, custom_download_dir=download_dir))
        else:
            # If no custom directory is specified, use the "Downloads" folder
            podcast_list.append(Podcast(podcast_name, rss_feed_link,
                                        custom_download_dir=os.path.join(os.path.expanduser("~"), "Downloads")))

        response = input("Do you want to add another podcast? Enter 'yes' or 'no': ").lower()
        if response == 'no':
            ongoing = False
        else:
            continue

    search_term = input("Enter the search term you want to use: ")

    for podcast in podcast_list:
        podcast_items = podcast.search_items(search_term, limit=3)
        episodes_metadata = get_episodes_metadata(podcast_items)
        for episode in episodes_metadata:
            url, title, release_date = episode
            simple_title = simplify_title(title)

            # Create a subdirectory for each podcast
            podcast_subdirectory = os.path.join(podcast.download_directory, podcast.name)
            if not os.path.exists(podcast_subdirectory):
                os.makedirs(podcast_subdirectory)

            # Include podcast name in the filename and store in the subdirectory
            file_path = os.path.join(podcast_subdirectory, f'{simple_title}.mp3')

            file = get_mp3_file(url)
            save_mp3_file(file, file_path)
            print(file_path, "saved")
