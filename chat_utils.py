import os
import requests
from groq import Groq
from googlesearch import search
from bs4 import BeautifulSoup

# Set your Groq API Key
groq_api_key = "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"
client = Groq(api_key=groq_api_key)

class ChatUtils:
    @staticmethod
    def chat_with_user(user_input, context="career"):
        """
        First agent: Generates an initial response to the user
        """
        content_prompt = ""
        if context == "career":
            content_prompt = (
                f"This is the user's input about career development. "
                f"Here is their question: {user_input}. "
                "Write a motivating, friendly answer in less than 20 words, and then write: "
                "'I will search the internet for useful info...' at the end."
            )
        else:  # health context
            content_prompt = (
                f"This is the user's input about occupational health. "
                f"Here is their question: {user_input}. "
                "Write a supportive, caring answer in less than 20 words, and then write: "
                "'I will search the internet for helpful advice...' at the end."
            )
            
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": content_prompt}],
            model="qwen-2.5-coder-32b",
        )
        return chat_completion.choices[0].message.content

    @staticmethod
    def generate_search_query(user_input, context="career"):
        """
        Second agent: Generates an appropriate search query based on user input
        """
        context_prompt = "career development" if context == "career" else "occupational health"
        prompt = (
            f"Generate a concise and effective Google search query related to {context_prompt} "
            f"for the following question: {user_input}. "
            "Return only the query, no explanation."
        )
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="qwen-2.5-coder-32b",
        )
        return chat_completion.choices[0].message.content.strip()

    @staticmethod
    def get_page_snippet(url):
        """
        Helper: Fetches and extracts useful content from a web page
        """
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(resp.text, "html.parser")
            title = soup.title.string.strip() if soup.title else ""
            paragraphs = soup.find_all("p")
            content = " ".join(p.text for p in paragraphs[:3])  # Get first few paragraphs
            return f"Title: {title}\nSnippet: {content[:400]}\n"
        except Exception as e:
            return f"Failed to fetch {url}: {e}\n"

    @staticmethod
    def retrieve_information(search_query):
        """
        Agent 2.5: Retrieves information from web search results
        """
        try:
            results = list(search(search_query, num_results=3))
            all_info = ""
            for url in results:
                snippet = ChatUtils.get_page_snippet(url)
                all_info += f"{snippet}\n"
            return all_info
        except Exception as e:
            return f"Error retrieving information: {e}"

    @staticmethod
    def contextualize_information(info, user_input, context="career"):
        """
        Third agent: Contextualizes the retrieved information for the user
        """
        context_prompt = ""
        if context == "career":
            context_prompt = (
                f"You are a career development specialist helping a user who asked: "
                f'"{user_input}"\n\n'
                f"You searched online and found this content:\n{info}\n\n"
                f"Now extract useful, clear, data-driven insights. Don't just summarize. "
                f"Give a helpful response (under 150 words) that is:\n"
                f"- Professional and encouraging\n"
                f"- Actionable with specific steps\n"
                f"- Knowledgeable but accessible\n"
                f"Write in Arabic as the user speaks Arabic."
            )
        else:  # health context
            context_prompt = (
                f"You are an occupational health specialist helping a user who asked: "
                f'"{user_input}"\n\n'
                f"You searched online and found this content:\n{info}\n\n"
                f"Now extract useful, clear, health-focused insights. Don't just summarize. "
                f"Give a supportive response (under 150 words) that is:\n"
                f"- Caring and empathetic\n"
                f"- Provides practical health advice\n"
                f"- Science-based but accessible\n"
                f"Write in Arabic as the user speaks Arabic."
            )
            
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": context_prompt}],
            model="qwen-2.5-coder-32b",
        )
        return chat_completion.choices[0].message.content.strip()

    @staticmethod
    def process_chat(user_input, context="career"):
        """
        Main processing function that orchestrates the chat flow
        """
        try:
            # Initial response
            initial_response = ChatUtils.chat_with_user(user_input, context)
            
            # Generate search query
            search_query = ChatUtils.generate_search_query(user_input, context)
            
            # Retrieve information
            raw_info = ChatUtils.retrieve_information(search_query)
            
            # Contextualize information
            final_response = ChatUtils.contextualize_information(raw_info, user_input, context)
            
            return final_response
        except Exception as e:
            if context == "career":
                return "عذراً، حدث خطأ أثناء معالجة طلبك. هل يمكنك إعادة صياغة سؤالك؟"
            else:
                return "عذراً، واجهنا مشكلة في الاستجابة لاستفسارك. هل يمكنك المحاولة مرة أخرى؟"