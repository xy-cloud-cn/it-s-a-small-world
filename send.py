import json, requests

server_ip = '127.0.0.1'
server_send_port = 5700

def get_group_list():
    cq_url = f"http://127.0.0.1:5700/get_group_list"
    rev = json.loads(requests.get(cq_url).text)
    return rev
def get_group_member_list(group_id):
    cq_url = f"http://127.0.0.1:5700/get_group_member_list?group_id={group_id}"
    rev = json.loads(requests.get(cq_url).text)
    return rev
