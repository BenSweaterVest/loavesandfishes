class_name ShopSystem
extends Node

signal transaction_completed(success: bool, message: String)

func buy_item(item_id: String, cost: int, quantity: int = 1) -> void:
	var player = GameState.player
	if not player:
		transaction_completed.emit(false, "No player available.")
		return

	var total_cost = cost * quantity
	if player.money < total_cost:
		transaction_completed.emit(false, "Not enough denarii.")
		return

	player.add_money(-total_cost)
	player.add_bread_item(item_id, quantity)
	transaction_completed.emit(true, "Purchase successful.")

func sell_item(item_id: String, value: int, quantity: int = 1) -> void:
	var player = GameState.player
	if not player:
		transaction_completed.emit(false, "No player available.")
		return

	if not player.has_item(item_id, quantity):
		transaction_completed.emit(false, "You don't have that item.")
		return

	player.remove_bread_item(item_id, quantity)
	player.add_money(value * quantity)
	transaction_completed.emit(true, "Sale successful.")

func donate_money(amount: int) -> void:
	var player = GameState.player
	if not player:
		transaction_completed.emit(false, "No player available.")
		return
	if amount <= 0:
		transaction_completed.emit(false, "Invalid donation amount.")
		return
	if player.money < amount:
		transaction_completed.emit(false, "Not enough denarii.")
		return

	player.add_money(-amount)
	var current = int(GameState.story_flags.get("donated_money", 0))
	GameState.story_flags["donated_money"] = current + amount
	if QuestManager:
		for quest_id in GameState.active_quests:
			QuestManager.advance_quest(quest_id)

	transaction_completed.emit(true, "Donation successful.")
