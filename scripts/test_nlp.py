"""
Test NLP Service with real Iran news examples
"""

from app.services.nlp_service import get_nlp_service

# Sample Iranian news articles (English)
sample_articles = [
    {
        "title": "Iran's President Meets Chinese Foreign Minister in Tehran",
        "content": """Iran's President Ebrahim Raisi met with Chinese Foreign Minister Wang Yi in Tehran on Tuesday to discuss bilateral relations and regional cooperation. The meeting focused on expanding economic ties, particularly in the energy and infrastructure sectors. Both sides emphasized the strategic partnership between Iran and China, highlighting the 25-year cooperation agreement signed in 2021. They also exchanged views on the situation in the Middle East and the importance of multilateralism."""
    },
    {
        "title": "Tehran Stock Exchange Shows Strong Growth in Technology Sector",
        "content": """The Tehran Stock Exchange witnessed significant growth in technology stocks this week, with the TSE index rising by 3.5 percent. Companies in the software development and telecommunications sectors led the gains. Analysts attribute this growth to increased government investment in digital infrastructure and the expansion of 5G networks across major Iranian cities. The positive trend is expected to continue as more tech startups enter the market."""
    },
    {
        "title": "Iran Successfully Launches New Satellite into Orbit",
        "content": """Iran's space agency successfully launched a new communications satellite into orbit using the domestically-produced Simorgh carrier rocket. The satellite, named Pars-1, will provide telecommunications and internet services across the country. This achievement marks a significant milestone in Iran's space program despite international sanctions. The launch was praised by government officials as evidence of Iranian scientific capabilities."""
    }
]

def test_nlp_service():
    """Test NLP service with sample articles."""
    print("🚀 Testing ARAS NLP Service (English-First Approach)\n")
    print("=" * 80)
    
    nlp = get_nlp_service()
    
    for i, article in enumerate(sample_articles, 1):
        print(f"\n📰 ARTICLE {i}: {article['title']}")
        print("-" * 80)
        
        # Analyze article
        result = nlp.analyze_article(article['title'], article['content'])
        
        # Display entities
        print("\n🏷️  ENTITIES:")
        for entity_type, entities in result['entities'].items():
            if entities:
                print(f"  {entity_type}:")
                for ent in entities[:5]:  # Show first 5
                    print(f"    - {ent['text']}")
        
        # Display sentiment
        print(f"\n😊 SENTIMENT:")
        print(f"  Label: {result['sentiment']['sentiment']}")
        print(f"  Score: {result['sentiment']['score']}")
        print(f"  Confidence: {result['sentiment']['confidence']}")
        
        # Display keywords
        print(f"\n🔑 TOP KEYWORDS:")
        for kw in result['keywords'][:8]:
            print(f"  - {kw['keyword']} (freq: {kw['frequency']}, relevance: {kw['relevance']})")
        
        # Display topics
        print(f"\n📂 TOPICS: {', '.join(result['topics'])}")
        
        print("\n" + "=" * 80)

if __name__ == "__main__":
    test_nlp_service()
