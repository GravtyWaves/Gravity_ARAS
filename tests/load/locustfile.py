"""
ARAS Load Testing with Locust
Test API performance under load

Built by Elite Team - QA Engineer (Testing Automation Expert)

Run:
    locust -f tests/load/locustfile.py --host=http://localhost:8000
    
Then open http://localhost:8089 and configure:
- Number of users: 100, 1000, or 10000
- Spawn rate: 10 users/second
"""

from locust import HttpUser, task, between
import random


class ARASUser(HttpUser):
    """Simulated ARAS API user."""
    
    # Wait 1-3 seconds between tasks
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when a user starts."""
        # Could authenticate here if needed
        pass
    
    @task(10)
    def health_check(self):
        """Test health endpoint (most frequent)."""
        self.client.get("/health")
    
    @task(5)
    def list_articles(self):
        """Test article listing."""
        params = {
            "skip": random.randint(0, 100),
            "limit": random.choice([10, 20, 50]),
        }
        self.client.get("/api/v1/articles/", params=params)
    
    @task(3)
    def search_articles(self):
        """Test full-text search."""
        search_terms = [
            "economy", "politics", "technology", "health",
            "Iran", "Middle East", "energy", "trade"
        ]
        params = {
            "query": random.choice(search_terms),
            "limit": 20,
        }
        self.client.get("/api/v1/articles/search", params=params)
    
    @task(2)
    def get_article(self):
        """Test single article retrieval."""
        # Assumes articles with IDs 1-100 exist
        article_id = random.randint(1, 100)
        self.client.get(f"/api/v1/articles/{article_id}")
    
    @task(2)
    def analyze_sentiment(self):
        """Test sentiment analysis endpoint."""
        texts = [
            "This is excellent news for the economy!",
            "The situation is deteriorating rapidly.",
            "Officials announced new policies today.",
            "Markets showed strong performance this week.",
            "Concerns remain about the ongoing crisis.",
        ]
        data = {
            "text": random.choice(texts),
            "language": "en"
        }
        self.client.post("/api/v1/analysis/sentiment", json=data)
    
    @task(2)
    def extract_entities(self):
        """Test entity extraction endpoint."""
        texts = [
            "President Biden met with Prime Minister Johnson in Washington.",
            "Apple announced new iPhone at the California headquarters.",
            "The European Union imposed sanctions on Russia.",
            "Amazon CEO Jeff Bezos visited the Seattle office.",
            "China and Iran signed a trade agreement worth $400 billion.",
        ]
        data = {
            "text": random.choice(texts),
            "language": "en"
        }
        self.client.post("/api/v1/analysis/entities", json=data)
    
    @task(1)
    def extract_topics(self):
        """Test topic extraction endpoint."""
        texts = [
            "Artificial intelligence and machine learning are transforming industries.",
            "Climate change poses significant risks to global food security.",
            "Cryptocurrency markets experienced high volatility this week.",
            "Renewable energy investments reached record levels.",
            "Healthcare systems face challenges from aging populations.",
        ]
        data = {
            "text": random.choice(texts),
            "language": "en"
        }
        self.client.post("/api/v1/analysis/topics", json=data)
    
    @task(1)
    def list_entities(self):
        """Test entity listing."""
        params = {
            "skip": 0,
            "limit": 20,
            "entity_type": random.choice(["PERSON", "ORG", "GPE"])
        }
        self.client.get("/api/v1/entities/", params=params)
    
    @task(1)
    def list_trends(self):
        """Test trends listing."""
        params = {
            "skip": 0,
            "limit": 10,
            "period": random.choice(["daily", "weekly", "monthly"])
        }
        self.client.get("/api/v1/trends/", params=params)


class StressTestUser(HttpUser):
    """Stress test user with more aggressive load."""
    
    wait_time = between(0.1, 0.5)  # Very short wait
    
    @task
    def rapid_fire_health(self):
        """Rapid health checks."""
        self.client.get("/health")
    
    @task
    def rapid_fire_search(self):
        """Rapid search requests."""
        self.client.get("/api/v1/articles/search?query=test&limit=10")


class ReadOnlyUser(HttpUser):
    """Read-only user for baseline performance."""
    
    wait_time = between(2, 5)
    
    @task(5)
    def health_check(self):
        self.client.get("/health")
    
    @task(3)
    def list_articles(self):
        self.client.get("/api/v1/articles/?skip=0&limit=20")
    
    @task(2)
    def search(self):
        self.client.get("/api/v1/articles/search?query=news&limit=10")
