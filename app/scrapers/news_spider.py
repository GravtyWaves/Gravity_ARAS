"""
ARAS News Scraper - Data Ingestion Service
RSS feeds + web scraping with Scrapy

Built by Elite Team - Backend Engineer (FastAPI Expert)
"""

import asyncio
import hashlib
import logging
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import feedparser
import yaml
from bs4 import BeautifulSoup
from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess

from app.schemas.news_schemas import NewsArticleCreate
from app.services.news_service import NewsService

logger = logging.getLogger(__name__)


class NewsSpider(Spider):
    """Scrapy spider for news article collection."""
    
    name = "aras_news_spider"
    
    def __init__(self, config_path: str = "config/news_sources.yaml", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = self._load_config(config_path)
        self.scraped_urls = set()
        self.articles = []
        
    def _load_config(self, config_path: str) -> Dict:
        """Load news sources configuration."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}
    
    def start_requests(self):
        """Generate initial requests from RSS feeds."""
        # Extract RSS feeds from config
        iranian_sources = self.config.get('iranian_english_sources', [])
        international_sources = self.config.get('international_english_sources', [])
        
        all_sources = iranian_sources + international_sources
        
        for source in all_sources:
            rss_feeds = source.get('rss_feeds', [])
            for feed_url in rss_feeds:
                yield Request(
                    url=feed_url,
                    callback=self.parse_rss,
                    meta={'source': source}
                )
    
    def parse_rss(self, response):
        """Parse RSS feed and extract article URLs."""
        source = response.meta['source']
        
        try:
            feed = feedparser.parse(response.text)
            
            for entry in feed.entries:
                article_url = entry.get('link')
                if not article_url or article_url in self.scraped_urls:
                    continue
                
                self.scraped_urls.add(article_url)
                
                # Extract metadata from RSS
                meta = {
                    'source': source,
                    'rss_title': entry.get('title', ''),
                    'rss_summary': entry.get('summary', ''),
                    'rss_published': entry.get('published', ''),
                }
                
                yield Request(
                    url=article_url,
                    callback=self.parse_article,
                    meta=meta
                )
                
        except Exception as e:
            logger.error(f"RSS parsing error for {response.url}: {e}")
    
    def parse_article(self, response):
        """Parse article page and extract content."""
        source = response.meta['source']
        
        try:
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Extract title (try multiple methods)
            title = (
                response.meta.get('rss_title') or
                self._extract_text(soup, ['h1', 'h2.title', 'article header h1']) or
                soup.title.string if soup.title else ''
            )
            
            # Extract content
            content = self._extract_content(soup)
            
            # Extract published date
            published_str = response.meta.get('rss_published', '')
            published_at = self._parse_date(published_str)
            
            # Create article
            if title and content:
                article = {
                    'title': title.strip(),
                    'content': content.strip(),
                    'url': response.url,
                    'source': source['name'],
                    'published_at': published_at,
                    'language': 'en',
                    'category': source.get('category', 'general'),
                }
                
                self.articles.append(article)
                logger.info(f"✓ Scraped: {title[:60]}...")
                
        except Exception as e:
            logger.error(f"Article parsing error for {response.url}: {e}")
    
    def _extract_text(self, soup: BeautifulSoup, selectors: List[str]) -> str:
        """Extract text using multiple selectors."""
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return ''
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract article content from page."""
        # Try common content selectors
        content_selectors = [
            'article .content',
            'article .article-content',
            'article .body',
            '.article-body',
            '.story-body',
            'div.content p',
            'article p',
        ]
        
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                paragraphs = [el.get_text(strip=True) for el in elements]
                content = '\n\n'.join(paragraphs)
                if len(content) > 100:  # Minimum content length
                    return content
        
        # Fallback: extract all paragraphs
        paragraphs = soup.find_all('p')
        content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs])
        return content
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string to datetime."""
        if not date_str:
            return datetime.now()
        
        try:
            # Try feedparser's time parsing
            from time import struct_time, mktime
            parsed = feedparser._parse_date(date_str)
            if isinstance(parsed, struct_time):
                return datetime.fromtimestamp(mktime(parsed))
        except:
            pass
        
        # Fallback to now
        return datetime.now()


class NewsIngestionService:
    """Service for automated news ingestion."""
    
    def __init__(self, config_path: str = "config/news_sources.yaml"):
        self.config_path = config_path
        self.news_service = NewsService()
    
    async def run_scraper(self) -> List[Dict]:
        """Run Scrapy spider and collect articles."""
        logger.info("Starting news scraper...")
        
        process = CrawlerProcess(settings={
            'USER_AGENT': 'ARAS News Aggregator v1.0.0',
            'ROBOTSTXT_OBEY': True,
            'CONCURRENT_REQUESTS': 5,
            'DOWNLOAD_DELAY': 2,
            'COOKIES_ENABLED': False,
            'TELNETCONSOLE_ENABLED': False,
            'LOG_LEVEL': 'WARNING',
        })
        
        spider = NewsSpider(config_path=self.config_path)
        
        # Run spider in separate thread (Scrapy uses Twisted reactor)
        def run_spider():
            process.crawl(spider)
            process.start()
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, run_spider)
        
        logger.info(f"✓ Scraped {len(spider.articles)} articles")
        return spider.articles
    
    async def ingest_articles(self, articles: List[Dict], db_session) -> Dict:
        """
        Ingest articles into database with duplicate detection.
        
        Returns:
            Dict with ingestion statistics
        """
        stats = {
            'total': len(articles),
            'inserted': 0,
            'duplicates': 0,
            'errors': 0
        }
        
        for article_data in articles:
            try:
                # Check for duplicates (URL-based)
                existing = await self.news_service.get_article_by_url(
                    article_data['url'],
                    db_session
                )
                
                if existing:
                    stats['duplicates'] += 1
                    continue
                
                # Create article
                article = NewsArticleCreate(**article_data)
                await self.news_service.create_article(article, db_session)
                
                stats['inserted'] += 1
                
            except Exception as e:
                logger.error(f"Ingestion error for {article_data.get('url')}: {e}")
                stats['errors'] += 1
        
        logger.info(
            f"Ingestion complete: {stats['inserted']} inserted, "
            f"{stats['duplicates']} duplicates, {stats['errors']} errors"
        )
        
        return stats
    
    async def run_full_ingestion(self, db_session) -> Dict:
        """
        Run complete ingestion pipeline:
        1. Scrape articles from RSS feeds
        2. Ingest into database with duplicate detection
        
        Returns:
            Dict with ingestion statistics
        """
        articles = await self.run_scraper()
        stats = await self.ingest_articles(articles, db_session)
        return stats


# Standalone script for manual testing
async def main():
    """Test scraper manually."""
    ingestion = NewsIngestionService()
    
    # Just run scraper (no DB)
    articles = await ingestion.run_scraper()
    
    print(f"\n✓ Scraped {len(articles)} articles:")
    for i, article in enumerate(articles[:5], 1):
        print(f"{i}. {article['title'][:70]}...")
        print(f"   Source: {article['source']}")
        print(f"   URL: {article['url'][:60]}...")
        print()


if __name__ == '__main__':
    asyncio.run(main())
