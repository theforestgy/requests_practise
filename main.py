import os
import requests
from dotenv import load_dotenv


load_dotenv()


def get_vk_user_info(vk_token, user_id):
    url = "https://api.vk.com/method/users.get"
    params = {
        'user_ids': user_id,
        'fields': 'first_name,last_name',
        'access_token': vk_token,
        'v': '5.131'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        user_info = response.json().get('response', [])
        if user_info:
            user = user_info[0]
            return {
                'first_name': user.get('first_name'),
                'last_name': user.get('last_name')
            }
    return {}


def get_leetcode_user_info(leetcode_id):
    url = f"https://leetcode-stats-api.herokuapp.com/{leetcode_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'total_solved': data.get('totalSolved'),
            'easy_solved': data.get('easySolved'),
            'medium_solved': data.get('mediumSolved'),
            'hard_solved': data.get('hardSolved')
        }
    return {}


def get_stepik_user_info(stepik_token, stepik_id):
    headers = {'Authorization': f'Bearer {stepik_token}'}
    response = requests.get(f'https://stepik.org/api/users/{stepik_id}', headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'users' in data and len(data['users']) > 0:
            user = data.get('users')[0]
            return {
                'name': user.get('first_name') + ' ' + user.get('last_name'),
                'solved_steps': user.get('solved_steps_count')
            }
    return {}


def main():
    vk_token = os.getenv('VK_TOKEN')
    vk_id = os.getenv('VK_ID')

    leetcode_id = os.getenv('LEETCODE_ID')

    stepik_token = os.getenv('STEPIK_TOKEN')
    stepik_id = os.getenv('STEPIK_ID')

    vk_info = get_vk_user_info(vk_token, vk_id)

    leetcode_info = get_leetcode_user_info(leetcode_id)

    stepik_info = get_stepik_user_info(stepik_token, stepik_id)

    print("VK Info:", vk_info)
    print("LeetCode Info:", leetcode_info)
    print("Stepik Info:", stepik_info)


if __name__ == "__main__":
    main()
