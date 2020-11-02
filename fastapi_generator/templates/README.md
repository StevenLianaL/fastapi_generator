# Document
## Flow
1. You need to configure the database in app/config.py. The default:
    
        DB_MODE = 'mysql'
        DB_HOST = '' if not DEBUG else 'localhost'
        DB_NAME = '' if not DEBUG else 'test'
        DB_USER = '' if not DEBUG else 'test'
        DB_PSWD = '' if not DEBUG else 'test'

2. Then you can run server:

        uvicorn app.main:app --reload