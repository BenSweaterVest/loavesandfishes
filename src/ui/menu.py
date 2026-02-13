"""
Menu System - Interactive UI for party, inventory, and game management
"""

from typing import List, Dict, Any, Optional, Callable
from enum import Enum

from utils.data_loader import get_data_loader, get_item, get_apostle
from utils.save_system import get_save_system


class MenuResult(Enum):
    """Menu interaction results"""
    CONTINUE = "continue"
    BACK = "back"
    EXIT = "exit"
    ACTION = "action"


class MenuItem:
    """Represents a single menu item"""

    def __init__(self,
                 text: str,
                 action: Optional[Callable] = None,
                 enabled: bool = True,
                 description: str = ""):
        """
        Initialize a menu item

        Args:
            text: Display text for the menu item
            action: Function to call when selected
            enabled: Whether the item can be selected
            description: Optional description shown when highlighted
        """
        self.text = text
        self.action = action
        self.enabled = enabled
        self.description = description

    def execute(self) -> Any:
        """Execute the menu item's action"""
        if self.action and self.enabled:
            return self.action()
        return None


class Menu:
    """Base menu class"""

    def __init__(self, title: str, items: List[MenuItem] = None):
        """
        Initialize a menu

        Args:
            title: Menu title
            items: List of menu items
        """
        self.title = title
        self.items = items or []
        self.selected_index = 0

    def add_item(self, item: MenuItem):
        """Add an item to the menu"""
        self.items.append(item)

    def move_up(self):
        """Move selection up"""
        self.selected_index = max(0, self.selected_index - 1)
        # Skip disabled items
        while self.selected_index > 0 and not self.items[self.selected_index].enabled:
            self.selected_index -= 1

    def move_down(self):
        """Move selection down"""
        self.selected_index = min(len(self.items) - 1, self.selected_index + 1)
        # Skip disabled items
        while self.selected_index < len(self.items) - 1 and not self.items[self.selected_index].enabled:
            self.selected_index += 1

    def select(self) -> Any:
        """Execute the selected item"""
        if 0 <= self.selected_index < len(self.items):
            return self.items[self.selected_index].execute()
        return None

    def get_display_text(self) -> List[str]:
        """
        Get menu display text

        Returns:
            List of strings to display
        """
        lines = []
        lines.append("=" * 60)
        lines.append(self.title.center(60))
        lines.append("=" * 60)
        lines.append("")

        for i, item in enumerate(self.items):
            prefix = "→ " if i == self.selected_index else "  "
            enabled_indicator = "" if item.enabled else " [DISABLED]"
            lines.append(f"{prefix}{item.text}{enabled_indicator}")

        # Show description of selected item
        if 0 <= self.selected_index < len(self.items):
            desc = self.items[self.selected_index].description
            if desc:
                lines.append("")
                lines.append("-" * 60)
                lines.append(desc)

        return lines


