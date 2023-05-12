import asyncio
import json
import os
from aiohttp import ClientSession

token: str


async def send_request(method: str, **params):
    params['access_token'] = token
    params['v'] = 5.131
    request = f'https://api.vk.com/method/{method}'
    async with ClientSession() as session:
        async with session.get(request, params=params) as response:
            return await response.json()


async def get_user_id(user_id):

    return (await send_request("utils.resolveScreenName", screen_name=user_id))['response']['object_id']


async def get_all_friends(friend):
    id = await get_user_id(friend)
    return (await send_request('friends.get', user_id=id)).get('response').get('items')


async def main():
    global token
    token = os.getenv("token")
    coincidence = None
    with open('friends.json', 'r') as file:
        friends = json.load(file).get('friends')
    for friend in friends:
        if coincidence is None:
            coincidence = await get_all_friends(friend)
            # coincidence.extend(get_all_friends(friend))
        else:
            if not coincidence:
                break
            coincidence = set(coincidence).intersection(await get_all_friends(friend))
    coincidence = ['https://vk.com/id' + str(i) for i in coincidence]
    for link in coincidence:
        print(link)
    with open(f'coincidence', 'w') as file:
        json.dump(coincidence, file, indent=4)


if __name__ == '__main__':
    asyncio.run(main())
