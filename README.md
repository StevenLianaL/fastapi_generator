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
- databases
## Command
    # generate main app
    fastapi main
    # generate main app with orm
    fastapi orm db_host db_name db_user db_pswd
    # only generate orm
    fastapi orm --only db_host db_name db_user db_pswd
    fastapi orm localhost test test test
    fastapi orm --mode t
    # generate sub app
    fastapi sub app-name
    # generate api from sub app / if app not exist, create it.
    fastapi api app-name api-name 
    # run fastapi app
    uvicorn app.main:app --reload
    


    
    
## Version
- 0.5.0
  - update more tortoise orm
  - use more template code
- 0.4.0
  - support tortoise orm with mode t
- 0.3.7 
    - add param is_only_orm
- 0.3.6
    - add orm generate
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