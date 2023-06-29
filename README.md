# pages-parser
Manager of page-parser tasks

#### ADT description


#### Build image and run app
    make run_app

#### Run project local without docker-compose
    poetry install
    poetry shell
    ./scripts/create-db-container.sh
    uvicorn run:app --reload
