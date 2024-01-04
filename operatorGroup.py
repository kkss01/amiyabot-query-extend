import os

from core import log
from amiyabot.log import LoggerManager

from .operatorData import OperatorData, OperatorSearchInfo

curr_dir = os.path.dirname(__file__)
relative_dir = curr_dir.split('\\')[-1]

log = LoggerManager(' \b\b查询扩展')


async def export_group(chain, group:list, desc:str,):
    content = ''
    member = []
    for item in group:
        
        content += f'{item} '
        
        operator = await OperatorData.get_operator_detail(OperatorSearchInfo(name=item))
        if operator:

            skins = operator.skins()
            skins.reverse()
            
            for skin in skins:
                avatar_path = f"resource/gamedata/avatar/{skin['skin_id']}.png"
                if os.path.exists(avatar_path):
                    avatar_path = avatar_path.replace('#','%23')
                    break
            else:
                log.warning(f'没有找到干员 {operator.name} 的任何头像') 
                avatar_path = f'plugins/{relative_dir}/icon/error/error_w.png' 

            member.append({
                'name':operator.name,
                'classes_code':operator.classes_code,
                'rarity':operator.rarity,
                'avatar_path':avatar_path
            })
            
    if member:
        template = f'{curr_dir}/template/extendInfoCommon.html'
        return chain.text(desc).html(template, member, height=200, width=720)
    
    else:
        return chain.text(desc).text(content) 


