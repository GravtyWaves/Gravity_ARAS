"""
spaCy NLP Engine - Production v1.0.0
English-only NLP with en_core_web_sm model

Features:
- Sentiment Analysis (lexicon-based)
- Named Entity Recognition (spaCy NER)
- Keyword Extraction (TF-based frequency)
- Async execution support

Built by Elite Team - Dr. Sarah Chen (Chief Architect)
Strategic Decision: English-only content for better ML/NLP performance
"""

import asyncio
import logging
from typing import Dict, List, Optional, Tuple
from collections import Counter

import spacy
from spacy.language import Language

logger = logging.getLogger(__name__)

import asyncio
import logging
from typing import Dict, List, Optional, Tuple
from collections import Counter

import spacy
from spacy.language import Language

logger = logging.getLogger(__name__)


class SpacyNLPEngine:
    """Production spaCy NLP engine for English text analysis."""

    def __init__(self, model_name: str = "en_core_web_sm"):
        """
        Initialize spaCy NLP engine.
        
        Args:
            model_name: spaCy model (default: en_core_web_sm for v1.0.0)
        """
        self.model_name = model_name
        self.nlp: Optional[Language] = None
        self._model_loaded = False
        
        # Load model immediately
        self.load_model()

    def load_model(self) -> bool:
        """
        Load spaCy model.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self._model_loaded and self.nlp is not None:
            return True
            
        try:
            logger.info(f"Loading spaCy model: {self.model_name}")
            self.nlp = spacy.load(self.model_name)
            
            # Verify NER component
            if "ner" not in self.nlp.pipe_names:
                logger.warning("NER component not found in pipeline")
            
            self._model_loaded = True
            logger.info(f"✓ spaCy model {self.model_name} loaded successfully")
            return True
            
        except OSError as e:
            logger.error(f"Failed to load spaCy model {self.model_name}: {e}")
            logger.error(f"Run: python -m spacy download {self.model_name}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error loading spaCy: {e}")
            return False

    async def analyze_sentiment_async(self, text: str) -> Dict:
        """
        Async sentiment analysis wrapper.
        
        Args:
            text: Input text
            
        Returns:
            Sentiment analysis results
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.analyze_sentiment, text)

    def analyze_sentiment(self, text: str) -> Dict:
        """
        Lexicon-based sentiment analysis (v1.0.0 simplified).
        
        Args:
            text: Input text
            
        Returns:
            {
                "sentiment": "positive|negative|neutral",
                "polarity": float (-1 to 1),
                "confidence": float (0 to 1)
            }
        """
        if not self._model_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        try:
            doc = self.nlp(text.lower())
            
            # Lexicon-based sentiment analysis
            positive_words = {
                'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
                'positive', 'best', 'better', 'outstanding', 'superb', 'brilliant',
                'impressive', 'exceptional', 'remarkable', 'successful', 'victory',
                'win', 'progress', 'improvement', 'growth', 'benefit', 'advantage',
                'strong', 'leading', 'breakthrough', 'innovation', 'achievement'
            }
            
            negative_words = {
                'bad', 'terrible', 'awful', 'horrible', 'negative', 'worst',
                'worse', 'poor', 'disappointing', 'failure', 'failed', 'crisis',
                'problem', 'issue', 'concern', 'threat', 'risk', 'danger',
                'decline', 'decrease', 'loss', 'damage', 'harm', 'conflict',
                'weak', 'falling', 'collapse', 'corruption', 'scandal', 'violation'
            }
            
            # Count sentiment words
            pos_count = sum(1 for token in doc if token.text in positive_words)
            neg_count = sum(1 for token in doc if token.text in negative_words)
            total_words = len([t for t in doc if not t.is_stop and not t.is_punct])
            
            if total_words == 0:
                return {
                    "sentiment": "neutral",
                    "polarity": 0.0,
                    "confidence": 0.5
                }
            
            # Calculate polarity
            pos_ratio = pos_count / total_words
            neg_ratio = neg_count / total_words
            
            if pos_count > neg_count:
                sentiment = "positive"
                polarity = min(0.9, 0.5 + pos_ratio * 2)
                confidence = min(0.95, 0.6 + (pos_count - neg_count) / total_words)
            elif neg_count > pos_count:
                sentiment = "negative"
                polarity = max(-0.9, -0.5 - neg_ratio * 2)
                confidence = min(0.95, 0.6 + (neg_count - pos_count) / total_words)
            else:
                sentiment = "neutral"
                polarity = 0.0
                confidence = 0.7 if pos_count == 0 else 0.5
            
            return {
                "sentiment": sentiment,
                "polarity": round(polarity, 2),
                "confidence": round(confidence, 2)
            }
            
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return {
                "sentiment": "neutral",
                "polarity": 0.0,
                "confidence": 0.0
            }

    async def extract_entities_async(self, text: str) -> List[Dict]:
        """Async entity extraction wrapper."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.extract_entities, text)

    def extract_entities(self, text: str) -> List[Dict]:
        """
        Named Entity Recognition using spaCy.
        
        Extracts: PERSON, ORG, GPE (locations), DATE, MONEY, and more.
        
        Args:
            text: Input text
            
        Returns:
            List of entities with metadata
        """
        if not self._model_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        try:
            doc = self.nlp(text)
            
            entities = []
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "description": spacy.explain(ent.label_)
                })
            
            return entities
            
        except Exception as e:
            logger.error(f"Entity extraction error: {e}")
            return []

    async def extract_keywords_async(self, text: str, top_n: int = 10) -> List[Tuple[str, float]]:
        """Async keyword extraction wrapper."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.extract_keywords, text, top_n)

    def extract_keywords(self, text: str, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Extract top keywords using TF-IDF and POS filtering.
        
        Args:
            text: Input text
            top_n: Number of keywords to extract
            
        Returns:
            List of (keyword, score) tuples
        """
        if not self._model_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        try:
            doc = self.nlp(text)
            
            # Filter tokens: keep nouns, proper nouns, adjectives
            # Exclude stop words and punctuation
            keywords = [
                token.lemma_.lower()
                for token in doc
                if (token.pos_ in ["NOUN", "PROPN", "ADJ"] and
                    not token.is_stop and
                    not token.is_punct and
                    len(token.text) > 2)
            ]
            
            # Count frequency
            keyword_freq = Counter(keywords)
            
            # Get top N
            top_keywords = keyword_freq.most_common(top_n)
            
            # Normalize scores
            if top_keywords:
                max_freq = top_keywords[0][1]
                return [(kw, freq / max_freq) for kw, freq in top_keywords]
            
            return []
            
        except Exception as e:
            logger.error(f"Keyword extraction error: {e}")
            return []

    async def summarize_async(self, text: str, ratio: float = 0.3) -> str:
        """Async text summarization wrapper."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.summarize, text, ratio)

    def summarize(self, text: str, ratio: float = 0.3) -> str:
        """
        Extractive summarization using sentence scoring.
        
        Args:
            text: Input text
            ratio: Ratio of sentences to keep (0.0 to 1.0)
            
        Returns:
            Summarized text
        """
        if not self._model_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        try:
            doc = self.nlp(text)
            
            # Extract sentences
            sentences = list(doc.sents)
            
            if len(sentences) <= 2:
                return text  # Too short to summarize
            
            # Score sentences based on word frequency
            word_freq = Counter()
            for token in doc:
                if not token.is_stop and not token.is_punct:
                    word_freq[token.lemma_.lower()] += 1
            
            # Normalize frequencies
            max_freq = max(word_freq.values()) if word_freq else 1
            for word in word_freq:
                word_freq[word] /= max_freq
            
            # Score sentences
            sentence_scores = {}
            for sent in sentences:
                score = 0
                word_count = 0
                for token in sent:
                    if token.lemma_.lower() in word_freq:
                        score += word_freq[token.lemma_.lower()]
                        word_count += 1
                
                if word_count > 0:
                    sentence_scores[sent] = score / word_count
            
            # Select top sentences
            num_sentences = max(1, int(len(sentences) * ratio))
            top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
            
            # Sort by original order
            summary_sentences = sorted([sent for sent, score in top_sentences], key=lambda x: x.start)
            
            return " ".join([sent.text.strip() for sent in summary_sentences])
            
        except Exception as e:
            logger.error(f"Summarization error: {e}")
            return text

    async def analyze_topics_async(self, texts: List[str], num_topics: int = 5) -> List[List[str]]:
        """
        Async wrapper for simple keyword-based topic extraction.
        
        Note: Advanced LDA removed for v1.0.0 simplicity
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.analyze_topics, texts, num_topics)

    def analyze_topics(self, texts: List[str], num_topics: int = 5) -> List[List[str]]:
        """
        Simple topic extraction using keyword frequency (v1.0.0 simplified).
        
        Args:
            texts: List of documents
            num_topics: Number of topics to extract
            
        Returns:
            List of topics, each represented by top keywords
        """
        if not texts:
            return []
        
        try:
            # Extract all keywords from all texts
            all_keywords = []
            for text in texts:
                keywords = self.extract_keywords(text, top_n=20)
                all_keywords.extend([kw for kw, score in keywords])
            
            # Count keyword frequency across documents
            keyword_freq = Counter(all_keywords)
            
            # Get most common keywords
            common_keywords = keyword_freq.most_common(num_topics * 5)
            
            # Create topic clusters (simplified)
            topics = []
            for i in range(min(num_topics, len(common_keywords) // 5)):
                topic_words = [kw for kw, freq in common_keywords[i*5:(i+1)*5]]
                if topic_words:
                    topics.append(topic_words)
            
            return topics
            
        except Exception as e:
            logger.error(f"Topic extraction error: {e}")
            return []

    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._model_loaded


# Global instance
_nlp_engine: Optional[SpacyNLPEngine] = None


def get_nlp_engine() -> SpacyNLPEngine:
    """
    Get global NLP engine instance (singleton).
    
    Returns:
        SpacyNLPEngine instance
    """
    global _nlp_engine
    
    if _nlp_engine is None:
        _nlp_engine = SpacyNLPEngine()
        _nlp_engine.load_model()
    
    return _nlp_engine
