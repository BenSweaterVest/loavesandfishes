"""
Dialogue and Cutscene System - Story presentation and NPC interactions
"""

from typing import List, Dict, Any, Optional, Callable
from enum import Enum


class DialogueChoice:
    """A choice in a dialogue tree"""

    def __init__(self,
                 text: str,
                 next_node: Optional[str] = None,
                 action: Optional[Callable] = None,
                 condition: Optional[Callable] = None):
        """
        Initialize dialogue choice

        Args:
            text: Choice text to display
            next_node: ID of next dialogue node
            action: Function to execute when chosen
            condition: Function that returns True if choice is available
        """
        self.text = text
        self.next_node = next_node
        self.action = action
        self.condition = condition

    def is_available(self) -> bool:
        """Check if this choice is available"""
        if self.condition:
            return self.condition()
        return True


class DialogueNode:
    """A node in a dialogue tree"""

    def __init__(self,
                 node_id: str,
                 speaker: str,
                 text: str,
                 choices: List[DialogueChoice] = None):
        """
        Initialize dialogue node

        Args:
            node_id: Unique node identifier
            speaker: Who is speaking
            text: Dialogue text
            choices: List of player choices (if any)
        """
        self.node_id = node_id
        self.speaker = speaker
        self.text = text
        self.choices = choices or []

    def add_choice(self, choice: DialogueChoice):
        """Add a choice to this node"""
        self.choices.append(choice)

    def get_available_choices(self) -> List[DialogueChoice]:
        """Get all available choices"""
        return [c for c in self.choices if c.is_available()]


class Dialogue:
    """Complete dialogue tree"""

    def __init__(self, dialogue_id: str, start_node: str):
        """
        Initialize dialogue

        Args:
            dialogue_id: Unique dialogue identifier
            start_node: ID of starting node
        """
        self.dialogue_id = dialogue_id
        self.start_node = start_node
        self.nodes: Dict[str, DialogueNode] = {}
        self.current_node: Optional[str] = None

    def add_node(self, node: DialogueNode):
        """Add a node to the dialogue"""
        self.nodes[node.node_id] = node

    def start(self):
        """Start the dialogue"""
        self.current_node = self.start_node

    def get_current_node(self) -> Optional[DialogueNode]:
        """Get the current dialogue node"""
        if self.current_node:
            return self.nodes.get(self.current_node)
        return None

    def choose(self, choice_index: int) -> Optional[DialogueNode]:
        """
        Make a choice and advance dialogue

        Args:
            choice_index: Index of chosen option

        Returns:
            Next dialogue node, or None if dialogue ended
        """
        current = self.get_current_node()
        if not current:
            return None

        available_choices = current.get_available_choices()
        if 0 <= choice_index < len(available_choices):
            choice = available_choices[choice_index]

            # Execute action if any
            if choice.action:
                choice.action()

            # Move to next node
            if choice.next_node:
                self.current_node = choice.next_node
                return self.get_current_node()

        # End of dialogue
        self.current_node = None
        return None

    def is_finished(self) -> bool:
        """Check if dialogue is finished"""
        current = self.get_current_node()
        return current is None or len(current.get_available_choices()) == 0


class CutsceneAction(Enum):
    """Types of cutscene actions"""
    DIALOGUE = "dialogue"
    MOVE_PLAYER = "move_player"
    MOVE_NPC = "move_npc"
    SHOW_IMAGE = "show_image"
    PLAY_SOUND = "play_sound"
    WAIT = "wait"
    FADE_OUT = "fade_out"
    FADE_IN = "fade_in"
    BATTLE = "battle"
    RECRUIT_APOSTLE = "recruit_apostle"
    RECEIVE_ITEM = "receive_item"
    SET_FLAG = "set_flag"


class CutsceneStep:
    """A single step in a cutscene"""

    def __init__(self,
                 action: CutsceneAction,
                 data: Dict[str, Any] = None,
                 wait_for_input: bool = False):
        """
        Initialize cutscene step

        Args:
            action: Type of action
            data: Action-specific data
            wait_for_input: Wait for player input before continuing
        """
        self.action = action
        self.data = data or {}
        self.wait_for_input = wait_for_input
        self.completed = False

    def execute(self, game_state) -> bool:
        """
        Execute this step

        Args:
            game_state: Current game state

        Returns:
            True if step completed
        """
        # This will be implemented by specific cutscene handlers
        self.completed = True
        return True


