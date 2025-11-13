# Comprehensive Requirements Document for Advanced News Analysis System (ARAS) - Free Edition
**Version:** 2.0 - Free
**Date:** 2025-11-12

## Table of Contents
1. [Project Introduction](#project-introduction)
2. [High-Level Objectives](#high-level-objectives)
3. [Scope of Coverage](#scope-of-coverage)
4. [System Architecture](#system-architecture)
5. [Main Modules](#main-modules)
6. [Data Models](#data-models)
7. [Key Features](#key-features)
8. [Technical Requirements - Free](#technical-requirements---free)
9. [User Interface](#user-interface)
10. [Entities and KPIs](#entities-and-kpis)
11. [Advanced Analytics](#advanced-analytics)
12. [Project Phases](#project-phases)
13. [Success Criteria](#success-criteria)
14. [Limitations of Free Edition](#limitations-of-free-edition)
15. [Approvals](#approvals)
16. [ARAS Microservice Project Team Structure](#aras-microservice-project-team-structure)

---

## 1. Project Introduction

### 1.1 Name and Purpose
**System Name:** ARAS (Advanced News Analysis System) - Free Edition  
**Purpose:** To create a smart, fully free platform for monitoring, analyzing, and forecasting news developments.

### 1.2 Free Edition Limitations
- Exclusive use of open-source technologies
- No paid services (e.g., Google Analytics, paid cloud services)
- Focus on general news content analysis
- Full privacy compliance

---

## 2. High-Level Objectives

### 2.1 Operational Objectives - Free
- Process up to 50,000 news articles daily from 200+ sources
- Response time under 500ms for typical queries
- Over 90% accuracy in classification and entity extraction
- Support for 50+ concurrent users

### 2.2 Analytical Objectives
- Automatic detection of emerging trends
- Discovery of complex communication networks
- Analysis of event interdependencies
- Forecasting developments with over 80% accuracy

---

## 3. Scope of Coverage

### 3.1 Free News Sources
- **Domestic Agencies (RSS/Web):** IRNA, Tasnim, Fars, Mehr, ISNA, Borna, Javan, Mizan, Rooidad24, Entekhab, Etemad, Shargh
- **International Agencies (RSS):** BBC News, Reuters, AP News, Al Jazeera
- **Social Networks (Public APIs):** Twitter API (free), Telegram Public Channels

### 3.2 Subject Areas
- Politics (domestic & international)
- Economy (markets, trade, industry)
- Society (incidents, health, education)
- Culture & Arts
- Sports
- Science & Technology

---

## 4. System Architecture

### 4.1 Overall Architecture - Free
```
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Data Sources  │──▶│   Crawler     │──▶│   NLP Engine   │
│ (RSS/Web)     │   │  (Scrapy)     │   │ (spaCy/Hazm)   │
└───────────────┘    └───────────────┘    └───────────────┘
                           │                   │
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Web Interface │◀──│ Django/FastAPI│◀──│ Analytics      │
│   (React)     │    │               │    │ Engine        │
└───────────────┘    └───────────────┘    └───────────────┘
```

### 4.2 Main Components - Free
- **Web Crawler** (Scrapy-based)
- **NLP Processing Engine** (spaCy + Hazm)
- **Graph Analytics** (NetworkX)
- **Trend Detection** (Custom Algorithms)
- **Django/FastAPI Backend**
- **React Frontend**

---

## 5. Main Modules

### 5.1 Data Ingestion Module - Free
```python
class DataIngestion:
    - Scrapy Web Crawler
    - RSS Feed Reader
    - Simple Twitter API Client
    - Public Telegram Channel Parser
    - Data Normalization
    - Duplicate Detection (SimHash)
```

### 5.2 Text Processing Module - Free
```python
class TextProcessing:
    - Persian NLP: Hazm Library
    - English NLP: spaCy (small models)
    - Entity Recognition (Pattern-based)
    - Sentiment Analysis (Lexicon-based)
    - Topic Modeling (Gensim LDA)
    - Keyword Extraction (TF-IDF)
```

### 5.3 Graph Analysis Module - Free
```python
class GraphAnalysis:
    - NetworkX for Graph Analysis
    - Community Detection (Louvain)
    - Centrality Analysis
    - Basic Graph Algorithms
    - Custom Relationship Extraction
```

### 5.4 Trend Detection Module - Free
```python
class TrendDetection:
    - Statistical Trend Analysis
    - Burst Detection
    - Pattern Recognition
    - Simple Predictive Models
```

---

## 6. Data Models

### 6.1 Main Entity Models - Free
```sql
ENTITY_MODELS:
  NewsArticle:
    - id, title, content, summary
    - source, published_date, language
    - category, tags, sentiment_score
    - entities[], topics[]
  
  Entity:
    - id, name, type (PERSON, ORG, LOCATION)
    - aliases[], attributes{}
    - relationships[]
  
  Trend:
    - id, name, description
    - start_date, peak_date, end_date
    - confidence_score, impact_level
```

### 6.2 Graph Communication Models - Free
```sql
GRAPH_MODELS:
  Node:
    - node_id, node_type, properties{}
  
  Edge:
    - source_id, target_id, relationship_type
    - strength, confidence
```

---

## 7. Key Features

### 7.1 Real-Time Analysis - Free
- News monitoring every 30 minutes
- Simple alerts for important events
- Daily dashboard updates
- Detection of emerging trends in less than 6 hours

### 7.2 Historical Analysis
- News archive since launch
- Simple historical trend analysis
- Period comparison
- Detection of recurring patterns

### 7.3 Artificial Intelligence - Free
- Simple language models for Persian and English
- Classic machine learning algorithms
- Advanced statistical analysis
- Simple clustering

---

## 8. Technical Requirements - Free

### 8.1 Free Infrastructure
- **Servers:** Basic VPS: 4GB RAM, 2 cores (minimum), Ubuntu Server
- **Storage:**
  - Primary Database: PostgreSQL
  - Search: PostgreSQL Full-Text Search
  - Cache: Redis
  - File Storage: Local Storage
- **Network:**
  - Bandwidth: 100Mbps
  - Domain: Free or low-cost domain

### 8.2 Free Technologies
- **Backend:**
  - Python 3.9+
  - Django or FastAPI
  - Celery for async tasks
  - Redis for caching
- **Frontend:**
  - React 18+
  - Chart.js for charts
  - D3.js for advanced visualizations
- **Data Science:**
  - Scikit-learn
  - Gensim for topic modeling
  - Hazm for Persian
  - spaCy for English
  - NetworkX for graph analysis

### 8.3 Security - Free
- Simple authentication
- Data encryption
- Basic access management
- Protection against common attacks

---

## 9. User Interface

### 9.1 Main Dashboard - Free
- **Performance Summary:** Overall system statistics
- **Daily Trends:** Hot keywords
- **Communication Map:** Simple entity graph
- **News Analysis:** Basic reports

### 9.2 Free Visualizations
```typescript
VISUALIZATION_TYPES:
  - Basic Charts (Chart.js)
  - Simple Network Graphs (vis.js)
  - Word Clouds
  - Timeline Visualizations
```

---

## 10. Entities and KPIs

### 10.1 Extracted Entities - Free
```python
ENTITY_TYPES = {
    "PERSON": "Individuals",
    "ORGANIZATION": "Organizations",
    "LOCATION": "Geographical Locations",
    "DATE": "Dates"
}
```

### 10.2 Key Performance Indicators - Free
```python
KPI_METRICS = {
    "Daily processed news count",
    "Average classification accuracy",
    "System response time",
    "Detected trends count"
}
```

---

## 11. Advanced Analytics - Free

### 11.1 Simple Network Analysis
- Identification of key entities
- Discovery of basic relationships
- Simple centrality analysis

### 11.2 Basic Temporal Analysis
- Identification of seasonal patterns
- Simple trend analysis
- Basic forecasting

### 11.3 Simple Sentiment Analysis
- Measurement of general sentiment
- Tracking sentiment changes

---

## 12. Project Phases - Free

### 12.1 Phase 1: Core Foundation (2 months)
- [x] Architecture design
- [ ] Basic crawler implementation
- [ ] Database and models
- [ ] Simple user interface
- [ ] Initial text processing

### 12.2 Phase 2: Main Analytics (4 months)
- [ ] Simple graph analysis module
- [ ] Basic trend detection system
- [ ] Simple visualizations
- [ ] Automated reporting

### 12.3 Phase 3: Improvement & Optimization (6 months)
- [ ] Improved text processing accuracy
- [ ] Addition of advanced analytics
- [ ] Performance optimization
- [ ] API development

---

## 13. Success Criteria - Free

### 13.1 Technical Criteria
- Uptime over 95%
- Processing 50,000+ news articles daily
- Response time under 500ms
- Over 90% accuracy in main tasks

### 13.2 Analytical Criteria
- Identification of 80%+ major trends
- 75%+ accuracy in forecasts
- Discovery of 85%+ key relationships

---

## 14. Limitations of Free Edition

### 14.1 Technical Limitations
- Lower data processing compared to enterprise edition
- Lower accuracy in some analyses
- Slower processing speed
- Limited scalability

### 14.2 Analytical Limitations
- Simpler analyses
- Lower accuracy in predictions
- Limited reporting

---

## 15. Approvals

| Role           | Name | Date       | Signature |
|----------------|------|------------|-----------|
| Project Manager|      |            |           |
| Technical Architect|  |            |           |
| Product Manager|      |            |           |

---

## ARAS Microservice Project Team Structure

### 1. Technical Team

- **Software Architect**
  - Designs overall system architecture and integration
  - Ensures scalability, security, and maintainability

- **Backend Developers (Python, Django/FastAPI)**
  - Implement core services, APIs, and business logic
  - Integrate NLP, graph analytics, and data ingestion modules

- **Frontend Developers (React, D3.js, Chart.js)**
  - Build user interfaces and dashboards
  - Implement data visualizations and ensure UX quality

- **DevOps Engineer**
  - Manages deployment, CI/CD pipelines, server infrastructure
  - Ensures uptime, monitoring, and backups

- **Database Engineer**
  - Designs and optimizes PostgreSQL schemas
  - Implements full-text search and data archiving

- **Data Scientist / NLP Engineer**
  - Develops and tunes models for entity extraction, sentiment analysis, topic modeling
  - Integrates spaCy, Hazm, Gensim, and scikit-learn

- **Security Specialist**
  - Implements authentication, encryption, and access control
  - Conducts vulnerability assessments

- **QA Engineer / Tester**
  - Designs and runs test cases for all modules
  - Ensures system reliability and performance

### 2. Domain Experts

- **Senior Journalist / News Analyst**
  - Guides news source selection and content validation
  - Defines criteria for news relevance and quality

- **Economist**
  - Advises on economic indicators and analysis models
  - Validates financial news and trends

- **Political Analyst**
  - Provides expertise on political events and entities
  - Assists in trend detection and network analysis

- **Sociologist**
  - Advises on social trends, sentiment, and impact analysis

- **Cultural Expert**
  - Guides coverage of arts, culture, and related topics

- **Sports Analyst**
  - Supports sports news processing and trend identification

- **Science & Technology Expert**
  - Validates tech/science news and assists in topic modeling

### 3. Support & Management

- **Project Manager**
  - Coordinates team activities, timelines, and deliverables
  - Manages communication between technical and domain teams

- **Product Owner**
  - Defines product vision, requirements, and priorities
  - Ensures alignment with user needs and business goals

- **UI/UX Designer**
  - Designs user flows, wireframes, and visual assets

- **Documentation Specialist**
  - Prepares technical and user documentation

- **Legal Advisor**
  - Ensures compliance with privacy and copyright laws

---

#### Team Collaboration
- Regular cross-team meetings for requirements gathering, validation, and feedback
- Domain experts support software team with real-world data, validation, and scenario design
- Technical team ensures platform meets analytical and operational needs of all domains

---

This team structure ensures the ARAS microservice is robust, accurate, and relevant across all news domains, supported by top technical and subject-matter experts.

---

This document provides the comprehensive requirements for the fully free edition of the ARAS system, to be implemented using open-source and free technologies.
