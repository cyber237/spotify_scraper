import typing as t

from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Playwright as SyncPlaywright


class PodCastNotFound(Exception):
    pass


class ErrorWhileFetchingPodCast(Exception):
    pass


class ErrorWhileExtractingPodcastData(Exception):
    pass


class SpotifyScraper:
    """
    This class exposes methods to scrape data from Spotify website.
    """

    HOSTURL = "https://open.spotify.com"
    NEWPAGECONFIG = {
        "viewport": {"width": 1470, "height": 956},
        "screen": {"width": 1470, "height": 956},
        "user_agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
        "geolocation": {"longitude": 42.254130, "latitude": -74.414519},
        "base_url": HOSTURL,
        "extra_http_headers": {
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    }

    @staticmethod
    def get_podcast(podcast: str) -> t.Dict[str, str]:
        """
        Scrape spotify website and return the podcast details.
        :param podcast: str: Spotify podcast id
        """
        with sync_playwright() as p:
            p: SyncPlaywright
            browser = p.chromium.launch()  # initialize the browser
            page = browser.new_page(
                **SpotifyScraper.NEWPAGECONFIG
            )  # create new page with provided configuration
            page.wait_for_load_state("domcontentloaded")

            try:
                response = page.goto(
                    f"{SpotifyScraper.HOSTURL}/show/{podcast}",
                    wait_until="domcontentloaded",
                )
            except Exception as e:
                browser.close()
                raise ErrorWhileFetchingPodCast(e)

            if response.status == 404:
                browser.close()
                raise PodCastNotFound("Podcast not found")
            if response.status >= 400 and response.status < 600:
                browser.close()
                raise ErrorWhileFetchingPodCast(
                    f"Error while fetching podcast: {response.status}"
                )

            # Extract the show title, rating and followers from the page
            try:
                ratings_wrapper = page.query_selector(
                    "div[data-testid='rating-and-topics'] button:first-child"
                )
                data = {
                    "title": page.query_selector(
                        "h1[data-testid='showTitle']"
                    ).inner_text(),
                    "overall_rating": ratings_wrapper.query_selector(
                        "span:first-child"
                    ).inner_text(),
                    "total_number_of_ratings": ratings_wrapper.query_selector(
                        "span:last-child"
                    )
                    .inner_text()
                    .lstrip("(")
                    .rstrip(")"),
                }
            except Exception as e:
                browser.close()
                raise ErrorWhileExtractingPodcastData()

            browser.close()

        return data
