# financial-QA

Simple API service to use GPT and FMP data to answer financial questions

## How to use it?

1. Have docker on your machine
2. Set API keys by duplicating the `.test.env` file and renaming it to `.env`
3. Build docker image using command `make build`
4. Start the FastAPI service by running `make run`
5. Once the api service starts, you can access it at `localhost:8000/docs` to use swagger docs.


## How it works?
- It uses prompt to ask GPT what api it should use to answer the following question.
- GPT provides a structured output the way we want it to be.
    - Current limitation is asking one question about one stock at a time, prompt can be modified to handle multiple question and stock at the same time.
- Once we have api to use and how to use it like query params etc., we execute the api request and get the financial data.
- The financial data is then fed again to GPT with the initial question to answer the question asked.

> Note: I haven't perfectly tested the docker-compose, since I run WSL2, there was some network issue. Feel free to directly run api service using command `poetry run uvicorn app:app --reload`