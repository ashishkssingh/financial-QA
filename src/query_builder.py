import logging
import os
from typing import Any
from openai import OpenAI
from src.api_call import get_financial_data
from src.answer_question import answer_question_using_data, get_api_information
from src.load_spec import read_api_spec

logger: logging.Logger = logging.getLogger("main")

client: OpenAI = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

api_document_spec = read_api_spec()

# question = """What was Tesla's revenue for Q2 2023?"""
# question = """what is the projected growth rate for Aritzia canada stock?"""
# question = """Pick three top stocks from canadian utilities industry which has historically given atleast 5% dividend returns"""


def get_answer(question: str):
    logger.info("question: %s", question)

    api_info = get_api_information(
        client=client, question=question, api_spec=api_document_spec
    )

    # Call the function
    fmp_output: dict[str, Any] = get_financial_data(api_info)

    logger.info("Example response: %s", fmp_output)

    answer = answer_question_using_data(
        client=client, question=question, data=fmp_output
    )

    logger.info("Final Answer curated by GPT: %s", answer)
    return answer
