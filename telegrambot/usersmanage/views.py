from django.shortcuts import render
from django.views import View
from tgbot.misc.sendall import sendall


class SendMessage(View):
    async def get(self, request):
        return render(request, "usersmanage/message_text.html")

    async def post(self, request):
        message_text = request.POST.get("text")
        await sendall(message_text)
        return render(request, "usersmanage/success_message.html")