class PartyMenu(Menu):
    """Menu for managing fish party"""

    def __init__(self, player, game_state=None, data_loader=None):
        """
        Initialize party menu

        Args:
            player: Player instance
        """
        super().__init__("PARTY MANAGEMENT")
        self.player = player
        self.rebuild_menu()

    def rebuild_menu(self):
        """Rebuild menu items based on current party"""
        self.items = []

        # Show active party
        if self.player.active_party:
            for i, fish in enumerate(self.player.active_party):
                status = "FAINTED" if fish.is_fainted() else "OK"
                item_text = f"{i+1}. {fish.name} (Lv.{fish.level}) - {fish.current_hp}/{fish.max_hp} HP [{status}]"
                description = f"Type: {fish.type} | ATK: {fish.get_effective_stat('atk')} DEF: {fish.get_effective_stat('def')} SPD: {fish.spd}"

                # Action: View/Switch/Heal
                self.add_item(MenuItem(
                    item_text,
                    action=lambda f=fish: self.fish_action_menu(f),
                    description=description
                ))
        else:
            self.add_item(MenuItem("No fish in party!", enabled=False))

        self.add_item(MenuItem(""))  # Spacer
        self.add_item(MenuItem("View Storage", action=self.view_storage))
        self.add_item(MenuItem("Party Stats", action=self.party_stats))
        self.add_item(MenuItem("Back", action=lambda: MenuResult.BACK))

    def fish_action_menu(self, fish) -> MenuResult:
        """
        Show actions for a specific fish

        Args:
            fish: The fish to show actions for

        Returns:
            MenuResult
        """
        print("\n" + "=" * 60)
        print(f"{fish.name} (Lv.{fish.level})".center(60))
        print("=" * 60)
        print(f"Type: {fish.type}")
        print(f"HP: {fish.current_hp}/{fish.max_hp}")
        print(f"ATK: {fish.get_effective_stat('atk')} DEF: {fish.get_effective_stat('def')} SPD: {fish.spd}")
        if fish.status_effects:
            print(f"Status: {', '.join(fish.status_effects)}")
        print("\nMoves:")
        for move in fish.known_moves:
            power = move.get("power", "-")
            print(f"- {move.get('name')} (Power: {power})")
        input("\nPress Enter to return...")
        return MenuResult.CONTINUE

    def view_storage(self) -> MenuResult:
        """View fish in storage"""
        print("\n" + "=" * 60)
        print("FISH STORAGE".center(60))
        print("=" * 60)

        if not self.player.fish_storage:
            print("No fish in storage.")
        else:
            for i, fish in enumerate(self.player.fish_storage, 1):
                status = "FAINTED" if fish.is_fainted() else "OK"
                print(f"{i}. {fish.name} (Lv.{fish.level}) - {fish.current_hp}/{fish.max_hp} HP [{status}]")

        input("\nPress Enter to return...")
        return MenuResult.CONTINUE

    def party_stats(self) -> MenuResult:
        """Show overall party statistics"""
        print("\n" + "=" * 60)
        print("PARTY STATS".center(60))
        print("=" * 60)

        party = self.player.active_party
        if not party:
            print("No active party members.")
        else:
            total_level = sum(fish.level for fish in party)
            total_hp = sum(fish.max_hp for fish in party)
            total_atk = sum(fish.get_effective_stat("atk") for fish in party)
            total_def = sum(fish.get_effective_stat("def") for fish in party)
            total_spd = sum(fish.spd for fish in party)
            count = len(party)
            print(f"Party Size: {count}")
            print(f"Average Level: {total_level // count}")
            print(f"Total Max HP: {total_hp}")
            print(f"Total ATK: {total_atk}")
            print(f"Total DEF: {total_def}")
            print(f"Total SPD: {total_spd}")

        input("\nPress Enter to return...")
        return MenuResult.CONTINUE


