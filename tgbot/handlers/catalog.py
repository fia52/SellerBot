from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from loader import db
from tgbot.keyboards.callback_datas import (
    pagination_call,
    show_next_level_data_call,
    add_to_shopping_cart_call,
    choose_item_count_call,
)
from tgbot.keyboards.inline import (
    main_menu,
    get_pages_keyboard,
    get_add_to_shopping_cart_keyboard,
    get_choose_item_count_keyboard,
    confirm_keyboard,
)


class CatalogFSM(StatesGroup):
    waiting_category_name = State()
    waiting_subcategory_name = State()


async def show_categories(callback: CallbackQuery):
    await callback.answer()
    array = await db.select_categories()
    await callback.message.answer(
        text="Добро пожаловать в каталог товаров, выберите интересующую вас категорию:",
        reply_markup=get_pages_keyboard(
            array=array, key="categories", next_level_name="subcategories"
        ),
    )
    await CatalogFSM.waiting_category_name.set()


async def show_chosen_category_page(callback: CallbackQuery, callback_data: dict):
    await callback.answer()
    current_page = int(callback_data.get("page"))
    array = await db.select_categories()
    markup = get_pages_keyboard(
        array=array,
        page=current_page,
        key="categories",
        next_level_name="subcategories",
    )
    await callback.message.edit_reply_markup(reply_markup=markup)


async def show_subcategories(
    callback: CallbackQuery, callback_data: dict, state: FSMContext
):
    await callback.answer()
    category_name = callback_data.get("category_name")

    async with state.proxy() as data:
        data["category_name"] = category_name

    array = await db.select_subcategories(category=category_name)
    markup = get_pages_keyboard(
        array=array,
        key="subcategories",
        next_level_name="items",
        category_name=category_name,
    )

    await callback.message.edit_reply_markup(reply_markup=markup)
    await CatalogFSM.next()


async def show_chosen_subcategory_page(callback: CallbackQuery, callback_data: dict):
    await callback.answer()
    current_page = int(callback_data.get("page"))
    category_name = callback_data.get("category_name")
    array = await db.select_subcategories(category=category_name)
    markup = get_pages_keyboard(
        array=array,
        page=current_page,
        key="subcategories",
        next_level_name="items",
        category_name=category_name,
    )
    await callback.message.edit_reply_markup(reply_markup=markup)


async def show_items(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()

    subcategory = callback_data.get("category_name")
    async with state.proxy() as data:
        category = data.get("category_name")

    items = await db.select_items(category=category, subcategory=subcategory)

    for item in items:
        await callback.message.bot.send_photo(
            callback.from_user.id, photo=item.get("photo_id")
        )
        await callback.message.answer(
            item.get("description"),
            reply_markup=get_add_to_shopping_cart_keyboard(item_id=item.get("item_id")),
        )

    await state.finish()


class AddToShoppingCartFSM(StatesGroup):
    waiting_for_item_count = State()
    waiting_for_confirm = State()


async def obtain_item_id(
    callback: CallbackQuery, callback_data: dict, state: FSMContext
):
    await callback.answer()
    await AddToShoppingCartFSM.waiting_for_item_count.set()

    async with state.proxy() as data:
        data["item_id"] = callback_data.get("item_id")

    markup = get_choose_item_count_keyboard()

    await callback.message.edit_reply_markup(reply_markup=markup)


async def obtain_item_count(
    callback: CallbackQuery, callback_data: dict, state: FSMContext
):
    await callback.answer()

    async with state.proxy() as data:
        data["count"] = callback_data.get("count")
        item = await db.select_one_item(item_id=int(data["item_id"]))
        count = data.get("count")

    description = item.get("description")

    await callback.message.edit_text(
        text=f"Добавить: {description} в количестве {count} шт. в корзину?"
    )
    await callback.message.edit_reply_markup(reply_markup=confirm_keyboard)

    await AddToShoppingCartFSM.next()


async def obtain_confirm(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    if callback.data == "Да":
        async with state.proxy() as data:
            await db.add_order(
                user_id=callback.from_user.id,
                item_id=int(data.get("item_id")),
                count=int(data.get("count")),
            )

        await callback.message.answer(
            text="Добавлено в корзину!", reply_markup=main_menu
        )

    else:
        await callback.message.answer(text="хорошо(", reply_markup=main_menu)

    await state.finish()


def register_catalog(dp: Dispatcher):
    dp.register_callback_query_handler(
        show_categories, lambda x: x.data and x.data == "catalog", state="*"
    ),
    dp.register_callback_query_handler(
        show_chosen_category_page,
        pagination_call.filter(key="categories"),
        state=CatalogFSM.waiting_category_name,
    )
    dp.register_callback_query_handler(
        show_subcategories,
        show_next_level_data_call.filter(next_level_name="subcategories"),
        state=CatalogFSM.waiting_category_name,
    )
    dp.register_callback_query_handler(
        show_chosen_subcategory_page,
        pagination_call.filter(key="subcategories"),
        state=CatalogFSM.waiting_subcategory_name,
    )
    dp.register_callback_query_handler(
        show_items,
        show_next_level_data_call.filter(next_level_name="items"),
        state=CatalogFSM.waiting_subcategory_name,
    )
    dp.register_callback_query_handler(
        obtain_item_id, add_to_shopping_cart_call.filter(), state="*"
    )
    dp.register_callback_query_handler(
        obtain_item_count,
        choose_item_count_call.filter(),
        state=AddToShoppingCartFSM.waiting_for_item_count,
    )
    dp.register_callback_query_handler(
        obtain_confirm,
        lambda x: x.data and x.data in ["Да", "Нет"],
        state=AddToShoppingCartFSM.waiting_for_confirm,
    )
