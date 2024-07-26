from fastapi import HTTPException
from pydantic import HttpUrl
from bs4 import BeautifulSoup
from langchain_community.document_loaders import AsyncHtmlLoader

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    def __init__(self, url: HttpUrl):
        self.url = url

    def __clean_html_content(
        self,
        html_content: str,
        wanted_tags: list[str],
        unwanted_tags: list[str] = ["script", "style"],
    ) -> str:
        soup = BeautifulSoup(html_content, "html.parser")
        for tag in unwanted_tags:
            for element in soup.find_all(tag):
                element.decompose()

        text_parts = []
        for tag in wanted_tags:
            elements = soup.find_all(tag)
            for element in elements:
                if tag == "a":
                    href = element.get("href")
                    text_parts.append(
                        f"{element.get_text()} ({href})" if href else element.get_text()
                    )
                else:
                    text_parts.append(element.get_text())

        content = " ".join(text_parts)
        lines = content.split("\n")
        stripped_lines = [line.strip() for line in lines]
        non_empty_lines = [line for line in stripped_lines if line]
        seen = set()
        deduped_lines = [
            line for line in non_empty_lines if not (line in seen or seen.add(line))
        ]
        cleaned_content = " ".join(deduped_lines)

        return cleaned_content

    async def scraping_with_langchain(
        self, wanted_tags: list[str] = ["h1", "h2", "h3", "span", "p", "a"]
    ) -> str:
        try:
            loader = AsyncHtmlLoader([self.url])
            docs = loader.load()
            cleaned_content = self.__clean_html_content(
                docs[0].page_content, wanted_tags
            )
            return cleaned_content
        except Exception as e:
            logger.error(f"Scraping Error: {e}")
            raise HTTPException(status_code=500, detail="Error scraping web content")