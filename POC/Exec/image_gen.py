import requests
import random

def generate(prompt):
    url = "https://api.airforce/v1/imagine"
    params = {
        "prompt": prompt,
        "size": "1:1",
        "seed": random.randint(100000, 999999),
        "model": "flux-realism",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        with open("generated_image.png", "wb") as f:
            f.write(response.content)
        print("Image saved as 'generated_image.png'")
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    prompt = input("Enter a prompt: ")
    generate(prompt)