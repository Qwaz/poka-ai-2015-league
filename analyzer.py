import json
import re
import os.path
import subprocess
import time


def parse_setting():
    setting_file = open('setting.json', 'r')
    return json.loads(setting_file.read())


setting = parse_setting()

if not os.path.isdir(setting['server_directory']):
    raise FileNotFoundError('서버 프로그램이 존재하지 않습니다: ' + setting['server'])

if not os.path.isdir(setting['ai_directory']):
    raise NotADirectoryError('AI 디렉토리를 찾을 수 없습니다: ' + setting['ai_directory'])

for team in setting['ai']:
    ai_path = os.path.join(setting['ai_directory'], team[1])
    if not os.path.exists(ai_path):
        raise FileNotFoundError('파일이 존재하지 않습니다: ' + ai_path)

result = {
    "ai_list": [team[0] for team in setting['ai']],
    "match": []
}

for index1, team1 in enumerate(setting['ai']):
    for index2, team2 in enumerate(setting['ai']):
        if index1 >= index2:
            continue
        current = {
            "team1": team1[0],
            "team2": team2[0],
            "result": []
        }

        for i in range(5):
            time.sleep(1)
            server_process = subprocess.Popen(os.path.join(setting['server_directory'], 'HAJE.SlimeAI.exe'),
                                              cwd=setting['server_directory'])
            time.sleep(1)

            team1_process = subprocess.Popen(['python', os.path.join(setting['ai_directory'], team1[1]), '-t', '1'],
                                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            team2_process = subprocess.Popen(['python', os.path.join(setting['ai_directory'], team2[1]), '-t', '2'],
                                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            count = [0, 0, 0]
            while True:
                line = team1_process.stdout.readline()
                match = re.match(br'Result: (\d+) / (\d+) / (\d+)', line)
                if match:
                    for i in range(3):
                        count[i] = int(match.group(i + 1))
                    break

            print('%s %d vs %s %d' % (team1[0], count[0], team2[0], count[1]))
            current['result'].append(count)
            server_process.kill()

        result['match'].append(current)

result_file = open('result.json', 'w')
json.dump(result, result_file)
