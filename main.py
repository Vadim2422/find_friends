import json
import os
import requests

token: str

def get_user_id(id):
    return requests.get(
        f'https://api.vk.com/method/utils.resolveScreenName?screen_name={id}&access_token={token}&v=5.131').json()[
        'response']['object_id']


def get_all_friends(friend):
    id = get_user_id(friend)
    all_ids = requests.get(
        f'https://api.vk.com/method/friends.get?user_id={id}&access_token={token}&v=5.131').json().get(
        'response').get('items')
    return all_ids


def main():
    global token
    token = os.getenv("token")
    coincidence = []
    with open('friends.json', 'r') as file:
        friends = json.load(file).get('friends')
    for index, friend in enumerate(friends):
        if index == 0:
            coincidence.extend(get_all_friends(friend))
        else:
            coincidence = set(coincidence).intersection(get_all_friends(friend))
    coincidence = ['https://vk.com/id' + str(i) for i in coincidence]
    for link in coincidence:
        print(link)
    with open(f'coincidence', 'w') as file:
        file.write(coincidence.__str__())


if __name__ == '__main__':
    main()