class InventoryMenu(Menu):
    """Menu for managing inventory"""

    def __init__(self, player):
        """
        Initialize inventory menu

        Args:
            player: Player instance
        """
        super().__init__("INVENTORY")
        self.player = player
        self.data_loader = get_data_loader()
        self.rebuild_menu()

    def rebuild_menu(self):
        """Rebuild menu based on current inventory"""
        self.items = []

        # Group items by category
        inventory = getattr(self.player, "bread_items", {})
        if inventory:
            self.add_item(MenuItem("=== BREAD ITEMS ===", enabled=False))

            for item_id, count in inventory.items():
                item_data = self.data_loader.get_item_by_id(item_id)
                item_name = item_data.get("name", item_id) if item_data else item_id
                description = ""
                if item_data:
                    flavor = item_data.get("flavor_text", {})
                    description = flavor.get("default", "")
                item_text = f"{item_name} x{count}"
                self.add_item(MenuItem(
                    item_text,
                    action=lambda id=item_id: self.use_item(id),
                    description=description or f"Use {item_name}"
                ))
        else:
            self.add_item(MenuItem("No items in inventory", enabled=False))

        self.add_item(MenuItem(""))

        # Show money
        self.add_item(MenuItem(
            f"Money: {self.player.money} denarii",
            enabled=False
        ))

        self.add_item(MenuItem(""))
        self.add_item(MenuItem("Back", action=lambda: MenuResult.BACK))

    def use_item(self, item_id: str) -> MenuResult:
        """
        Use an item from inventory

        Args:
            item_id: ID of item to use

        Returns:
            MenuResult
        """
        item_data = self.data_loader.get_item_by_id(item_id)
        if not item_data:
            print("That item does nothing.")
            input("Press Enter...")
            return MenuResult.CONTINUE

        if not self.player.has_item(item_id):
            print("You don't have that item.")
            input("Press Enter...")
            return MenuResult.CONTINUE

        if not self.player.active_party:
            print("No fish available.")
            input("Press Enter...")
            return MenuResult.CONTINUE

        target_fish = self.player.active_party[0]
        effect = item_data.get("effect", "")
        duration = int(item_data.get("duration", 0))

        if effect == "heal_hp":
            healed = target_fish.heal(int(item_data.get("power", 0)))
            print(f"{target_fish.name} restored {healed} HP!")
        elif effect == "heal_and_cure_poison":
            healed = target_fish.heal(int(item_data.get("power", 0)))
            target_fish.remove_status_effect("poisoned")
            print(f"{target_fish.name} restored {healed} HP and was cured!")
        elif effect == "heal_and_atk_boost":
            healed = target_fish.heal(int(item_data.get("heal_power", 0)))
            boost = float(item_data.get("atk_boost", 0)) / 100.0
            if boost > 0:
                target_fish.apply_stat_modifier("atk", 1.0 + boost, duration)
            print(f"{target_fish.name} restored {healed} HP and felt stronger!")
        elif effect == "full_heal_all":
            for fish in self.player.active_party:
                fish.heal(fish.max_hp)
                fish.clear_status_effects()
            print("All fish were fully healed!")
        elif effect == "atk_boost":
            boost = float(item_data.get("boost_percent", 0)) / 100.0
            if boost > 0:
                target_fish.apply_stat_modifier("atk", 1.0 + boost, duration)
            print(f"{target_fish.name}'s attack rose!")
        elif effect == "spd_boost":
            boost = float(item_data.get("boost_percent", 0)) / 100.0
            if boost > 0:
                target_fish.apply_stat_modifier("spd", 1.0 + boost, duration)
            print(f"{target_fish.name}'s speed rose!")
        elif effect == "def_boost":
            boost = float(item_data.get("boost_percent", 0)) / 100.0
            if boost > 0:
                target_fish.apply_stat_modifier("def", 1.0 + boost, duration)
            print(f"{target_fish.name}'s defense rose!")
        elif effect == "remove_all_debuffs":
            target_fish.clear_status_effects()
            target_fish.reset_stat_modifiers()
            print(f"{target_fish.name} was purified!")
        elif effect == "auto_revive":
            if target_fish.is_fainted():
                revive_hp = int(item_data.get("revive_hp", 1))
                target_fish.current_hp = max(1, revive_hp)
                print(f"{target_fish.name} was revived!")
            else:
                print("Nothing happened.")
        elif effect == "invincible":
            target_fish.apply_status_effect("invincible", duration)
            print(f"{target_fish.name} became invincible!")
        else:
            print("That item does nothing.")

        self.player.remove_bread_item(item_id, 1)
        self.rebuild_menu()
        input("Press Enter...")
        return MenuResult.CONTINUE


class ShopMenu(Menu):
    """Menu for shop interactions"""

    def __init__(self, player, shop_data: Dict[str, Any]):
        """
        Initialize shop menu

        Args:
            player: Player instance
            shop_data: Shop configuration (items, prices, etc.)
        """
        super().__init__(f"SHOP - {shop_data.get('name', 'General Store')}")
        self.player = player
        self.shop_data = shop_data
        self.mode = "buy"  # buy or sell
        self.data_loader = get_data_loader()
        self.rebuild_menu()

    def rebuild_menu(self):
        """Rebuild shop menu"""
        self.items = []

        self.add_item(MenuItem(
            f"Your Money: {self.player.money} denarii",
            enabled=False
        ))
        self.add_item(MenuItem(""))

        if self.mode == "buy":
            # Show items for sale
            items_for_sale = self.shop_data.get("items", [])

            for item in items_for_sale:
                item_id = item["id"]
                price = item["price"]
                stock = item.get("stock", "∞")

                can_afford = self.player.money >= price
                item_text = f"{item_id} - {price} denarii"
                if stock != "∞":
                    item_text += f" (Stock: {stock})"

                self.add_item(MenuItem(
                    item_text,
                    action=lambda id=item_id, p=price: self.buy_item(id, p),
                    enabled=can_afford,
                    description=item.get("description", "")
                ))
        else:
            # Show player items to sell
            inventory = getattr(self.player, "bread_items", {})
            for item_id, count in inventory.items():
                sell_price = self.get_sell_price(item_id)
                item_text = f"{item_id} x{count} - Sell for {sell_price} denarii"

                self.add_item(MenuItem(
                    item_text,
                    action=lambda id=item_id, p=sell_price: self.sell_item(id, p),
                    description=f"You have {count}"
                ))

        self.add_item(MenuItem(""))
        mode_text = "Switch to Sell" if self.mode == "buy" else "Switch to Buy"
        self.add_item(MenuItem(mode_text, action=self.toggle_mode))
        self.add_item(MenuItem("Leave Shop", action=lambda: MenuResult.BACK))

    def buy_item(self, item_id: str, price: int) -> MenuResult:
        """
        Buy an item

        Args:
            item_id: Item to buy
            price: Price of item

        Returns:
            MenuResult
        """
        if self.player.money >= price:
            self.player.add_money(-price)
            self.player.add_bread_item(item_id, 1)
            self.rebuild_menu()

        return MenuResult.CONTINUE

    def sell_item(self, item_id: str, price: int) -> MenuResult:
        """
        Sell an item

        Args:
            item_id: Item to sell
            price: Sell price

        Returns:
            MenuResult
        """
        if self.player.has_item(item_id):
            self.player.remove_bread_item(item_id, 1)
            self.player.add_money(price)
            self.rebuild_menu()

        return MenuResult.CONTINUE

    def toggle_mode(self) -> MenuResult:
        """Toggle between buy and sell mode"""
        self.mode = "sell" if self.mode == "buy" else "buy"
        self.rebuild_menu()
        return MenuResult.CONTINUE

    def get_sell_price(self, item_id: str) -> int:
        """
        Get sell price for an item

        Args:
            item_id: Item ID

        Returns:
            Sell price (typically 50% of buy price)
        """
        item_data = self.data_loader.get_item_by_id(item_id)
        if not item_data:
            return 0
        return max(1, int(item_data.get("cost", 0) * 0.5))


