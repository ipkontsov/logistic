from config import settings
import asyncio

async def test_redis():
    try:
        client = settings.redis_client
        print('✅ Подключаемся к Redis...')
        await client.set('test_key', 'hello_from_python')
        value = await client.get('test_key')
        print(f'✅ Redis работает! Значение: {value}')
    except Exception as e:
        print(f'❌ Ошибка подключения к Redis: {e}')
    finally:
        await client.aclose()

if __name__ == '__main__':
    asyncio.run(test_redis())