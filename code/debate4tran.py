"""
MAD: Multi-Agent Debate with Large Language Models
Copyright (C) 2023  The MAD Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import os
import json
import random
# random.seed(0)
import argparse
from langcodes import Language
from utils.agent import Agent
from datetime import datetime
from tqdm import tqdm


NAME_LIST=[
    "Affirmative side",
    "Negative side",
    "Moderator",
]

class DebatePlayer(Agent):
    def __init__(self, name: str, temperature:float, openai_api_key: str, sleep_time: float) -> None:
        """Create a player in the debate

        Args:
            name (str): name of this player
            temperature (float): higher values make the output more random, while lower values make it more focused and deterministic
            openai_api_key (str): As the parameter name suggests
            sleep_time (float): sleep because of rate limits
        """
        super(DebatePlayer, self).__init__(name, temperature, openai_api_key, sleep_time)


class Debate:
    def __init__(self,
            temperature: float=0, 
            num_players: int=3, 
            save_file_dir: str=None,
            openai_api_key: str=None,
            prompts_path: str=None,
            max_round: int=3,
            sleep_time: float=0
        ) -> None:
        """Create a debate

        Args:
            temperature (float): higher values make the output more random, while lower values make it more focused and deterministic
            num_players (int): num of players
            save_file_dir (str): dir path to json file
            openai_api_key (str): As the parameter name suggests
            prompts_path (str): prompts path (json file)
            max_round (int): maximum Rounds of Debate
            sleep_time (float): sleep because of rate limits
        """

        self.temperature = temperature
        self.num_players = num_players
        self.save_file_dir = save_file_dir
        self.openai_api_key = openai_api_key
        self.max_round = max_round
        self.sleep_time = sleep_time
        # 不再需要model_name，因为使用固定的deepseek模型

        # init save file
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d_%H:%M:%S")
        self.save_file = {
            'start_time': current_time,
            'end_time': '',
            'model_name': 'deepseek-chat',
            'temperature': temperature,
            'num_players': num_players,
            'success': False,
            "src_lng": "",
            "tgt_lng": "",
            'source': '',
            'reference': '',
            'base_translation': '',
            "debate_translation": '',
            "Reason": '',
            "Supported Side": '',
            'players': {},
        }
        prompts = json.load(open(prompts_path))
        self.save_file.update(prompts)
        self.init_prompt()

        if self.save_file.get('base_translation', '') == "" and self.save_file.get('base_answer', '') == "":
            self.create_base()

        # creat&init agents
        self.creat_agents()
        self.init_agents()


    def init_prompt(self):
        def prompt_replace(key):
            src_lng = self.save_file.get("src_lng", "")
            tgt_lng = self.save_file.get("tgt_lng", "")
            source = self.save_file.get("source", "")
            base_translation = self.save_file.get("base_translation", "")
            base_answer = self.save_file.get("base_answer", "")
            content = self.save_file[key]
            content = content.replace("##src_lng##", src_lng)
            content = content.replace("##tgt_lng##", tgt_lng)
            content = content.replace("##source##", source)
            content = content.replace("##base_translation##", base_translation)
            content = content.replace("##base_answer##", base_answer)
            
            self.save_file[key] = content
        prompt_replace("base_prompt")
        prompt_replace("player_meta_prompt")
        prompt_replace("moderator_meta_prompt")
        prompt_replace("judge_prompt_last2")

    def create_base(self):
        print(f"\n===== Question Answering Task =====\n{self.save_file['base_prompt']}\n")
        agent = DebatePlayer(name='Baseline', temperature=self.temperature, openai_api_key=self.openai_api_key, sleep_time=self.sleep_time)
        agent.add_event(self.save_file['base_prompt'])
        base_answer = agent.ask()
        agent.add_memory(base_answer)
        self.save_file['base_answer'] = base_answer
        self.save_file['affirmative_prompt'] = self.save_file['affirmative_prompt'].replace("##base_answer##", base_answer)
        self.save_file['players'][agent.name] = agent.memory_lst

    def creat_agents(self):
        # creates players
        self.players = [
            DebatePlayer(name=name, temperature=self.temperature, openai_api_key=self.openai_api_key, sleep_time=self.sleep_time) for name in NAME_LIST
        ]
        self.affirmative = self.players[0]
        self.negative = self.players[1]
        self.moderator = self.players[2]

    def init_agents(self):
        # start: set meta prompt
        self.affirmative.set_meta_prompt(self.save_file['player_meta_prompt'])
        self.negative.set_meta_prompt(self.save_file['player_meta_prompt'])
        self.moderator.set_meta_prompt(self.save_file['moderator_meta_prompt'])
        
        # start: first round debate, state opinions
        print(f"===== Debate Round-1 =====\n")
        self.affirmative.add_event(self.save_file['affirmative_prompt'])
        self.aff_ans = self.affirmative.ask()
        self.affirmative.add_memory(self.aff_ans)

        self.negative.add_event(self.save_file['negative_prompt'].replace('##aff_ans##', self.aff_ans))
        self.neg_ans = self.negative.ask()
        self.negative.add_memory(self.neg_ans)

        self.moderator.add_event(self.save_file['moderator_prompt'].replace('##aff_ans##', self.aff_ans).replace('##neg_ans##', self.neg_ans).replace('##round##', 'first'))
        self.mod_ans = self.moderator.ask()
        self.moderator.add_memory(self.mod_ans)
        self.mod_ans = eval(self.mod_ans)

    def round_dct(self, num: int):
        dct = {
            1: 'first', 2: 'second', 3: 'third', 4: 'fourth', 5: 'fifth', 6: 'sixth', 7: 'seventh', 8: 'eighth', 9: 'ninth', 10: 'tenth'
        }
        return dct[num]
            
    def save_file_to_json(self, id):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d_%H:%M:%S")
        save_file_path = os.path.join(self.save_file_dir, f"{id}.json")
        
        self.save_file['end_time'] = current_time
        json_str = json.dumps(self.save_file, ensure_ascii=False, indent=4)
        with open(save_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

    def broadcast(self, msg: str):
        """Broadcast a message to all players. 
        Typical use is for the host to announce public information

        Args:
            msg (str): the message
        """
        # print(msg)
        for player in self.players:
            player.add_event(msg)

    def speak(self, speaker: str, msg: str):
        """The speaker broadcast a message to all other players. 

        Args:
            speaker (str): name of the speaker
            msg (str): the message
        """
        if not msg.startswith(f"{speaker}: "):
            msg = f"{speaker}: {msg}"
        # print(msg)
        for player in self.players:
            if player.name != speaker:
                player.add_event(msg)

    def ask_and_speak(self, player: DebatePlayer):
        ans = player.ask()
        player.add_memory(ans)
        self.speak(player.name, ans)


    def run(self):

        for round in range(self.max_round - 1):

            if self.mod_ans.get("debate_answer", "") != '':
                break
            else:
                print(f"===== Debate Round-{round+2} =====\n")
                self.affirmative.add_event(self.save_file['debate_prompt'].replace('##oppo_ans##', self.neg_ans))
                self.aff_ans = self.affirmative.ask()
                self.affirmative.add_memory(self.aff_ans)

                self.negative.add_event(self.save_file['debate_prompt'].replace('##oppo_ans##', self.aff_ans))
                self.neg_ans = self.negative.ask()
                self.negative.add_memory(self.neg_ans)

                self.moderator.add_event(self.save_file['moderator_prompt'].replace('##aff_ans##', self.aff_ans).replace('##neg_ans##', self.neg_ans).replace('##round##', self.round_dct(round+2)))
                self.mod_ans = self.moderator.ask()
                self.moderator.add_memory(self.mod_ans)
                self.mod_ans = eval(self.mod_ans)

        if self.mod_ans.get("debate_answer", "") != '':
            self.save_file.update(self.mod_ans)
            self.save_file['success'] = True

        # ultimate deadly technique.
        else:
            judge_player = DebatePlayer(name='Judge', temperature=self.temperature, openai_api_key=self.openai_api_key, sleep_time=self.sleep_time)
            aff_ans = self.affirmative.memory_lst[2]['content']
            neg_ans = self.negative.memory_lst[2]['content']

            judge_player.set_meta_prompt(self.save_file['moderator_meta_prompt'])

            # extract answer candidates
            judge_player.add_event(self.save_file['judge_prompt_last1'].replace('##aff_ans##', aff_ans).replace('##neg_ans##', neg_ans))
            ans = judge_player.ask()
            judge_player.add_memory(ans)

            # select one from the candidates
            judge_player.add_event(self.save_file['judge_prompt_last2'])
            ans = judge_player.ask()
            judge_player.add_memory(ans)
            
            ans = eval(ans)
            if ans.get("debate_answer", "") != '':
                self.save_file['success'] = True
                # save file
            self.save_file.update(ans)
            self.players.append(judge_player)

        for player in self.players:
            self.save_file['players'][player.name] = player.memory_lst


def parse_args():
    parser = argparse.ArgumentParser("", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-i", "--input-file", type=str, required=True, help="Input file path")
    parser.add_argument("-o", "--output-dir", type=str, required=True, help="Output file dir")
    parser.add_argument("-lp", "--lang-pair", type=str, required=True, help="Language pair")
    parser.add_argument("-k", "--api-key", type=str, required=True, help="OpenAI api key")
    parser.add_argument("-m", "--model-name", type=str, default="gpt-3.5-turbo", help="Model name")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    openai_api_key = args.api_key

    current_script_path = os.path.abspath(__file__)
    # 使用os.path模块处理路径，确保跨平台兼容
    MAD_path = os.path.dirname(os.path.dirname(current_script_path))

    src_lng, tgt_lng = args.lang_pair.split('-')
    src_full = Language.make(language=src_lng).display_name()
    tgt_full = Language.make(language=tgt_lng).display_name()

    config_path = os.path.join(MAD_path, "code", "utils", "config4.json")
    config = json.load(open(config_path, "r"))

    inputs = open(args.input_file, "r", encoding="utf-8").readlines()
    inputs = [l.strip() for l in inputs]

    save_file_dir = args.output_dir
    if not os.path.exists(save_file_dir):
            os.mkdir(save_file_dir)

    for id, input in enumerate(tqdm(inputs)):
        # files = os.listdir(save_file_dir)
        # if f"{id}.json" in files:
        #     continue

        prompts_path = os.path.join(save_file_dir, f"{id}-config.json")

        # 处理输入格式，支持制表符或空格分隔
        if '\t' in input:
            parts = input.split('\t')
        else:
            # 使用正则表达式分割，处理多个空格的情况
            import re
            parts = re.split('\s+', input, 1)
        
        config['source'] = parts[0]
        config['reference'] = parts[1] if len(parts) > 1 else ''
        config['src_lng'] = src_full
        config['tgt_lng'] = tgt_full

        with open(prompts_path, 'w') as file:
            json.dump(config, file, ensure_ascii=False, indent=4)

        debate = Debate(save_file_dir=save_file_dir, num_players=3, openai_api_key=openai_api_key, prompts_path=prompts_path, temperature=0, sleep_time=0)
        debate.run()
        debate.save_file_to_json(id)