class MainMenu(Menu):
    """Main game menu"""

    def __init__(self, player, game_state=None, data_loader=None):
        """
        Initialize main menu

        Args:
            player: Player instance
        """
        super().__init__("MAIN MENU")
        self.player = player
        self.game_state = game_state
        self.data_loader = data_loader or get_data_loader()

        self.add_item(MenuItem(
            "Party",
            action=lambda: self.open_submenu(PartyMenu(self.player)),
            description="Manage your fish party"
        ))

        self.add_item(MenuItem(
            "Inventory",
            action=lambda: self.open_submenu(InventoryMenu(self.player)),
            description="View and use items"
        ))

        self.add_item(MenuItem(
            "Apostles",
            action=self.view_apostles,
            description="View recruited apostles"
        ))

        self.add_item(MenuItem(
            "Quests",
            action=self.view_quests,
            description="View active and completed quests"
        ))

        self.add_item(MenuItem(
            "Parables",
            action=self.view_parables,
            description="View collected parables"
        ))

        self.add_item(MenuItem(
            "Status",
            action=self.view_status,
            description="View Jesus's status and progress"
        ))

        self.add_item(MenuItem(""))

        self.add_item(MenuItem(
            "Save Game",
            action=self.save_game,
            description="Save your progress"
        ))

        self.add_item(MenuItem(
            "Settings",
            action=self.settings,
            description="Game settings"
        ))

        self.add_item(MenuItem(
            "Exit to Title",
            action=lambda: MenuResult.EXIT,
            description="Return to title screen"
        ))

    def open_submenu(self, submenu: Menu) -> MenuResult:
        """
        Open a submenu

        Args:
            submenu: Menu to open

        Returns:
            MenuResult
        """
        return submenu

    def view_apostles(self) -> MenuResult:
        """View apostles menu"""
        print("\n" + "=" * 60)
        print("APOSTLES".center(60))
        print("=" * 60)

        if not self.player.recruited_apostles:
            print("No apostles recruited yet.")
        else:
            for apostle_id in self.player.recruited_apostles:
                apostle_data = get_apostle(apostle_id)
                name = apostle_data.get("name", apostle_id) if apostle_data else apostle_id
                print(f"- {name} ({apostle_id})")

        input("\nPress Enter to return...")
        return MenuResult.CONTINUE

    def view_quests(self) -> MenuResult:
        """View quests menu"""
        print("\n" + "=" * 60)
        print("QUEST LOG".center(60))
        print("=" * 60)

        if not self.game_state:
            print("Quest data unavailable.")
            input("\nPress Enter to return...")
            return MenuResult.CONTINUE

        quests_data = self.data_loader.load_json("quests.json").get("quests", [])
        quest_names = {q.get("id", ""): q.get("name", "Unknown") for q in quests_data}

        print("Active Quests:")
        if self.game_state.active_quests:
            for quest_id in self.game_state.active_quests:
                print(f"- {quest_names.get(quest_id, quest_id)}")
        else:
            print("  None")

        print("\nCompleted Quests:")
        if self.game_state.completed_quests:
            for quest_id in self.game_state.completed_quests:
                print(f"- {quest_names.get(quest_id, quest_id)}")
        else:
            print("  None")

        input("\nPress Enter to return...")
        return MenuResult.CONTINUE

    def view_parables(self) -> MenuResult:
        """View collected parables"""
        print("\n" + "=" * 60)
        print("PARABLES".center(60))
        print("=" * 60)

        if not self.game_state:
            print("Parable data unavailable.")
            input("\nPress Enter to return...")
            return MenuResult.CONTINUE

        parables_data = self.data_loader.load_json("parables.json").get("parables", [])
        parable_names = {p.get("id", ""): p.get("name", "Unknown") for p in parables_data}

        if self.game_state.collected_parables:
            for parable_id in self.game_state.collected_parables:
                print(f"- {parable_names.get(parable_id, parable_id)}")
        else:
            print("No parables collected yet.")

        input("\nPress Enter to return...")
        return MenuResult.CONTINUE

    def view_status(self) -> MenuResult:
        """View player status"""
        print("\n" + "=" * 60)
        print("STATUS".center(60))
        print("=" * 60)

        print(f"Name: {self.player.name}")
        print(f"Level: {self.player.level}")
        print(f"HP: {self.player.current_hp}/{self.player.max_hp}")
        print(f"Money: {self.player.money} denarii")
        print(f"Miracle Meter: {self.player.miracle_meter:.1f}%")
        print(f"Battles Won: {self.player.battles_won}")
        print(f"Battles Lost: {self.player.battles_lost}")

        input("\nPress Enter to return...")
        return MenuResult.CONTINUE

    def save_game(self) -> MenuResult:
        """Save the game"""
        save_system = get_save_system()
        choice = input("Save slot (1-5): ").strip()
        try:
            slot = int(choice) if choice else 1
            if save_system.save_game(self.player, slot):
                print("Game saved!")
            else:
                print("Save failed.")
        except ValueError:
            print("Invalid slot.")

        input("Press Enter to continue...")
        return MenuResult.CONTINUE

    def settings(self) -> MenuResult:
        """Open settings menu"""
        print("\nSettings are not yet configurable in the text UI.")
        input("Press Enter to return...")
        return MenuResult.CONTINUE


