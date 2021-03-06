from django.shortcuts import render, redirect
from .models import Company, Trading, Bidding
from users.models import User
from .forms import TradeForm, BidForm, CompanyForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Share as var


def coming(request):
	return render(request, 'home/comingsoon.html')

def comingbidding(request):
	return render(request, 'home/comingsoon.html')

def home(request):
	context = {
		'Companys': Company.objects.all()
	}
	return render(request, 'home/index.html', context)

def timepage(request):
	return render(request, 'home/save.html')

def time(request):

	i = var.objects.all();
	print(i)
	for j in i:
		coin = j.shareholder.eCoins + j.percentage_of_share*j.company.multiplication_factor*10
		User.objects.filter(id = j.shareholder.id).update(eCoins = coin)
	return redirect('timepage')

@login_required()
def tradingUpdateView(request, id=None):
	if id:
		trade = Trading.objects.get(id = id)
		if request.method == 'POST':
			form = TradeForm(request.POST, instance=trade)
			if trade.highest_bid < int(form['highest_bid'].value()) and form.is_valid():
				trade.buyer = request.user
				form.save()
			else:
				messages.add_message(request, messages.INFO, 'Enter a Bid Price higher than the current Highest Bid Price')
			return redirect('trading')
	else:
		form = TradeForm()

	context = {
		'form':form	,
		'Tradings': Trading.objects.all(),
		'Companys': Company.objects.all(),
	}

	return render(request, 'home/trading.html', context)
	

@login_required()
def bidding(request, id=None):
	if id:
		bid = Bidding.objects.filter(id = id).first()
		if request.method == 'POST':
			form = BidForm(request.POST, instance=bid)
			if bid.bidding_price < int(form['bidding_price'].value()) and form.is_valid():
				bid.buyer = request.user
				form.save()
			else:
				messages.add_message(request, messages.INFO, 'Enter a Bid Price higher than the current Highest Bid Price')
			return redirect('bidding')
	else:
		form = BidForm()
	context = {
		'form' : form,
		'Bid': Bidding.objects.all(),
		'Companys': Company.objects.all()	
	}
	return render(request, 'home/letsbid.html', context)

def mycompanies(request, id=None):
	if id:
		current_share = var.objects.get(id = id)
		if request.method == 'POST':
			form = CompanyForm(request.POST)
			if int(form['percentage_for_sale'].value()) > 5 and int(form['percentage_for_sale'].value()) < 49 and form.is_valid():
				form.instance.company = current_share.company
				form.instance.your_bid_price = int(form['highest_bid'].value())
				form.save()
			else:
				messages.add_message(request, messages.INFO, 'You need to sell minimum 5 percent of Shares')
			return redirect('trading')
	else:
		form = CompanyForm()

	context = {
		'form' : form,
		'Shares': var.objects.filter(shareholder=request.user),
	}
	return render(request, 'home/mycompanies.html', context)

def newpage(request):
    return render(request, 'home/newpage.html')

