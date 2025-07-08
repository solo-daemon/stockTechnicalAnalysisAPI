# stockTechnicalAnalysisAPI
An API which provides endpoint for stock information indicator updates

## User Model with rate-limiter

<img width="894" alt="Screenshot 2025-07-08 at 2 47 43 PM" src="https://github.com/user-attachments/assets/082c2016-a564-4ee1-bb48-8394e78464cd" />

## app-structure

```zsh
❯ tree
.
├── __init__.py
├── __pycache__
│   ├── __init__.cpython-311.pyc
│   ├── __init__.cpython-313.pyc
│   ├── main.cpython-311.pyc
│   └── main.cpython-313.pyc
├── api
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   ├── dependecies.cpython-311.pyc
│   │   ├── dependecies.cpython-313.pyc
│   │   ├── main.cpython-313.pyc
│   │   ├── routes.cpython-311.pyc
│   │   └── routes.cpython-313.pyc
│   ├── dependecies.py
│   └── routes.py
├── app.Dockerfile
├── app.env
├── auth
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   ├── dependencies.cpython-313.pyc
│   │   ├── routes.cpython-311.pyc
│   │   └── routes.cpython-313.pyc
│   ├── auth.env
│   ├── dependencies.py
│   └── routes.py
├── cache
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   ├── redis.cpython-311.pyc
│   │   └── redis.cpython-313.pyc
│   └── redis.py
├── data
│   └── stocks_ohlc_data.parquet
├── database
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   ├── dependecies.cpython-311.pyc
│   │   ├── dependecies.cpython-313.pyc
│   │   ├── postgres.cpython-311.pyc
│   │   └── postgres.cpython-313.pyc
│   ├── database.env
│   ├── dependecies.py
│   └── postgres.py
├── dependencies.py
├── main.py
├── middleware
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   ├── db_session.cpython-313.pyc
│   │   ├── rate_limiter.cpython-311.pyc
│   │   ├── rate_limiter.cpython-313.pyc
│   │   ├── url_cache.cpython-311.pyc
│   │   └── url_cache.cpython-313.pyc
│   ├── db_session.py
│   ├── rate_limiter.py
│   └── url_cache.py
├── models
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   ├── user.cpython-311.pyc
│   │   └── user.cpython-313.pyc
│   └── user.py
└── requirements.txt
```

## Images

<img width="717" alt="image" src="https://github.com/user-attachments/assets/4dd66e95-6f66-4ae2-8270-0f346061a657" />

## api-testing

<img width="923" alt="image" src="https://github.com/user-attachments/assets/929d10b0-72ef-4858-8e63-8cc165a652d4" />




