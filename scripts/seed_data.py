"""
Database Seed Data Generator
Creates realistic test data for development and testing

Built by Elite Team - Data Engineer & QA Lead
"""

import asyncio
import random
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.news_models import Edge, Entity, NewsArticle, Node, Trend


class SeedDataGenerator:
    """Generate realistic seed data for testing."""

    def __init__(self):
        self.persian_sources = [
            "BBC Persian",
            "Iran International",
            "RadioFarda",
            "VOA Persian",
            "Tasnim News",
            "IRNA",
            "Mehr News",
            "ISNA",
            "Khabar Online",
            "Entekhab",
        ]

        self.english_sources = [
            "BBC News",
            "CNN",
            "Reuters",
            "The Guardian",
            "New York Times",
            "Washington Post",
            "Al Jazeera English",
            "Bloomberg",
            "TechCrunch",
            "The Verge",
        ]

        self.categories = [
            "Politics",
            "Technology",
            "Science",
            "Business",
            "Sports",
            "Entertainment",
            "Health",
            "Environment",
            "Education",
            "Culture",
        ]

        self.persian_titles = [
            "توافق جدید در مذاکرات هسته‌ای",
            "پیشرفت چشمگیر در فناوری هوش مصنوعی",
            "کشف جدید در حوزه پزشکی",
            "تحولات اقتصادی در خاورمیانه",
            "مسابقات ورزشی بین‌المللی",
            "رویدادهای فرهنگی و هنری",
            "تغییرات آب و هوایی و محیط زیست",
            "نوآوری‌های تکنولوژیکی",
            "تحولات سیاسی منطقه",
            "پیشرفت در علوم فضایی",
        ]

        self.english_titles = [
            "Breakthrough in AI Research",
            "Global Climate Summit Results",
            "Major Tech Company Announces Innovation",
            "Political Developments in Middle East",
            "Economic Growth in Emerging Markets",
            "Medical Discovery Could Change Treatment",
            "Space Exploration Milestone Achieved",
            "International Sports Championship",
            "Cultural Heritage Conservation Project",
            "Renewable Energy Revolution",
        ]

        self.entity_types = ["PERSON", "ORG", "LOCATION", "DATE", "EVENT", "PRODUCT"]

        self.entity_names = {
            "PERSON": [
                "Dr. Sarah Johnson",
                "Mohammad Reza Ahmadi",
                "Prof. John Smith",
                "Fatima Al-Mansouri",
                "David Chen",
            ],
            "ORG": [
                "United Nations",
                "Google",
                "Microsoft",
                "Tehran University",
                "MIT",
                "WHO",
            ],
            "LOCATION": [
                "Tehran",
                "New York",
                "London",
                "Dubai",
                "Paris",
                "Tokyo",
                "Berlin",
            ],
            "EVENT": [
                "COP28",
                "World Economic Forum",
                "Olympic Games",
                "Nobel Prize",
                "Tech Summit",
            ],
            "PRODUCT": [
                "GPT-4",
                "iPhone 15",
                "Tesla Model 3",
                "COVID-19 Vaccine",
                "Quantum Computer",
            ],
        }

    def generate_persian_content(self, title: str) -> tuple[str, str]:
        """Generate Persian article content and summary."""
        content = f"""
در گزارش {title}، تحولات مهمی در این حوزه مشاهده شده است. کارشناسان معتقدند 
که این پیشرفت می‌تواند تاثیر قابل توجهی بر آینده داشته باشد.

بر اساس آخرین اطلاعات، این موضوع توجه بسیاری از فعالان حوزه را به خود جلب کرده 
و انتظار می‌رود در ماه‌های آینده شاهد تحولات بیشتری باشیم.

تحلیلگران بر این باورند که عوامل مختلفی در این رویداد نقش داشته‌اند و باید 
منتظر نتایج بلندمدت آن بود. این امر می‌تواند فرصت‌های جدیدی را فراهم آورد.

در نهایت، این گزارش نشان می‌دهد که همکاری‌های بین‌المللی و تلاش‌های مشترک 
می‌تواند به نتایج مثبتی منجر شود و راه را برای پیشرفت‌های آینده هموار کند.
        """.strip()

        summary = f"گزارشی در مورد {title} که به تحولات اخیر و چشم‌انداز آینده می‌پردازد."

        return content, summary

    def generate_english_content(self, title: str) -> tuple[str, str]:
        """Generate English article content and summary."""
        content = f"""
In a significant development, {title.lower()} marks an important milestone 
in this field. Experts suggest that this advancement could have far-reaching 
implications for the future.

According to latest reports, this development has attracted considerable 
attention from industry professionals and stakeholders. Further developments 
are expected in the coming months as the situation evolves.

Analysts believe that multiple factors have contributed to this outcome, and 
the long-term effects remain to be seen. This could potentially open up new 
opportunities and possibilities across various sectors.

The findings demonstrate that international cooperation and collaborative 
efforts can lead to positive outcomes, paving the way for future progress 
and innovation in this domain.
        """.strip()

        summary = f"A comprehensive report on {title.lower()} and its implications."

        return content, summary

    async def create_articles(self, session: AsyncSession, count: int = 100):
        """Create sample news articles."""
        articles = []
        persian_count = count // 2
        english_count = count - persian_count

        # Generate Persian articles
        for i in range(persian_count):
            title = random.choice(self.persian_titles)
            content, summary = self.generate_persian_content(title)
            published_date = datetime.now() - timedelta(days=random.randint(1, 90))

            article = NewsArticle(
                title=f"{title} - {i}",
                content=content,
                summary=summary,
                source=random.choice(self.persian_sources),
                published_date=published_date,
                language="fa",
                category=random.choice(self.categories),
                tags=[
                    random.choice(["سیاست", "فناوری", "علم", "اقتصاد", "فرهنگ"])
                    for _ in range(random.randint(2, 5))
                ],
                sentiment_score=round(random.uniform(-1.0, 1.0), 2),
                entities=[],
                topics=[],
                url=f"https://example.com/fa/article-{i}-{published_date.timestamp()}",
            )
            articles.append(article)

        # Generate English articles
        for i in range(english_count):
            title = random.choice(self.english_titles)
            content, summary = self.generate_english_content(title)
            published_date = datetime.now() - timedelta(days=random.randint(1, 90))

            article = NewsArticle(
                title=f"{title} - {i}",
                content=content,
                summary=summary,
                source=random.choice(self.english_sources),
                published_date=published_date,
                language="en",
                category=random.choice(self.categories),
                tags=[
                    random.choice(["politics", "tech", "science", "business", "culture"])
                    for _ in range(random.randint(2, 5))
                ],
                sentiment_score=round(random.uniform(-1.0, 1.0), 2),
                entities=[],
                topics=[],
                url=f"https://example.com/en/article-{i}-{published_date.timestamp()}",
            )
            articles.append(article)

        session.add_all(articles)
        await session.commit()
        print(f"✅ Created {len(articles)} articles ({persian_count} Persian, {english_count} English)")
        return articles

    async def create_entities(self, session: AsyncSession, count: int = 50):
        """Create sample entities."""
        entities = []

        for entity_type in self.entity_types:
            names = self.entity_names.get(
                entity_type, [f"{entity_type}_{i}" for i in range(10)]
            )
            for i in range(count // len(self.entity_types)):
                entity = Entity(
                    name=random.choice(names) + f" {i}",
                    type=entity_type,
                    aliases=[f"alias_{j}" for j in range(random.randint(1, 3))],
                    attributes={
                        "importance": random.choice(["high", "medium", "low"]),
                        "verified": random.choice([True, False]),
                    },
                    confidence_score=round(random.uniform(0.5, 1.0), 2),
                )
                entities.append(entity)

        session.add_all(entities)
        await session.commit()
        print(f"✅ Created {len(entities)} entities")
        return entities

    async def create_trends(self, session: AsyncSession, count: int = 20):
        """Create sample trends."""
        trends = []
        trend_names = [
            "AI Revolution",
            "Climate Action",
            "Digital Transformation",
            "Space Exploration",
            "Renewable Energy",
            "Quantum Computing",
            "Biotechnology",
            "Cybersecurity",
            "5G Networks",
            "Electric Vehicles",
            "Remote Work",
            "Cryptocurrency",
            "Virtual Reality",
            "Smart Cities",
            "Precision Medicine",
            "Edge Computing",
            "Green Technology",
            "Autonomous Vehicles",
            "Blockchain",
            "Metaverse",
        ]

        for i in range(count):
            start_date = datetime.now() - timedelta(days=random.randint(30, 180))
            peak_date = start_date + timedelta(days=random.randint(10, 60))
            end_date = peak_date + timedelta(days=random.randint(10, 90))

            trend = Trend(
                name=trend_names[i] if i < len(trend_names) else f"Trend {i}",
                description=f"Analysis of {trend_names[i] if i < len(trend_names) else f'Trend {i}'} and its impact",
                start_date=start_date,
                peak_date=peak_date,
                end_date=end_date if random.random() > 0.3 else None,
                confidence_score=round(random.uniform(0.6, 1.0), 2),
                impact_level=random.choice(["low", "medium", "high"]),
                keywords=[
                    f"keyword_{j}" for j in range(random.randint(3, 7))
                ],
            )
            trends.append(trend)

        session.add_all(trends)
        await session.commit()
        print(f"✅ Created {len(trends)} trends")
        return trends

    async def create_graph_data(
        self, session: AsyncSession, entities: list, articles: list
    ):
        """Create sample graph nodes and edges."""
        nodes = []
        edges = []

        # Create nodes from entities
        for entity in entities[:30]:  # Use first 30 entities
            node = Node(
                node_id=f"entity_{entity.id}",
                node_type=entity.type.lower(),
                properties={
                    "name": entity.name,
                    "confidence": entity.confidence_score,
                },
            )
            nodes.append(node)

        # Create nodes from articles
        for article in articles[:20]:  # Use first 20 articles
            node = Node(
                node_id=f"article_{article.id}",
                node_type="article",
                properties={
                    "title": article.title,
                    "category": article.category,
                },
            )
            nodes.append(node)

        session.add_all(nodes)
        await session.flush()

        # Create edges (relationships)
        for i in range(min(50, len(nodes) - 1)):
            source_node = random.choice(nodes)
            target_node = random.choice(nodes)

            if source_node.node_id != target_node.node_id:
                edge = Edge(
                    source_id=source_node.node_id,
                    target_id=target_node.node_id,
                    relationship_type=random.choice(
                        ["mentions", "related_to", "co_occurs", "references"]
                    ),
                    strength=round(random.uniform(0.3, 1.0), 2),
                    confidence=round(random.uniform(0.5, 1.0), 2),
                    properties={
                        "context": random.choice(["same_article", "same_topic", "same_time"])
                    },
                )
                edges.append(edge)

        session.add_all(edges)
        await session.commit()
        print(f"✅ Created {len(nodes)} graph nodes and {len(edges)} edges")

    async def seed_all(self):
        """Seed all data."""
        print("🌱 Starting database seeding...")

        engine = create_async_engine(settings.DATABASE_URL, echo=False)
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with async_session() as session:
            # Create articles
            articles = await self.create_articles(session, count=100)

            # Create entities
            entities = await self.create_entities(session, count=50)

            # Create trends
            trends = await self.create_trends(session, count=20)

            # Create graph data
            await self.create_graph_data(session, entities, articles)

        print("\n✅ Database seeding completed successfully!")
        print(f"📊 Summary:")
        print(f"   - Articles: 100 (50 Persian, 50 English)")
        print(f"   - Entities: 50")
        print(f"   - Trends: 20")
        print(f"   - Graph Nodes: ~50")
        print(f"   - Graph Edges: ~50")


async def main():
    """Main entry point."""
    generator = SeedDataGenerator()
    await generator.seed_all()


if __name__ == "__main__":
    asyncio.run(main())
