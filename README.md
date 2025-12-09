# Crypto Investor Dashboard

A personalized crypto investor dashboard that gets to know users through an onboarding quiz and displays daily AI-curated content tailored to their interests. Users can provide feedback (thumbs up/down) to help improve future recommendations.

## Features

- **User Authentication**: Secure JWT-based authentication with email/password
- **Onboarding Quiz**: Personalized setup to understand user preferences
- **Daily Dashboard**: Four customizable sections:
  - **Market News**: Latest cryptocurrency news from CryptoPanic API
  - **Coin Prices**: Real-time prices from CoinGecko API
  - **AI Insight**: Daily AI-generated insights using OpenRouter
  - **Fun Meme**: Random crypto memes
- **Feedback System**: Thumbs up/down voting on all content for future model improvements
- **Responsive Design**: Modern, clean UI that works on all devices

## Tech Stack

### Backend
- **Flask**: Python web framework
- **MongoDB**: NoSQL database (MongoDB Atlas)
- **JWT**: Token-based authentication
- **bcrypt**: Password hashing
- **External APIs**: CoinGecko, CryptoPanic, OpenRouter

### Frontend
- **React**: UI library
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **React Icons**: Icon library

## Project Structure

```
MoveoEx/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── config.py             # Configuration
│   │   ├── models.py             # MongoDB models
│   │   ├── utils.py              # Helper functions
│   │   ├── routes/               # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── dashboard.py
│   │   │   ├── preferences.py
│   │   │   └── feedback.py
│   │   └── services/             # External API integrations
│   │       ├── coingecko.py
│   │       ├── cryptopanic.py
│   │       ├── ai_service.py
│   │       └── meme_service.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── Procfile                  # Deployment config
│   ├── app.py                    # Production entry point
│   └── run.py                    # Development server
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── services/             # API services
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── .env.example
├── data/
│   └── memes.json                # Static meme data
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 16+ and npm
- MongoDB Atlas account (free tier) or local MongoDB
- OpenRouter API key (optional, for AI insights)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set:
   - `SECRET_KEY`: Random secret key for Flask
   - `JWT_SECRET_KEY`: Random secret key for JWT tokens
   - `MONGO_URI`: MongoDB connection string
   - `OPENROUTER_API_KEY`: Your OpenRouter API key (optional)

5. **Run development server**:
   ```bash
   python run.py
   ```
   
   Server runs on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set:
   - `REACT_APP_API_URL`: Backend API URL (default: `http://localhost:5000/api`)

4. **Run development server**:
   ```bash
   npm start
   ```
   
   App runs on `http://localhost:3000`

## API Documentation

### Authentication Endpoints

#### Register
- **POST** `/api/auth/register`
- **Body**: `{ "email": "user@example.com", "password": "password123", "name": "John Doe" }`
- **Response**: `{ "access_token": "...", "user": {...} }`

#### Login
- **POST** `/api/auth/login`
- **Body**: `{ "email": "user@example.com", "password": "password123" }`
- **Response**: `{ "access_token": "...", "user": {...} }`

#### Get Current User
- **GET** `/api/auth/me`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "user": {...} }`

### Dashboard Endpoints

#### Get Dashboard Data
- **GET** `/api/dashboard`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "dashboard": { "news": [...], "prices": [...], "ai_insight": {...}, "meme": {...} } }`

### User Preferences

#### Save Preferences
- **POST** `/api/user/preferences`
- **Headers**: `Authorization: Bearer <token>`
- **Body**: 
  ```json
  {
    "investor_type": "HODLer",
    "interested_assets": ["Bitcoin", "Ethereum"],
    "content_types": ["Market News", "Fun"]
  }
  ```

#### Get Preferences
- **GET** `/api/user/preferences`
- **Headers**: `Authorization: Bearer <token>`

### Feedback

#### Submit Feedback
- **POST** `/api/feedback`
- **Headers**: `Authorization: Bearer <token>`
- **Body**: 
  ```json
  {
    "content_type": "news",
    "content_hash": "...",
    "vote": 1
  }
  ```
- **Vote**: `1` for thumbs up, `-1` for thumbs down

## Deployment

### Backend Deployment (Render/Railway)

1. **Push code to GitHub**

2. **Create new service** on Render or Railway

3. **Configure environment variables**:
   - `SECRET_KEY`
   - `JWT_SECRET_KEY`
   - `MONGO_URI`
   - `OPENROUTER_API_KEY` (optional)

4. **Set build command**: `pip install -r requirements.txt`

