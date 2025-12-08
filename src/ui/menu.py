"""
Menu System - Interactive UI for party, inventory, and game management
"""

from typing import List, Dict, Any, Optional, Callable
from enum import Enum


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

    def __init__(self, player):
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
        # TODO: Implement fish-specific actions
        # - View details
        # - Switch position
        # - Use item on fish
        # - View moves
        return MenuResult.CONTINUE

    def view_storage(self) -> MenuResult:
        """View fish in storage"""
        # TODO: Implement storage viewing
        return MenuResult.CONTINUE

    def party_stats(self) -> MenuResult:
        """Show overall party statistics"""
        # TODO: Show aggregate party stats
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
        self.rebuild_menu()

    def rebuild_menu(self):
        """Rebuild menu based on current inventory"""
        self.items = []

        # Group items by category
        if self.player.bread_inventory:
            self.add_item(MenuItem("=== BREAD ITEMS ===", enabled=False))

            for item_id, count in self.player.bread_inventory.items():
                # TODO: Load item data to get name and description
                item_text = f"{item_id} x{count}"
                self.add_item(MenuItem(
                    item_text,
                    action=lambda id=item_id: self.use_item(id),
                    description=f"Use {item_id}"
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
        # TODO: Implement item usage
        # - Select target fish
        # - Apply item effect
        # - Update inventory
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
            for item_id, count in self.player.bread_inventory.items():
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
        # TODO: Look up item buy price and return 50%
        return 10  # Placeholder


class MainMenu(Menu):
    """Main game menu"""

    def __init__(self, player):
        """
        Initialize main menu

        Args:
            player: Player instance
        """
        super().__init__("MAIN MENU")
        self.player = player

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
        # TODO: Implement submenu handling
        return MenuResult.CONTINUE

    def view_apostles(self) -> MenuResult:
        """View apostles menu"""
        # TODO: Implement apostles viewing
        return MenuResult.CONTINUE

    def view_quests(self) -> MenuResult:
        """View quests menu"""
        # TODO: Implement quest log
        return MenuResult.CONTINUE

    def view_parables(self) -> MenuResult:
        """View collected parables"""
        # TODO: Implement parable collection viewer
        return MenuResult.CONTINUE

    def view_status(self) -> MenuResult:
        """View player status"""
        # TODO: Show player stats, progress, etc.
        return MenuResult.CONTINUE

    def save_game(self) -> MenuResult:
        """Save the game"""
        # TODO: Implement save system
        return MenuResult.CONTINUE

    def settings(self) -> MenuResult:
        """Open settings menu"""
        # TODO: Implement settings
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
