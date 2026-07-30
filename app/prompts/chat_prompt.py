from typing import List


class ChatPromptBuilder:

    @staticmethod
    def build(prompt: str) -> List[dict]:
        return [
            {
                "role": "system",
                "content": (
                    "You are an famous wedding planner in Kakinada Andhrapradesh. "
                    "Provide clear, concise, and technically accurate responses."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]