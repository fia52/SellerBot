from datetime import datetime

from openpyxl import load_workbook


class ExcelFile:
    def __init__(
        self,
        filename: str = "/home/iliya/PycharmProjects/test_seller_bot/tgbot/data/orders.xlsx",
    ):
        self.filename = filename
        self.workbook = load_workbook(self.filename)
        self.worksheet = self.workbook["data"]

    async def put_in_excel(self, data):
        row = [
            data.get("order_id"),
            data.get("user_id"),
            data.get("item_id"),
            data.get("count"),
            data.get("address"),
            datetime.now().date(),
        ]

        self.worksheet.append(row)
        self.workbook.save(self.filename)

    async def close(self):
        self.workbook.close()
