import asyncio

import httpx

import schema
import database


def get_count_people(url: str) -> int:
    response = httpx.get(url)
    return int(response.json().get('count'))


async def get_character_info(semaphore: asyncio.Semaphore,
                             session: httpx.AsyncClient,
                             url: str,
                             id: int) -> schema.Character:
    async with semaphore:
        response = await session.get(f'{url}{id}')
    data = response.json()
    return schema.Character(id=id, **data)


async def main():
    await database.create_table()

    semaphore = asyncio.Semaphore(20)
    base_url = 'https://swapi.dev/api/people/'

    counter_people = get_count_people(base_url)

    url_tasks = []
    async with httpx.AsyncClient(timeout=None) as session:
        # for number in range(1, counter_people + 1):
        for number in [*list(range(1, 17)), *list(range(18, 84))]:
            task = asyncio.create_task(get_character_info(semaphore, session, base_url, number))
            url_tasks.append(task)

        characters = await asyncio.gather(*url_tasks)

    db_tasks = []
    for character in characters:
        tasks = asyncio.create_task(database.create_character(character))
        db_tasks.append(tasks)

    await asyncio.gather(*db_tasks)


if __name__ == '__main__':
    asyncio.run(main())
