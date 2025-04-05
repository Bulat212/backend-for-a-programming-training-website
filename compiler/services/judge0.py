# services/judge0.py
import requests

JUDGE0_URL = "https://judge0-ce.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": "1f22a27c68msh287a3885ca7c4ddp1dbe31jsn88340c7f029b",
    "Content-Type": "application/json"
}

def execute_code(code, language_id, input_data=""):
    # formatted_input = input_data.replace('\r\n', '\n').strip() if input_data else ""
    
    data = {
        "source_code": code,
        "language_id": language_id,
        "stdin": input_data,
        "cpu_time_limit": 5,  # Макс 5 секунд
        "memory_limit": 128000  # 128 MB
    }
    
    response = requests.post(
        f"{JUDGE0_URL}/submissions",
        json=data,
        headers=HEADERS
    )
    return response.json()["token"]  # ID выполнения

def get_execution_result(token):
    response = requests.get(
        f"{JUDGE0_URL}/submissions/{token}",
        headers=HEADERS
    )
    return response.json()

# Пример ответа:
# {
#   "stdout": "42\n",
#   "stderr": null,
#   "status": {"description": "Accepted"}
# }