# Document
## Description
- This project is used to quickly generate fastapi project.
## Flow for Main App
1. run main app command
2. config config.py db or set in environment
## Requirements
- python 3.8
- click
- pandas
## Command
    # generate main app
    fastapi main
    # run fastapi app
    uvicorn app.main:app --reload
    # generate sub app
    fastapi sub app-name
    # generate api from sub app / if app not exist, create it.
    fastapi api app-name api-name 

    
    
## Version
- 0.3.5
    - update command with click
- 0.3
    - generate api of sub app.
- 0.2.1
    - generate sub app with auto load api
- 0.2
    - generate sub app
- 0.1.3
    - auto load sub app
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