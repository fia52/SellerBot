import math

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callback_datas import (
    pagination_call,
    show_next_level_data_call,
    add_to_shopping_cart_call,
    choose_item_count_call,
    make_order_call,
    delete_order_call,
)

required_chats = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="group", url="https://t.me/+4W3P5znpCY5lODhi"),
            InlineKeyboardButton(text="chanel", url="https://t.me/test_sseller_bot"),
        ]
    ]
)

main_menu = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Каталог", callback_data="catalog"),
            InlineKeyboardButton(text="Корзина", callback_data="shopping_cart"),
            InlineKeyboardButton(text="FAQ", switch_inline_query_current_chat="FAQ"),
        ]
    ],
)

confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="Да"),
            InlineKeyboardButton(text="Нет", callback_data="Нет"),
        ]
    ]
)


def get_shopping_cart_keyboard(order_id: int):
    shopping_cart_keyboard = InlineKeyboardMarkup(row_width=1)
    make_order_button = InlineKeyboardButton(
        text="Сделать заказ", callback_data=make_order_call.new(order_id=order_id)
    )
    delete_button = InlineKeyboardButton(
        text="Удалить", callback_data=delete_order_call.new(order_id=order_id)
    )
    shopping_cart_keyboard.insert(make_order_button).insert(delete_button)
    return shopping_cart_keyboard


def get_add_to_shopping_cart_keyboard(item_id: int):
    add_to_shopping_cart = InlineKeyboardMarkup()
    add_button = InlineKeyboardButton(
        "Добавить в корзину",
        callback_data=add_to_shopping_cart_call.new(item_id=item_id),
    )
    add_to_shopping_cart.insert(add_button)
    return add_to_shopping_cart


def get_choose_item_count_keyboard():
    choose_item_count_keyboard = InlineKeyboardMarkup(row_width=2)
    for i in range(1, 11):
        choose_item_count_keyboard.insert(
            InlineKeyboardButton(
                text=f"{i} шт.", callback_data=choose_item_count_call.new(count=i)
            )
        )
    return choose_item_count_keyboard


def get_pages_keyboard(
    array: list,
    key: str,
    page: int = 1,
    next_level_name: str = "empty",
    category_name: str = "empty",
):
    markup = InlineKeyboardMarkup(row_width=1)
    max_items_per_page = 3
    first_item_index = (page - 1) * max_items_per_page
    last_item_index = page * max_items_per_page

    sliced_array = array[first_item_index:last_item_index]
    category_buttons = list()

    for category in sliced_array:
        category_buttons.append(
            InlineKeyboardButton(
                text=category,
                callback_data=show_next_level_data_call.new(
                    next_level_name=next_level_name, category_name=category
                ),
            )
        )

    pages_buttons = list()
    first_page = 1
    first_page_text = "<< 1"
    max_page = math.ceil(len(array) / max_items_per_page)
    max_page_text = f"{max_page} >>"

    # pages_buttons.append(
    #     InlineKeyboardButton(
    #         text=first_page_text,
    #         callback_data=pagination_call.new(key=key,
    #                                           page=first_page)
    #     )
    # )

    previous_page = page - 1
    previous_page_text = "<< "

    current_page_text = f"<{page}>"

    next_page = page + 1
    next_page_text = " >>"

    if previous_page >= first_page:
        pages_buttons.append(
            InlineKeyboardButton(
                text=previous_page_text,
                callback_data=pagination_call.new(
                    key=key, page=previous_page, category_name=category_name
                ),
            )
        )
    else:
        pages_buttons.append(
            InlineKeyboardButton(
                text=" . ",
                callback_data=pagination_call.new(
                    key=key, page="empty", category_name=category_name
                ),
            )
        )

    pages_buttons.append(
        InlineKeyboardButton(
            text=current_page_text,
            callback_data=pagination_call.new(
                key=key, page="empty", category_name=category_name
            ),
        )
    )

    if next_page <= max_page:
        pages_buttons.append(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=pagination_call.new(
                    key=key, page=next_page, category_name=category_name
                ),
            )
        )
    else:
        pages_buttons.append(
            InlineKeyboardButton(
                text=" . ",
                callback_data=pagination_call.new(
                    key=key, page="empty", category_name=category_name
                ),
            )
        )

    # pages_buttons.append(
    #     InlineKeyboardButton(
    #         text=max_page_text,
    #         callback_data=pagination_call.new(key=key,
    #                                           page=max_page)
    #     )
    # )

    for button in category_buttons:
        markup.insert(button)

    markup.row(*pages_buttons)

    return markup
