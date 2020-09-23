from engine.characters.position import Position
from protos import character_pb2


class CharacterDecision:
    def __init__(self, decision_type: str, action_position: Position, inventory_index=None):
        self.action_position = action_position
        self.decision_type = decision_type
        if inventory_index is not None:
            self.inventory_index = inventory_index

    def build_proto_class_character_decision(self):
        decision_builder = character_pb2.CharacterDecision()

        if self.decision_type == "NONE":
            decision_builder.decision_type = character_pb2.DecisionType.NONE
        elif self.decision_type == "MOVE":
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

        decision_builder.index = self.inventory_index
        decision_builder.target_position = self.action_position.build_proto_class()

        return decision_builder
