import logging
import json
from livekit.agents import llm
from openai import OpenAI
import os
from cerebras.cloud.sdk import Cerebras

logger = logging.getLogger("function-calling-demo")
logger.setLevel(logging.INFO)


class AssistantFnc(llm.FunctionContext):
    def __init__(self, llm_instance: llm.LLM):
        super().__init__()
        self.llm = llm_instance
        self._meditation_schedule = {}

    @property
    def meditation_schedule(self):
        return self._meditation_schedule

    @llm.ai_callable(description="Build a guided meditation session")
    async def build_guided_meditation_session(self, length: int, topic: str) -> str:
        logger.info("Function called: Building guided meditation session with LLM")

        prompt = (
            f"Create a JSON script for a guided meditation session that lasts {length} minutes on the topic of {topic}. "
            "The JSON should have the following structure:\n"
            "{\n"
            '  "script": {\n'
            '    "lines": [\n'
            '      {"time": 0, "text": "Instruction 1"},\n'
            '      {"time": 20, "text": "Instruction 2"},\n'
            '      ...\n'
            '    ]\n'
            "  }\n"
            "}\n\n"
            "Ensure that the instructions are appropriate for a guided meditation and that the timing "
            "increments are logical (e.g., every 20 seconds). The total duration of all instructions "
            "should match the requested length. Return only JSON content."
        )

        while True:  # Will keep trying until success or non-400 error
            try:
                client = Cerebras(
                    api_key=os.environ.get("CEREBRAS_API_KEY"),
                )
                response = client.chat.completions.create(
                    model="llama3.1-70b",
                    messages=[
                        {"role": "system", "content": prompt}
                    ],
                    stream=False,
                    response_format={"type": "json_object"}
                )
               
                response_text = response.choices[0].message.content
                response_text = response_text.strip()
                script = json.loads(response_text)

                if "script" not in script or "lines" not in script["script"]:
                    raise ValueError("Invalid script structure generated by LLM.")
                logger.info(f"Meditation script generated by LLM.")
                self._meditation_schedule = script
                return "Created meditation script."

            except Exception as e:
                if hasattr(e, 'status_code') and e.status_code == 400:
                    logger.warning("Received 400 error, retrying...")
                    continue
                logger.error(f"An error occurred while generating the meditation script: {e}")
        
