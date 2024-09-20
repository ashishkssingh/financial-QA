import datetime
import logging
from typing import Any
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

from src.api_call import convert_json_output_to_dict

logger = logging.getLogger("src.answer_question")

today = datetime.date.today()


def get_api_information(client: OpenAI, question: str, api_spec: str):
    completion: ChatCompletion = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {
                "role": "system",
                "content": "You are a knowledgeable assistant who helps me find the right API route and parameters based on specific documentation.",
            },
            {
                "role": "user",
                "content": f"""Today's date is {today} and the year is {today.year}. 
                What API call would you make to answer the following question: `{question}`. 
                Here is api documentation you should use for reference `{api_spec}`"""
                + """
                Important notes:
                - Use only the parameters listed in the documentation.
                - Omit the apiKey in query_params and ticker_symbol in path params.
                - Understand the question and tell me the date range I should filter the api output on, latest being today's date.
                - Use query params to filter by date if api document allows for filtering on date.
                - Use limit query param wherever possible to limit the data we pull from api, if its available in the documentation.
                - Provide only the JSON output, without any additional explanations or text, in the following format:
                    {
                        "ticker_symbol": "",
                        "url_without_ticker_symbol_or_query_params": "",
                        "path_parameters": {},
                        "query_params": {},
                        "use_ticker_or_not": true or false
                    }
                """,
            },
        ],
    )

    # Print the generated response
    which_api_to_use = completion.choices[0].message.content

    which_api_to_use_dict = convert_json_output_to_dict(which_api_to_use)

    logger.info("JSON: %s", which_api_to_use_dict)
    return which_api_to_use_dict


def answer_question_using_data(client: OpenAI, question: str, data: Any) -> str | None:
    completion = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant who answers questions using provided financial data.",
            },
            {
                "role": "user",
                "content": f"""{question}
                Use the following data to answer the question:
                {str(data)}
                """,
            },
        ],
    )
    answer: str | None = completion.choices[0].message.content
    return answer
