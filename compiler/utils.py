import time
from compiler.models import Test
from compiler.services.judge0 import execute_code, get_execution_result


LANGUAGE_IDS = {
    "python": 71,
    "javascript": 63,
    "cpp": 54,
    "java": 62
}

def run_tests(code, language, project):

    if language.compiler_name not in LANGUAGE_IDS:
        return {"status": False, "error": "Unsupported language"}
    
    tests = Test.objects.filter(project=project)

    output = None

    for test in tests:
        # output = test.input_data.replace('\\n', '\n').rstrip()
        # print(output)
        # print(test.output)
        # print(input_data)
        # print("end")
        formatted_input= test.input_data.replace('\\n', '\n')
        token = execute_code(code, LANGUAGE_IDS[language.compiler_name], formatted_input)
        time.sleep(2)  # Ждем завершения выполнения
        
        result = get_execution_result(token)

        output = result.get("stdout") or result.get("stderr")
        formatted_output= output.strip()

        if formatted_output != test.output:
            return {
                "status": False,
                "output": output
            }
    
    return {"status": True, "output": output or "Тестов нет"}

