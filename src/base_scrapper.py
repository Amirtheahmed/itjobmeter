import json
from abc import ABC, abstractmethod

import requests
from requests import Session, Response

from src.logger import setup_logger

logger = setup_logger()


class BaseScraper(ABC):
    """
    Abstract base class for all scraper classes.
    """

    def __init__(self, proxy_manager):
        super().__init__()
        self.proxy_manager = proxy_manager

    @abstractmethod
    def scrape(self):
        """
        Method to perform the scraping action.
        This must be overridden by all subclasses.

        :return: A dictionary with the scraped data.
        """
        pass

    def http_get(self, session, url, proxied=False):
        if proxied is True:
            proxy = self.proxy_manager.get_proxy()
            try:
                if proxy is not None:
                    proxies = {"http": proxy, "https": proxy}
                    response = session.get(url, proxies=proxies)
                else:
                    response = session.get(url)

                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if proxied:
                    logger.error(f"Request failed using proxy {proxy}: {e}")
                else:
                    logger.error(f"Request failed: {e}")
        else:
            return session.get(url)

    def http_post(self, session: Session, url: str, body: dict, headers: dict, proxied: bool = False) -> Response:
        """
        Perform post request with data

        :param session:
        :param url:
        :param body:
        :param proxied:
        :return:
        """
        body = json.dumps(body)
        if proxied is True:
            proxy = self.proxy_manager.get_proxy()
            try:
                if proxy is not None:
                    proxies = {"http": proxy, "https": proxy}
                    response = session.post(url, data=body, headers=headers, proxies=proxies)
                else:
                    response = session.post(url, data=body, headers=headers)

                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if proxied:
                    logger.error(f"Request failed using proxy {proxy}: {e}")
                else:
                    logger.error(f"Request failed: {e}")
        else:
            return session.post(url, data=body, headers=headers)

