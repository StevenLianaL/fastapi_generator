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
    python -m fastapi_generator.main with orm
    # run fastapi app
    uvicorn app.main:app --reload

    
    
## Version
- 0.1.2
    - write main app project files
- 0.1.1
    - generate with orm
- 0.1
    - generate base app: can run it!
- 0.0.2 
    - create main app files 
- 0.0.1
    - only create app/main.py