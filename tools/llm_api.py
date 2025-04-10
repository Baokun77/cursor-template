#!/usr/bin/env /workspace/tmp_windsurf/venv/bin/python3

from openai import OpenAI
import argparse
import os
from dotenv import load_dotenv
from pathlib import Path
import sys
import base64
from typing import Optional
import mimetypes

def load_environment():
    """Load environment variables from .env files in order of precedence"""
    # Order of precedence:
    # 1. System environment variables (already loaded)
    # 2. .env.local (user-specific overrides)
    # 3. .env (project defaults)
    # 4. .env.example (example configuration)
    
    env_files = ['.env.local', '.env', '.env.example']
    env_loaded = False
    
    print("Current working directory:", Path('.').absolute(), file=sys.stderr)
    print("Looking for environment files:", env_files, file=sys.stderr)
    
    for env_file in env_files:
        env_path = Path('.') / env_file
        print(f"Checking {env_path.absolute()}", file=sys.stderr)
        if env_path.exists():
            print(f"Found {env_file}, loading variables...", file=sys.stderr)
            load_dotenv(dotenv_path=env_path)
            env_loaded = True
            print(f"Loaded environment variables from {env_file}", file=sys.stderr)
            # Print loaded keys (but not values for security)
            with open(env_path) as f:
                keys = [line.split('=')[0].strip() for line in f if '=' in line and not line.startswith('#')]
                print(f"Keys loaded from {env_file}: {keys}", file=sys.stderr)
    
    if not env_loaded:
        print("Warning: No .env files found. Using system environment variables only.", file=sys.stderr)
        print("Available system environment variables:", list(os.environ.keys()), file=sys.stderr)

# Load environment variables at module import
load_environment()

def encode_image_file(image_path: str) -> tuple[str, str]:
    """
    Encode an image file to base64 and determine its MIME type.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        tuple: (base64_encoded_string, mime_type)
    """
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = 'image/png'  # Default to PNG if type cannot be determined
        
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
    return encoded_string, mime_type

def create_llm_client():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return OpenAI(api_key=api_key)

def query_llm(prompt: str, client=None, model=None, image_path: Optional[str] = None) -> Optional[str]:
    """
    Query OpenAI with a prompt and optional image attachment.
    
    Args:
        prompt (str): The text prompt to send
        client: The OpenAI client instance
        model (str, optional): The model to use
        image_path (str, optional): Path to an image file to attach
        
    Returns:
        Optional[str]: The LLM's response or None if there was an error
    """
    if client is None:
        client = create_llm_client()
    
    try:
        # Set default model
        if model is None:
            model = "gpt-4o"
        
        messages = [{"role": "user", "content": []}]
        
        # Add text content
        messages[0]["content"].append({
            "type": "text",
            "text": prompt
        })
        
        # Add image content if provided
        if image_path:
            encoded_image, mime_type = encode_image_file(image_path)
            messages[0]["content"] = [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{encoded_image}"}}
            ]
        
        kwargs = {
            "model": model,
            "messages": messages,
            "temperature": 0.7,
        }
        
        # Add o1-specific parameters
        if model == "o1":
            kwargs["response_format"] = {"type": "text"}
            kwargs["reasoning_effort"] = "low"
            del kwargs["temperature"]
        
        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
            
    except Exception as e:
        print(f"Error querying LLM: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description='Query OpenAI with a prompt')
    parser.add_argument('--prompt', type=str, help='The prompt to send to OpenAI', required=True)
    parser.add_argument('--model', type=str, help='The model to use (default: gpt-4o)')
    parser.add_argument('--image', type=str, help='Path to an image file to attach to the prompt')
    args = parser.parse_args()

    response = query_llm(args.prompt, model=args.model, image_path=args.image)
    if response:
        print(response)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()