# Image Extractor Pro

**Advanced Web Crawler & Image Classification System**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/PySide6-6.5+-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

## 📋 Overview

Image Extractor Pro is a sophisticated desktop application for recursive website crawling, intelligent image extraction, and automated classification. Built with performance and scalability in mind, it employs multi-threading, advanced pattern recognition, and a modern Qt6 interface to deliver professional-grade image harvesting capabilities.

## 🏗️ Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                      Presentation Layer                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   MainWindow │  │   QThread   │  │  EnhancedProgressBar│  │
│  │   (Qt6 GUI)  │  │  Controllers│  │  (Real-time stats)  │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                      Business Layer                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Recursive │  │    Image    │  │  AllCategories      │  │
│  │   Crawler   │◄─┤  Classifier │──┤  Downloader         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                      Data Layer                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  ImageInfo  │  │   QSettings │  │   File I/O (JSON,   │  │
│  │   (Domain)  │  │ (Persistence)│  │    Reports, Images) │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Design Patterns

| Pattern | Implementation | Purpose |
|---------|---------------|---------|
| **MVC** | Qt Widgets + Controllers | Separation of concerns |
| **Observer** | Signal/Slot mechanism | Event-driven updates |
| **Strategy** | Classification algorithms | Pluggable categorization |
| **Thread Pool** | QThread + Queue | Concurrent processing |
| **Factory** | ImageInfo creation | Domain object generation |

## 🚀 Technical Specifications

### Performance Metrics
- **Concurrent Requests**: Up to 20 parallel connections
- **Memory Management**: Lazy loading with caching
- **Request Optimization**: Connection pooling & retry strategies
- **Processing Speed**: ~60 pages/minute (benchmarked)

### Classification Engine

```python
# Scoring Algorithm
- URL Pattern Matching: +5 points
- Keyword Detection: +3-4 points
- Dimension Analysis: +2-3 points
- Format Detection: +2-5 points
- Confidence Threshold: >10 points
```

### Supported Categories (25+)
- `logo`, `icone`, `banniere`, `produit`, `photo`, `avatar`
- `background`, `bouton`, `social`, `drapeau`, `illustration`
- `carte`, `qr-code`, `spinner`, `separateur`, `badge`
- `certification`, `publicite`, `infographie`, `emoji`
- `gif-anime`, `gif-statique`, `transparent`, `data-embed`

## 💻 Implementation Details

### Key Algorithms

**1. Recursive Crawling**
```python
def analyze_page(url, depth):
    # BFS-based traversal
    # Depth control with max_depth parameter
    # Subdomain filtering via domain matching
    # Link normalization with URL parsing
```

**2. Image Classification**
```python
def classify_image(img_info):
    # Multi-factor scoring system
    # Pattern-based regex matching
    # Content-type detection
    # Dimension heuristics
```

**3. Concurrent Downloading**
```python
# Thread-safe queue management
# Mutex-protected counters
# Progressive chunk streaming
# Error recovery with retries
```

## 🔧 Installation & Configuration

### Prerequisites
```bash
Python 3.8+
PySide6 >= 6.5
requests >= 2.28
beautifulsoup4 >= 4.11
Pillow >= 9.0
```

### Setup
```bash
# Clone repository
git clone https://github.com/your-repo/image-extractor-pro](https://github.com/omarbadrani/Image-Extractor-Pro
cd image-extractor-pro

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Configuration Parameters
```json
{
  "max_pages": 100,
  "max_depth": 5,
  "delay": 1,
  "timeout": 60,
  "include_subdomains": false,
  "classify_immediately": true
}
```

## 📊 Performance Optimization

### Memory Management
- Image data caching with LRU eviction
- Streaming downloads for large files
- Bounded queues for page processing
- Garbage collection optimization

### Network Optimization
```python
# Retry strategy
Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504]
)

# Connection pooling
HTTPAdapter(
    pool_connections=10,
    pool_maxsize=20
)
```

## 🔒 Security Features

- SSL/TLS verification
- Request timeout enforcement
- User-agent rotation
- Path traversal prevention
- Input sanitization
- Safe filename generation

## 📈 Scalability

The architecture supports:
- **Horizontal scaling**: Multiple instances
- **Vertical scaling**: Thread pool expansion
- **Distributed processing**: Queue-based distribution
- **Batch operations**: Bulk downloads with progress tracking

## 🧪 Testing

```bash
# Unit tests
pytest tests/ -v

# Performance benchmarks
python benchmarks/crawler_benchmark.py

# Classification accuracy
python tests/test_classifier.py --accuracy
```

## 📦 Output Formats

- **JSON**: Complete metadata export
- **TXT**: Human-readable reports
- **Images**: Organized in category folders
- **CSV**: Tabular data export (optional)

## 🎯 Use Cases

- **Digital Forensics**: Evidence collection
- **Content Migration**: Website to local archive
- **Data Analysis**: Image pattern recognition
- **Quality Assurance**: Visual asset verification
- **Research**: Web content categorization

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing`)
5. Open Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add type hints for new functions
- Include unit tests for critical features
- Document public APIs

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

*Built with Python, PySide6, and a passion for elegant software architecture*
