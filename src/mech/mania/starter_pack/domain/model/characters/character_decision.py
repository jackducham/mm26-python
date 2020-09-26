from mech.mania.engine.domain.model import character_pb2
from mech.mania.starter_pack.domain.model.characters.position import Position


class CharacterDecision:
    def __init__(self, decision_type: str, action_position: Position, action_index=None):
        self.action_position = action_position
        self.decision_type = decision_type
        if action_index is not None:
            self.action_index = action_index

    def build_proto_class_character_decision(self):
        decision_builder = character_pb2.CharacterDecision()

        if self.decision_type == "MOVE":
            decision_builder.decision_type = character_pb2.DecisionType.MOVE
        elif self.decision_type == "ATTACK":
            decision_builder.decision_type = character_pb2.DecisionType.ATTACK
        elif self.decision_type == "PORTAL":
            decision_builder.decision_type = character_pb2.DecisionType.PORTAL
        elif self.decision_type == "DROP":
            decision_builder.decision_type = character_pb2.DecisionType.DROP
        elif self.decision_type == "EQUIP":
            decision_builder.decision_type = character_pb2.DecisionType.EQUIP
        elif self.decision_type == "PICKUP":
            decision_builder.decision_type = character_pb2.DecisionType.PICKUP
        else:
            decision_builder.decision_type = character_pb2.DecisionType.NONE

        decision_builder.index = self.action_index
        if self.action_position is not None:
            decision_builder.target_position = self.action_position.build_proto_class()

        return decision_builder
