import requests

OLLAMA_URL = 'http://localhost:11434'

class OllamaError(Exception):
    pass


def call_ollama(prompt, model='llama3.1:latest', timeout=240):
    try:
        r = requests.post(f'{OLLAMA_URL}/api/generate', json={
            'model': model,
            'prompt': prompt,
            'stream': False,
            'options': {'temperature': 0.8, 'top_p': 0.92}
        }, timeout=timeout)
    except requests.exceptions.ConnectionError as e:
        raise OllamaError('Ollama is not running. Open a terminal and run: ollama serve') from e
    except requests.exceptions.Timeout as e:
        raise OllamaError(f'Ollama timed out after {timeout} seconds. Use a smaller model or increase timeout.') from e

    if r.status_code == 404:
        msg = ''
        try:
            msg = r.json().get('error', '')
        except Exception:
            msg = r.text[:300]
        raise OllamaError(
            f'Ollama returned 404. Most likely model "{model}" is not available to the running Ollama server. '
            f'Run: ollama list  |  then use the exact NAME shown. Details: {msg}'
        )

    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        raise OllamaError(f'Ollama error {r.status_code}: {r.text[:500]}') from e

    return (r.json().get('response') or '').strip()
