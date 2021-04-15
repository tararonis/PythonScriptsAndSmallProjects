"""
Parse the pages("https://pcsmith.cccm.com/studies/russian?page="[63-89])
for valid links with high quality audio
and download audio files in multiprocesses
https://stackoverflow.com/questions/3044580/multiprocessing-vs-threading-python
https://stackoverflow.com/questions/18114285/what-are-the-differences-between-the-threading-and-multiprocessing-modules
"""
import os
import datetime
from multiprocessing import Pool
from bs4 import BeautifulSoup
import requests


def stopwhatch(func):
    """
    Decorator that measure time
    """

    def wrapper(*args):
        start = datetime.datetime.now()
        return_value = func(*args)
        total = datetime.datetime.now() - start
        print(
            f"{'#'*15}{str(func.__name__).upper()} processed in {total.seconds} seconds"
        )
        return return_value

    return wrapper


@stopwhatch
def get_links(start_end: tuple, url: str) -> dict:
    """Function that takes site url and pages that need to parse.
    Parse them for valid links with high quality audio and returns the dict with them.

    Args:
        start_end (tuple): range of pages
        url (str): site url

    Returns:
        dict: dictionary with links {id:link}. we need id to storage the downloading files in order.
    """
    audio_links = []
    for i in range(start_end[0], start_end[1] + 1):
        target_url = url + str(i)
        request = requests.get(target_url, allow_redirects=False)

        soup = BeautifulSoup(request.content, "lxml")
        links = soup.find_all("a")
        for link in links:
            #forbiden_words = ["Захария", "Малахии", "undefined", "pdf", "16.mp3"]
            if all(
                [
                    (
                        "media.pastorchuck" in str(link)
                    ),  # every downloading link have it in body
                    ("Захария" not in str(link)),  # first page contains audio files
                    ("Малахии" not in str(link)),  # from old testament
                    ("undefined" not in str(link)),  # and some "garbage" links
                    ("pdf" not in str(link)),
                    ("16.mp3" not in str(link)),
                ]
            ):  # low quality audio files

                audio_links.append(link.attrs["href"])
    dict_links = {i: audio_links[i] for i in range(0, len(audio_links))}
    return dict_links


def download_file(link: str):
    """
    Download audio file with provided link and storage it in the temp folder

    Args:
        link (str): link with audio file
    """
    name = f"{link[0]}_{link[1].split('/')[-1]}"
    path = os.path.join("/home/roman/MyFiles/!temp/new_testament/", name)

    if not os.path.exists(path):
        request = requests.get(link[1], allow_redirects=True)
        open(path, "wb").write(request.content)


@stopwhatch
def multiprocessing(links: dict):
    """Generate 15 processes and download audio files from
    provided dictionary with links

    Args:
        links ([dict]): dictionary with links {id:url}
    """
    pools = Pool(15)
    pools.map(download_file, links)


def main():
    """Entry poinit"""
    pages_start_end = (63, 89)
    parsed_site = "https://pcsmith.cccm.com/studies/russian?page="
    links = get_links(pages_start_end, parsed_site)
    multiprocessing(links.items())


if __name__ == "__main__":
    main()
