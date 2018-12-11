from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from customUser.models import CustomUser, Transactions
from mainGameApp.models import SportBet, UserBet


def getBets():
    sportBets = SportBet.objects.filter(status=-1)
    print(sportBets)
    if sportBets.count() > 0:
        return [[singleBet.id, singleBet.name, singleBet.w1, singleBet.d, singleBet.w2] for
                singleBet in
                sportBets.order_by('id')]


def homeView(request):
    content = {
        'content': 'Hello GUYS!'
    }
    return render(request, 'home.html', content)


def game(request):
    sendValues = {}
    if request.user.is_authenticated:
        userObj = request.user
        userBalance = request.user.balance
        sendValues = {'userBalance': userBalance,
                      'username': userObj.username,
                      'is_valid': False,
                      'betsList': getBets(),
                      }

    if request.is_ajax():
        sendValues['is_valid'] = True
        sendValues['betsList'] = getBets()

        return JsonResponse(sendValues)

    return render(request, 'game.html', sendValues)


def fillCashView(request):
    if request.POST.get('pay') == 'Pay':
        amount = int(request.POST.get('fillBalance'))
        userBalance = request.user.balance
        Transactions.objects.create(user=request.user, amount=amount)
        CustomUser.objects.select_for_update().filter(id=request.user.id).update(balance=userBalance + amount)
        return redirect('home')

    return render(request, 'fillCash.html', {})


def withdrawCashView(request):
    if request.POST.get('Withdraw') == 'Withdraw':
        amount = int(request.POST.get('withdrawBalance'))
        userBalance = request.user.balance
        Transactions.objects.create(user=request.user, amount=amount * -1)
        CustomUser.objects.select_for_update().filter(id=request.user.id).update(balance=userBalance - amount)
        return redirect('home')

    return render(request, 'withdrawBalance.html', {})


def makeBet(request):
    if request.user.is_authenticated:
        betValue = request.POST['betValue']
        betID = request.POST['betID']
        betRes = request.POST['res']
        betObj = SportBet.objects.get(id=int(betID))

        if not betObj.status == -1:
            return render(request, '404.html', {})

        coef = 1
        if betRes == '1':
            coef = betObj.w1
        if betRes == '0':
            coef = betObj.d
        if betRes == '2':
            coef = betObj.w2

        userBalance = request.user.balance - int(betValue)
        CustomUser.objects.select_for_update().filter(id=request.user.id).update(balance=userBalance)
        UserBet.objects.create(user=request.user, bet=betObj, coefficient=coef, status=0, side=int(betRes),
                               betValue=int(betValue))

        return JsonResponse({
            'is_valid': True,
            'userBalance': userBalance,
        })
    return render(request, '404.html', {})


def closeBet(request):
    if request.user.is_staff:
        sendValues = {'betsList': getBets(),
                      'username': request.user.username,
                      'is_valid': False,
                      }
        if request.is_ajax():
            sendValues['is_valid'] = True
            betRes = int(request.POST['res'])
            betID = int(request.POST['betID'])

            if SportBet.objects.filter(id=betID):
                betObj = SportBet.objects.get(id=betID)
                userBets = UserBet.objects.filter(bet=betObj).order_by('id')
                SportBet.objects.filter(id=betID).update(status=betRes)

                wonUsers = UserBet.objects.filter(bet=betObj, side=betRes)
                wonUsers.select_for_update().update(status=1)
                UserBet.objects.select_for_update().filter(bet=betObj).filter(~Q(side=betRes)).update(status=2)

                for eachUser in wonUsers.values('user', 'betValue', 'coefficient'):
                    winner = CustomUser.objects.get(id=eachUser['user'])
                    userBalance = winner.balance + eachUser['coefficient'] * eachUser['betValue']
                    CustomUser.objects.select_for_update().filter(id=eachUser['user']).update(balance=userBalance)
            return JsonResponse({
                'is_valid': True,
            })
        return render(request, 'closeBet.html', sendValues)


def betHistory(request):
    sendValues = {'username': request.user.username}
    userBets = UserBet.objects.filter(user=request.user).order_by('id')
    sendValues['betHistory'] = list(userBets)
    return render(request, 'betHistory.html', sendValues)

