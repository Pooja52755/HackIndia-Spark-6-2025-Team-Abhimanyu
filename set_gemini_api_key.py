#!/usr/bin/env python3
import os
import sys

def set_api_key():
    if len(sys.argv) < 2:
        print("Usage: python set_gemini_api_key.py YOUR_API_KEY")
        return
    
    api_key = sys.argv[1]
    
    # Check if .env file exists
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    
    if os.path.exists(env_path):
        # Read existing content
        with open(env_path, 'r') as file:
            lines = file.readlines()
        
        # Update or add API key
        api_key_found = False
        for i, line in enumerate(lines):
            if line.startswith('GEMINI_API_KEY='):
                lines[i] = f'GEMINI_API_KEY={api_key}\n'
                api_key_found = True
                break
        
        if not api_key_found:
            lines.append(f'\nGEMINI_API_KEY={api_key}\n')
        
        # Write back to file
        with open(env_path, 'w') as file:
            file.writelines(lines)
    else:
        # Create new .env file
        with open(env_path, 'w') as file:
            file.write(f'GEMINI_API_KEY={api_key}\n')
            file.write('FLASK_DEBUG=False\n')
    
    print(f"Gemini API key has been set in {env_path}")
    print("You can now run the application with your API key.")

if __name__ == "__main__":
    set_api_key() 