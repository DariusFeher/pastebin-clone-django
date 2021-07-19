from datetime import datetime

import pytz
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .forms import PastebinForm
from .models import PastebinClone

# Create your views here.

def clone_pastebin_create(request):
	if request.method == "POST":
		form = PastebinForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			pastebin = PastebinClone(
				title=cd['title'],
				body=cd['body']
			)
			pastebin.save()
			detail_page = pastebin.get_absolute_url()
			return redirect(detail_page)
		else:
			return render(request, 'newPastebin.html', {'form': form})
	form = PastebinForm()
	template = 'newPastebin.html'
	context = {'form': form}
	return render(request, template, context)

def clone_pastebin_edit(request, pk):
	pastebin = get_object_or_404(PastebinClone, pk=pk)
	if request.method == "POST":
		form = PastebinForm(request.POST)
		print(form.is_valid())
		if form.is_valid():
			cd = form.cleaned_data
			if (cd['title'] != pastebin.title or cd['body'] != pastebin.body):
				PastebinClone.objects.filter(pk=pk).update(
					title=cd['title'],
					body=cd['body'],
					updated=datetime.now(pytz.timezone('Europe/Bucharest'))
				)
			detail_page = pastebin.get_absolute_url()
			return redirect(detail_page)
		else:
			return render(request, 'editPastebin.html', {'form': form})
	else:
		template = 'editPastebin.html'
		form = PastebinForm(instance=pastebin)
		context = {"form": form, 'object': pastebin}
		return render(request, template, context)

def clone_pastebin_delete(request, pk):
	pastebin = get_object_or_404(PastebinClone, pk=pk)
	if request.method == 'POST':
		pastebin.delete()
		return redirect('/')
	return render(request, 'main.html')


class PastebinsView(ListView):
	model = PastebinClone
	template_name = 'main.html'

class PastebinDetailView(DetailView):
	model = PastebinClone
	template_name = 'detail.html'