5. **Set start command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`

### Frontend Deployment (Vercel/Netlify)

1. **Push code to GitHub**

2. **Import project** on Vercel or Netlify

3. **Configure environment variables**:
   - `REACT_APP_API_URL`: Your deployed backend URL

4. **Build settings**:
   - Build command: `npm run build`
   - Publish directory: `build`

### MongoDB Atlas Setup

1. **Create free cluster** on MongoDB Atlas

2. **Create database user**

3. **Whitelist IP addresses** (or use 0.0.0.0/0 for development)

4. **Get connection string** and add to backend `.env`

## Database Schema

### Users Collection
```json
{
  "_id": ObjectId,
  "email": "user@example.com",
  "password_hash": "bcrypt_hash",
  "name": "John Doe",
  "preferences": {
    "investor_type": "HODLer",
    "interested_assets": ["Bitcoin", "Ethereum"],
    "content_types": ["Market News", "Fun"],
    "created_at": ISODate
  },
  "created_at": ISODate,
  "updated_at": ISODate
}
```

### Feedback Collection
```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "content_type": "news|insight|meme|price",
  "content_hash": "sha256_hash",
  "vote": 1 | -1,
  "timestamp": ISODate
}
```

## Bonus: Training Process for Model Improvements

### Overview

The feedback system collects user votes (thumbs up/down) on all dashboard content. This data can be used to train recommendation models and improve content curation.

### Data Collection

1. **Feedback Storage**: All votes are stored in the `feedback` collection with:
   - User ID (for personalization)
   - Content type (news, insight, meme, price)
   - Content hash (unique identifier)
   - Vote value (1 or -1)
   - Timestamp

2. **Content Metadata**: Each content item includes:
   - Source information
   - User preferences at time of viewing
   - Content characteristics (topics, sentiment, etc.)

### Training Approach

#### 1. Feature Engineering

Extract features from feedback data:
- **User Features**: Investor type, preferred assets, content type preferences
- **Content Features**: Source, topic, sentiment, recency
- **Interaction Features**: Time of day, device type, session context

#### 2. Recommendation Model

**Collaborative Filtering**:
- Find users with similar preferences
- Recommend content liked by similar users
- Use matrix factorization (e.g., SVD, NMF)

**Content-Based Filtering**:
- Analyze content characteristics
- Match content to user preferences
- Use TF-IDF or embeddings for text content

**Hybrid Approach**:
- Combine collaborative and content-based methods
- Weight based on data availability
- Use ensemble methods for better accuracy

#### 3. Model Training Pipeline

```python
# Pseudocode for training pipeline

1. Data Collection
   - Aggregate feedback from MongoDB
   - Create user-content interaction matrix
   - Extract features

2. Data Preprocessing
   - Handle missing values
   - Normalize features
   - Split train/validation/test sets

3. Model Training
   - Train recommendation model (e.g., LightFM, Surprise)
   - Tune hyperparameters
   - Validate on test set

4. Model Evaluation
   - Precision@K, Recall@K
   - Mean Average Precision (MAP)
   - User satisfaction metrics

5. Model Deployment
   - Save model artifacts
   - Create inference API
   - A/B test new recommendations
```

#### 4. Continuous Learning

- **Online Learning**: Update model with new feedback in real-time
- **Retraining Schedule**: Retrain weekly/monthly with accumulated data
- **Feedback Loop**: Monitor recommendation quality and user engagement

### Implementation Suggestions

1. **Feature Store**: Store pre-computed features for fast model inference
2. **Model Registry**: Version and track model performance
3. **A/B Testing**: Test new recommendation strategies
4. **Monitoring**: Track recommendation quality metrics
5. **Cold Start Problem**: Use content-based recommendations for new users

### Example Training Script Structure

```python
# train_recommendation_model.py

from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from lightfm import LightFM
from lightfm.evaluation import precision_at_k

# 1. Load feedback data
client = MongoClient(MONGO_URI)
feedback = list(client.db.feedback.find())
users = list(client.db.users.find())

# 2. Build interaction matrix
# ... feature engineering ...

# 3. Train model
model = LightFM(loss='warp')
model.fit(train_interactions, epochs=30, num_threads=2)

# 4. Evaluate
precision = precision_at_k(model, test_interactions, k=10).mean()

# 5. Save model
import pickle
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
```

### Metrics to Track

- **Engagement Rate**: % of users who interact with recommendations
- **Click-Through Rate**: % of recommended content clicked
- **Feedback Sentiment**: Ratio of positive to negative feedback
- **Diversity**: Variety of content recommended
- **Coverage**: % of available content recommended

## Development Notes

### AI Tools Used

This project was developed with assistance from:
- **Cursor AI**: Code generation and refactoring
- **GitHub Copilot**: Code suggestions and autocomplete

### Key Design Decisions

1. **JWT Authentication**: Stateless, scalable authentication
2. **MongoDB**: Flexible schema for user preferences and feedback
3. **Service Layer**: Separated API integrations for maintainability
4. **Content Hashing**: SHA256 hashes for unique content identification
5. **Fallback Content**: Static fallbacks when APIs fail

## License

This project is created for educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