class MenuManager:
    """Manages menu stack and navigation"""

    def __init__(self):
        """Initialize menu manager"""
        self.menu_stack: List[Menu] = []
        self.running = False

    def push_menu(self, menu: Menu):
        """
        Push a menu onto the stack

        Args:
            menu: Menu to push
        """
        self.menu_stack.append(menu)

    def pop_menu(self) -> Optional[Menu]:
        """
        Pop the current menu from the stack

        Returns:
            The popped menu, or None if stack is empty
        """
        if self.menu_stack:
            return self.menu_stack.pop()
        return None

    def current_menu(self) -> Optional[Menu]:
        """
        Get the current menu

        Returns:
            Current menu, or None if stack is empty
        """
        if self.menu_stack:
            return self.menu_stack[-1]
        return None

    def clear_menus(self):
        """Clear all menus from the stack"""
        self.menu_stack.clear()

    def handle_input(self, key: str) -> MenuResult:
        """
        Handle keyboard input

        Args:
            key: Key pressed (up, down, select, back, etc.)

        Returns:
            MenuResult
        """
        menu = self.current_menu()
        if not menu:
            return MenuResult.EXIT

        if key == "up":
            menu.move_up()
            return MenuResult.CONTINUE
        elif key == "down":
            menu.move_down()
            return MenuResult.CONTINUE
        elif key == "select":
            result = menu.select()

            # Handle special results
            if result == MenuResult.BACK:
                self.pop_menu()
                return MenuResult.CONTINUE
            elif result == MenuResult.EXIT:
                return MenuResult.EXIT
            elif isinstance(result, Menu):
                # If a menu is returned, push it onto the stack
                self.push_menu(result)
                return MenuResult.CONTINUE

            return MenuResult.CONTINUE
        elif key == "back":
            self.pop_menu()
            if not self.menu_stack:
                return MenuResult.EXIT
            return MenuResult.CONTINUE

        return MenuResult.CONTINUE

    def render(self) -> List[str]:
        """
        Render the current menu

        Returns:
            List of strings to display
        """
        menu = self.current_menu()
        if menu:
            return menu.get_display_text()
        return ["No menu active"]
