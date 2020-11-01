# Document
## Description
- This project is used to quickly generate fastapi project.
## Flow for Main App
1. run main app command
2. config config.py db or set in environment
## Requirements
- python 3.8
## Command
    # generate main app
    python -m fastapi_generator.main
    # gen main app with orm
    pip install pandas orm
    python -m fastapi_generator.main -o 1
    # run fastapi app
    uvicorn app.main:app --reload

    
    
## Version
- 0.1
    - generate base app: can run it!
- 0.0.2 
    - create main app files 
- 0.0.1
    - only create app/main.py