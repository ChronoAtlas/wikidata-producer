from enum import Enum


class KafkaMessageType(Enum):
    NewBattle = "NewBattle"
    BattleUpdate = "BattleUpdate"