class Cutscene:
    """A cutscene sequence"""

    def __init__(self, cutscene_id: str, name: str):
        """
        Initialize cutscene

        Args:
            cutscene_id: Unique cutscene identifier
            name: Cutscene name
        """
        self.cutscene_id = cutscene_id
        self.name = name
        self.steps: List[CutsceneStep] = []
        self.current_step = 0
        self.is_playing = False
        self.is_complete = False

    def add_step(self, step: CutsceneStep):
        """Add a step to the cutscene"""
        self.steps.append(step)

    def start(self):
        """Start playing the cutscene"""
        self.is_playing = True
        self.is_complete = False
        self.current_step = 0

    def advance(self, game_state) -> bool:
        """
        Advance to next step

        Args:
            game_state: Current game state

        Returns:
            True if cutscene is still playing
        """
        if self.current_step >= len(self.steps):
            self.is_playing = False
            self.is_complete = True
            return False

        step = self.steps[self.current_step]

        if not step.completed:
            step.execute(game_state)

        if step.completed:
            self.current_step += 1

        return self.is_playing

    def get_current_step(self) -> Optional[CutsceneStep]:
        """Get current cutscene step"""
        if 0 <= self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None

    def skip(self):
        """Skip the cutscene"""
        self.is_playing = False
        self.is_complete = True
        self.current_step = len(self.steps)


class DialogueManager:
    """Manages all dialogues and cutscenes"""

    def __init__(self):
        """Initialize dialogue manager"""
        self.dialogues: Dict[str, Dialogue] = {}
        self.cutscenes: Dict[str, Cutscene] = {}
        self.current_dialogue: Optional[Dialogue] = None
        self.current_cutscene: Optional[Cutscene] = None

    def register_dialogue(self, dialogue: Dialogue):
        """Register a dialogue"""
        self.dialogues[dialogue.dialogue_id] = dialogue

    def register_cutscene(self, cutscene: Cutscene):
        """Register a cutscene"""
        self.cutscenes[cutscene.cutscene_id] = cutscene

    def start_dialogue(self, dialogue_id: str) -> bool:
        """
        Start a dialogue

        Args:
            dialogue_id: Dialogue to start

        Returns:
            True if dialogue started
        """
        dialogue = self.dialogues.get(dialogue_id)
        if dialogue:
            dialogue.start()
            self.current_dialogue = dialogue
            return True
        return False

    def start_cutscene(self, cutscene_id: str) -> bool:
        """
        Start a cutscene

        Args:
            cutscene_id: Cutscene to start

        Returns:
            True if cutscene started
        """
        cutscene = self.cutscenes.get(cutscene_id)
        if cutscene:
            cutscene.start()
            self.current_cutscene = cutscene
            return True
        return False

    def is_in_dialogue(self) -> bool:
        """Check if currently in dialogue"""
        return self.current_dialogue is not None and not self.current_dialogue.is_finished()

    def is_in_cutscene(self) -> bool:
        """Check if currently in cutscene"""
        return self.current_cutscene is not None and self.current_cutscene.is_playing

    def create_simple_dialogue(self,
                               dialogue_id: str,
                               speaker: str,
                               lines: List[str]) -> Dialogue:
        """
        Create a simple linear dialogue

        Args:
            dialogue_id: Dialogue ID
            speaker: Speaker name
            lines: List of dialogue lines

        Returns:
            Dialogue instance
        """
        dialogue = Dialogue(dialogue_id, "start")

        for i, line in enumerate(lines):
            node_id = f"node_{i}" if i > 0 else "start"
            next_node = f"node_{i+1}" if i < len(lines) - 1 else None

            node = DialogueNode(node_id, speaker, line)

            if next_node:
                node.add_choice(DialogueChoice("Continue", next_node))
            else:
                node.add_choice(DialogueChoice("End", None))

            dialogue.add_node(node)

        self.register_dialogue(dialogue)
        return dialogue

    def create_quest_dialogue(self,
                              dialogue_id: str,
                              quest_giver: str,
                              quest_text: str,
                              accept_callback: Callable = None,
                              decline_callback: Callable = None) -> Dialogue:
        """
        Create a quest acceptance dialogue

        Args:
            dialogue_id: Dialogue ID
            quest_giver: NPC offering quest
            quest_text: Quest description
            accept_callback: Function to call if quest accepted
            decline_callback: Function to call if quest declined

        Returns:
            Dialogue instance
        """
        dialogue = Dialogue(dialogue_id, "offer")

        # Offer node
        offer = DialogueNode("offer", quest_giver, quest_text)
        offer.add_choice(DialogueChoice(
            "Accept Quest",
            "accepted",
            action=accept_callback
        ))
        offer.add_choice(DialogueChoice(
            "Decline",
            "declined",
            action=decline_callback
        ))
        dialogue.add_node(offer)

        # Accepted node
        accepted = DialogueNode(
            "accepted",
            quest_giver,
            "Thank you! May the Lord be with you on this journey."
        )
        accepted.add_choice(DialogueChoice("Farewell", None))
        dialogue.add_node(accepted)

        # Declined node
        declined = DialogueNode(
            "declined",
            quest_giver,
            "I understand. Come back if you change your mind."
        )
        declined.add_choice(DialogueChoice("Farewell", None))
        dialogue.add_node(declined)

        self.register_dialogue(dialogue)
        return dialogue
