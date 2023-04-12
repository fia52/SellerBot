from aiogram.utils.callback_data import CallbackData

pagination_call = CallbackData("paginator", "key", "page", "category_name")
show_next_level_data_call = CallbackData(
    "show_next_level_data_call", "next_level_name", "category_name"
)
add_to_shopping_cart_call = CallbackData("add_to_shopping_cart", "item_id")
choose_item_count_call = CallbackData("choose_item_count", "count")
make_order_call = CallbackData("make_order", "order_id")
delete_order_call = CallbackData("delete_order", "order_id")
