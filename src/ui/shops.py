"""
Shop System - Fishmonger and Baker shops
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from utils.data_loader import get_data_loader


@dataclass
class ShopItem:
    """Represents an item for sale in a shop"""
    id: str
    name: str
    price: int
    description: str
    stock: Optional[int] = None  # None = infinite stock
    level_requirement: int = 1
    region_requirement: Optional[str] = None


class Shop:
    """Base shop class"""

    def __init__(self,
                 shop_id: str,
                 name: str,
                 description: str,
                 greeting: str):
        """
        Initialize a shop

        Args:
            shop_id: Unique shop identifier
            name: Shop display name
            description: Shop description
            greeting: Shopkeeper greeting
        """
        self.shop_id = shop_id
        self.name = name
        self.description = description
        self.greeting = greeting
        self.inventory: List[ShopItem] = []
        self.buy_multiplier = 1.0  # Price multiplier for buying
        self.sell_multiplier = 0.5  # Multiplier for selling (50% of buy price)

    def add_item(self, item: ShopItem):
        """Add an item to shop inventory"""
        self.inventory.append(item)

    def get_items(self, player_level: int = 1, region: str = None) -> List[ShopItem]:
        """
        Get available items based on player progress

        Args:
            player_level: Player's current level
            region: Current region

        Returns:
            List of available shop items
        """
        available = []

        for item in self.inventory:
            # Check level requirement
            if item.level_requirement > player_level:
                continue

            # Check region requirement
            if item.region_requirement and item.region_requirement != region:
                continue

            # Check stock
            if item.stock is not None and item.stock <= 0:
                continue

            available.append(item)

        return available

    def purchase_item(self, item_id: str, player, quantity: int = 1) -> bool:
        """
        Purchase an item from the shop

        Args:
            item_id: ID of item to purchase
            player: Player instance
            quantity: Number to purchase

        Returns:
            True if purchase succeeded
        """
        # Find item
        item = None
        for shop_item in self.inventory:
            if shop_item.id == item_id:
                item = shop_item
                break

        if not item:
            return False

        # Check stock
        if item.stock is not None and item.stock < quantity:
            return False

        # Calculate total price
        total_price = int(item.price * self.buy_multiplier * quantity)

        # Check if player can afford
        if player.money < total_price:
            return False

        # Complete purchase
        player.add_money(-total_price)
        player.add_bread_item(item_id, quantity)

        # Update stock
        if item.stock is not None:
            item.stock -= quantity

        return True

    def sell_item(self, item_id: str, player, quantity: int = 1) -> bool:
        """
        Sell an item to the shop

        Args:
            item_id: ID of item to sell
            player: Player instance
            quantity: Number to sell

        Returns:
            True if sale succeeded
        """
        # Check if player has item
        if not player.has_item(item_id):
            return False

        # Find item in shop (to get base price)
        base_price = 10  # Default sell price

        for shop_item in self.inventory:
            if shop_item.id == item_id:
                base_price = shop_item.price
                break

        # Calculate sell price
        sell_price = int(base_price * self.sell_multiplier * quantity)

        # Complete sale
        player.remove_bread_item(item_id, quantity)
        player.add_money(sell_price)

        return True


class BakerShop(Shop):
    """Baker shop - sells bread items (healing and buffs)"""

    def __init__(self, town: str = "General"):
        """
        Initialize baker shop

        Args:
            town: Town name (affects inventory)
        """
        super().__init__(
            shop_id=f"baker_{town.lower()}",
            name=f"{town} Bakery",
            description="Fresh bread and baked goods",
            greeting="Welcome to the bakery! May I offer you the bread of life?"
        )

        # Stock basic items
        self.add_item(ShopItem(
            id="plain_pita",
            name="Plain Pita",
            price=20,
            description="Restores 30 HP",
            level_requirement=1
        ))

        self.add_item(ShopItem(
            id="ryedemption_roll",
            name="Ryedemption Roll",
            price=50,
            description="Restores 50 HP",
            level_requirement=5
        ))

        self.add_item(ShopItem(
            id="faith_bagel",
            name="Faith Bagel",
            price=80,
            description="Restores 80 HP and cures status effects",
            level_requirement=10
        ))

        self.add_item(ShopItem(
            id="whole_grain_grace",
            name="Whole Grain Grace",
            price=120,
            description="Restores 100 HP",
            level_requirement=15
        ))

        self.add_item(ShopItem(
            id="blessed_baguette",
            name="Blessed Baguette",
            price=150,
            description="Restores 150 HP to one fish",
            level_requirement=20
        ))

        self.add_item(ShopItem(
            id="manna_muffin",
            name="Manna Muffin",
            price=200,
            description="Restores 200 HP and grants ATK +20% for 3 turns",
            level_requirement=25
        ))

        self.add_item(ShopItem(
            id="pumpernickel_prayer",
            name="Pumpernickel Prayer",
            price=250,
            description="Restores all HP to one fish",
            level_requirement=30
        ))

        self.add_item(ShopItem(
            id="sourdough_salvation",
            name="Sourdough Salvation",
            price=300,
            description="Revives fainted fish with 50% HP",
            level_requirement=25
        ))

        self.add_item(ShopItem(
            id="challah_chosen",
            name="Challah of the Chosen",
            price=400,
            description="Fully heals entire party",
            level_requirement=35
        ))

        self.add_item(ShopItem(
            id="ciabatta_covenant",
            name="Ciabatta of the Covenant",
            price=500,
            description="Restores all HP and grants all stat boosts for 5 turns",
            level_requirement=40
        ))

        # Regional special items
        if town == "Cana":
            self.add_item(ShopItem(
                id="wedding_bread",
                name="Wedding Bread",
                price=100,
                description="Celebration bread that restores 120 HP",
                level_requirement=5,
                region_requirement="Coastal"
            ))

        elif town == "Jerusalem":
            self.add_item(ShopItem(
                id="passover_matzo",
                name="Passover Matzo",
                price=600,
                description="Unleavened bread of freedom. Grants immunity to status for 3 turns.",
                level_requirement=45,
                region_requirement="Jerusalem"
            ))

            self.add_item(ShopItem(
                id="last_supper_loaf",
                name="Last Supper Loaf",
                price=1000,
                description="This is my body, broken for you. Fully heals party and fills miracle meter.",
                level_requirement=50,
                stock=1,  # Only one available
                region_requirement="Jerusalem"
            ))


class FishmongerShop(Shop):
    """Fishmonger shop - buys fish and sells fishing supplies"""

    def __init__(self, town: str = "General"):
        """
        Initialize fishmonger shop

        Args:
            town: Town name
        """
        super().__init__(
            shop_id=f"fishmonger_{town.lower()}",
            name=f"{town} Fishmonger",
            description="Fresh fish and fishing supplies",
            greeting="Welcome! Looking to catch or sell some fish?"
        )

        # Fishing supplies
        self.add_item(ShopItem(
            id="basic_net",
            name="Basic Net",
            price=100,
            description="Increases fish catch rate by 10%",
            level_requirement=1
        ))

        self.add_item(ShopItem(
            id="quality_net",
            name="Quality Net",
            price=300,
            description="Increases fish catch rate by 20%",
            level_requirement=10
        ))

        self.add_item(ShopItem(
            id="miraculous_net",
            name="Miraculous Net",
            price=800,
            description="Increases fish catch rate by 40% and rare fish encounters",
            level_requirement=25
        ))

        # Fish food (for stat training)
        self.add_item(ShopItem(
            id="fish_food_hp",
            name="HP Pellets",
            price=150,
            description="Permanently increases a fish's HP by 5",
            level_requirement=15
        ))

        self.add_item(ShopItem(
            id="fish_food_atk",
            name="ATK Pellets",
            price=150,
            description="Permanently increases a fish's ATK by 3",
            level_requirement=15
        ))

        self.add_item(ShopItem(
            id="fish_food_def",
            name="DEF Pellets",
            price=150,
            description="Permanently increases a fish's DEF by 3",
            level_requirement=15
        ))

        self.add_item(ShopItem(
            id="fish_food_spd",
            name="SPD Pellets",
            price=150,
            description="Permanently increases a fish's SPD by 3",
            level_requirement=15
        ))

        # Held items for fish
        self.add_item(ShopItem(
            id="sea_shell",
            name="Sea Shell",
            price=200,
            description="Fish held item: +10% DEF",
            level_requirement=10
        ))

        self.add_item(ShopItem(
            id="coral_charm",
            name="Coral Charm",
            price=250,
            description="Fish held item: Restores 5% HP each turn",
            level_requirement=15
        ))

        self.add_item(ShopItem(
            id="pearl_necklace",
            name="Pearl Necklace",
            price=400,
            description="Fish held item: +15% SPD",
            level_requirement=20
        ))

        self.add_item(ShopItem(
            id="ancient_hook",
            name="Ancient Hook",
            price=500,
            description="Fish held item: +20% critical hit chance",
            level_requirement=25
        ))

        # Special regional items
        if town == "Galilee":
            self.add_item(ShopItem(
                id="galilean_special",
                name="Galilean Fish Food",
                price=100,
                description="Hometown special! All stats +1",
                level_requirement=1,
                region_requirement="Galilee"
            ))

        elif town == "Tiberias":
            self.add_item(ShopItem(
                id="royal_bait",
                name="Royal Bait",
                price=600,
                description="Attracts rare fish. +30% rare encounter rate.",
                level_requirement=30,
                region_requirement="Coastal"
            ))

    def buy_fish(self, fish_id: str, fish_level: int, player) -> bool:
        """
        Buy a fish from the player

        Args:
            fish_id: Fish ID
            fish_level: Fish level (affects price)
            player: Player instance

        Returns:
            True if purchase succeeded
        """
        # Calculate fish value based on level and rarity
        base_value = 50
        level_bonus = fish_level * 10

        data_loader = get_data_loader()
        fish_data = data_loader.get_fish_by_id(fish_id)
        tier = fish_data.get("tier") if fish_data else 1

        rarity_multiplier = 1.0
        if tier == 2:
            rarity_multiplier = 1.5
        elif tier == 3:
            rarity_multiplier = 2.0
        elif str(tier).lower() == "special":
            rarity_multiplier = 3.0

        total_value = int((base_value + level_bonus) * rarity_multiplier)

        player.add_money(total_value)

        return True


# Pre-configured shops for major towns
TOWN_SHOPS = {
    "Nazareth": {
        "baker": BakerShop("Nazareth"),
        "fishmonger": FishmongerShop("Nazareth")
    },
    "Cana": {
        "baker": BakerShop("Cana"),
        "fishmonger": FishmongerShop("Cana")
    },
    "Capernaum": {
        "baker": BakerShop("Capernaum"),
        "fishmonger": FishmongerShop("Capernaum")
    },
    "Bethsaida": {
        "baker": BakerShop("Bethsaida"),
        "fishmonger": FishmongerShop("Bethsaida")
    },
    "Magdala": {
        "baker": BakerShop("Magdala"),
        "fishmonger": FishmongerShop("Magdala")
    },
    "Chorazin": {
        "baker": BakerShop("Chorazin"),
        "fishmonger": FishmongerShop("Chorazin")
    },
    "Tiberias": {
        "baker": BakerShop("Tiberias"),
        "fishmonger": FishmongerShop("Tiberias")
    },
    "Gadara": {
        "baker": BakerShop("Gadara"),
        "fishmonger": FishmongerShop("Gadara")
    },
    "Samaria": {
        "baker": BakerShop("Samaria"),
        "fishmonger": FishmongerShop("Samaria")
    },
    "Jericho": {
        "baker": BakerShop("Jericho"),
        "fishmonger": FishmongerShop("Jericho")
    },
    "Bethany": {
        "baker": BakerShop("Bethany"),
        "fishmonger": FishmongerShop("Bethany")
    },
    "Bethlehem": {
        "baker": BakerShop("Bethlehem"),
        "fishmonger": FishmongerShop("Bethlehem")
    },
    "Jerusalem": {
        "baker": BakerShop("Jerusalem"),
        "fishmonger": FishmongerShop("Jerusalem")
    }
}


def get_shop(town: str, shop_type: str = "baker") -> Optional[Shop]:
    """
    Get a shop instance for a town

    Args:
        town: Town name
        shop_type: "baker" or "fishmonger"

    Returns:
        Shop instance or None
    """
    if town in TOWN_SHOPS and shop_type in TOWN_SHOPS[town]:
        return TOWN_SHOPS[town][shop_type]
    return None
