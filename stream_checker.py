import asyncio
from stream_status import is_stream_live
from bot import send_telegram_message

PREVIOUS_STATUS = False


async def main():
    global PREVIOUS_STATUS
    while True:
        try:
            is_live = await is_stream_live()
            if is_live and not PREVIOUS_STATUS:
                await send_telegram_message("🎥 Стрим начался!")
                PREVIOUS_STATUS = True
            elif not is_live:
                PREVIOUS_STATUS = False
        except Exception as e:
            print(f"[ERROR] {e}")
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
