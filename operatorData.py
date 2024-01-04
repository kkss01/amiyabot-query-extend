from dataclasses import dataclass

from core.resource.arknightsGameData import ArknightsGameData, ArknightsGameDataResource


@dataclass
class OperatorSearchInfo:
    name: str = ''
    skin_key: str = ''
    group_key: str = ''
    voice_key: str = ''
    story_key: str = ''
    
    
class OperatorData:
    @classmethod
    async def get_operator_detail(cls, info: OperatorSearchInfo):
        operators = ArknightsGameData.operators

        if not info.name or info.name not in operators:
            return None

        operator = operators[info.name]

        return operator

 