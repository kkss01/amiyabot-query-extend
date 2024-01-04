import os
import re
import asyncio
from typing import Dict, List, Any

from core import log
from core.util import any_match, find_most_similar, remove_punctuation
from core.customPluginInstance import AmiyaBotPluginInstance
from core.resource.arknightsGameData import ArknightsGameData
from amiyabot import Message, Chain
from amiyabot.log import LoggerManager

from .operatorData import OperatorData, OperatorSearchInfo
from .operatorGroup import export_group

curr_dir = os.path.dirname(__file__)
relative_dir = curr_dir.split('\\')[-1]
STR_DICT_LIST = Dict[str, List[str]]

log = LoggerManager(' \b\b查询扩展')

class QueryExtendInstance(AmiyaBotPluginInstance):
    def install(self):
        asyncio.create_task(ExtendInfo.init_extend_info())


bot = QueryExtendInstance(
    name='干员查询扩展',
    version='2.5.2',
    plugin_id='kkss-query-extend',
    plugin_type='',
    description='查询某个类别的所属干员',
    document=f'{curr_dir}/README.md',
    global_config_default=f'{curr_dir}/default.json',
    global_config_schema=f'{curr_dir}/schema.json',
)

def remove_prefix(text:str):
    for item in bot.prefix_keywords:
        if text.startswith(item):
            text = text.replace(item, '', 1)
            return text
    
    return text

class ExtendInfo:
    operators_name: List[str] = []
    classes_sub: STR_DICT_LIST = {}
    classes: STR_DICT_LIST = {}
    drawer: STR_DICT_LIST = {}
    race: STR_DICT_LIST = {}
    nation: STR_DICT_LIST = {}
    group: STR_DICT_LIST = {}
    team: STR_DICT_LIST = {}
    index = [classes_sub,classes,race,nation,group,team,drawer]

    @classmethod
    async def init_extend_info(cls):

        operators = sorted(ArknightsGameData.operators.values(), key=lambda x:x.rarity, reverse=True)

        for item in operators:
            ExtendInfo.operators_name.append(item.name)
            ExtendInfo.append(ExtendInfo.classes_sub, item.classes_sub, item.name)
            ExtendInfo.append(ExtendInfo.classes, item.classes, item.classes_sub, True)
            ExtendInfo.append(ExtendInfo.race, item.race, item.name)
            ExtendInfo.append(ExtendInfo.nation, item.nation, item.name)
            ExtendInfo.append(ExtendInfo.group, item.group, item.name)
            ExtendInfo.append(ExtendInfo.team, item.team, item.name)
            ExtendInfo.append(ExtendInfo.drawer, item.drawer, item.name)

        l = 0
        for dict in ExtendInfo.index:
            l += len(dict)
            
        log.info(f'已注册 {l} 个对象')
            

    @staticmethod
    def append(target_dict: STR_DICT_LIST, key: str, value: Any, no_repeat=False):
        if key not in target_dict:
            target_dict[key] = [value]
        else:
            if no_repeat and value in target_dict[key]:
                return
            target_dict[key].append(value)

async def search_char_by_text(text: str) :
    source = ExtendInfo.operators_name

    res = find_most_similar(text, source)
    if res and remove_punctuation(res) in remove_punctuation(text):
        return res


async def extend_verify(data: Message):
    level = bot.get_config('defaultLevel')
    
    if attr := any_match(data.text, ['分支','种族','势力','阵营','队伍','画师']):
        level += 3
        
    candidate = [0,'']
    for index, info_dict in enumerate(ExtendInfo.index):
        if attr == '势力' and index == 2:
                continue
            
        for key in list(info_dict):
            if key in data.text:           
                
                if len(key) > len(candidate[1]):
                    candidate = [index, key]

    if candidate[1]:
        return True, level, candidate


@bot.on_message(verify=extend_verify, check_prefix=True)
async def search_group(data: Message, source=''):
    index, key = data.verify.keypoint 

    descriptions = [
        '分支 [{}] 共有以下 {} 名干员',
        '职业 [{}] 共有以下 {} 个子职业',
        '种族 [{}] 共有以下 {} 名干员',
        '势力 [{}] 共有以下 {} 名干员',
        '阵营 [{}] 共有以下 {} 名干员',
        '队伍 [{}] 共有以下 {} 名干员',
        '画师 [{}] 作品共有以下 {} 名干员',
    ]
    
    try: 
        desc = descriptions[index].format(key, len(ExtendInfo.index[index][key])) + '\n'
    except KeyError:
        await log.warning(f'无法找到键 {key}')
        return
    
    chain = Chain(data).text(source)
    return await export_group(chain, ExtendInfo.index[index][key], desc)
    
   
async def reverse_verify(data: Message):
    level = 4
    text = remove_prefix(data.text)
    r = re.search(r'(.+)的(分支|职业|种族|势力|阵营|队伍|画师)', text)
    if not r:
        return False

    level += bot.get_config('defaultLevel')
    return True, level, [r.group(1),r.group(2)]
    
@bot.on_message(verify=reverse_verify, check_prefix=True)
async def _(data: Message):
    
    search_name = data.verify.keypoint[0]
    name = await search_char_by_text(search_name)
    
    operator = await OperatorData.get_operator_detail(OperatorSearchInfo(name=name))
    if not operator:
        return Chain(data).text(f'没有找到干员 "{search_name}"')
    
    type_list = ['分支','职业','种族','势力','阵营','队伍','画师']
    type_attr = [
        operator.classes_sub,
        operator.classes,
        operator.race,
        operator.nation,
        operator.group,
        operator.team,
        operator.drawer,
    ]
    type_name = data.verify.keypoint[1]
    index = type_list.index(type_name)
    search_attr = type_attr[index]  

    data.verify.keypoint = index, search_attr

    if search_attr == '未知' and bot.get_config('hideUnknown'):
        return Chain(data).text(f'干员 {name} 没有所属的 {type_name}, 请尝试其他类别 (种族/势力/阵营/队伍)')
    
    chain = await search_group(data, f'{name} 的')
    return chain
    

    

