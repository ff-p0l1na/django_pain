import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
# from random import choice
from .models import FlashCard
from .forms import FlashCardAdder, FlashCardForm


def add_flashcard(request):
    submitted = False
    if request.method == "POST":
        form = FlashCardAdder(request.POST)
        if form.is_valid():
            FlashCard = form.save(commit=False)
            FlashCard.author = request.user
            form.save()
            return HttpResponseRedirect('/dodaj_fiszke?submitted=True')
    else:
        form = FlashCardAdder
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'flashcards/add_flashcard.html', {'form': form, 'submitted': submitted,})


@login_required
def all_flashcards(request):
    fc_list = FlashCard.objects.filter(author=request.user)
    return render(request, 'flashcards/fc_list.html',
                  {'fc_list': fc_list})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    if request.user.is_authenticated:
        name = request.user.username
    else:
        name = "Nieznajomy"
    month = month.title()
    # miesiac na cyfre
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # kalendarz
    cal = HTMLCalendar().formatmonth(year, month_number)

    # obecny rok
    now = datetime.now()
    current_year = now.year

    # godzina
    time = now.strftime('%H:%M')

    return render(request,
                  'flashcards/home.html', {'name': name,
                                'year': year,
                                'month': month,
                                'month_number': month_number,
                                'cal': cal,
                                'current_year': current_year,
                                'time': time,
                                })


# def quiz(request):
#     if request.method == 'POST':
#         form = FlashCardForm(request.POST)
#         if form.is_valid():
#             flashcard_id = request.session.get('flashcard_id')
#             flashcard = get_object_or_404(FlashCard, id=flashcard_id)
#             user_answer = form.cleaned_data['back']
#             if user_answer.lower() == flashcard.back.lower():
#                 message = f"Dobrze! Poprawna odpowiedź to: {user_answer}."
#             else:
#                 message = f"Błąd. Poprawna odpowiedź to: {flashcard.back}."
#             request.session['quiz_message'] = message
#             request.session['quiz_answer'] = flashcard.back
#             return redirect('quiz_res')
#     else:
#         flashcard = FlashCard.objects.order_by('?').first()
#         request.session['flashcard_id'] = flashcard.id
#         form = FlashCardForm()
#     context = {
#         'flashcard': flashcard,
#         'form': form,
#     }
#     return render(request, 'flashcards/quiz.html', context)

def quiz(request):
    if request.method == 'POST':
        form = FlashCardForm(request.POST)
        if form.is_valid():
            flashcard_id = request.session.get('flashcard_id')
            flashcard = get_object_or_404(FlashCard, id=flashcard_id)
            user_answer = form.cleaned_data['back']
            if user_answer.lower() == flashcard.back.lower():
                message = f"Dobrze! Poprawna odpowiedź to: {user_answer}."
            else:
                message = f"Błąd. Poprawna odpowiedź to: {flashcard.back}."
            request.session['quiz_message'] = message
            request.session['quiz_answer'] = flashcard.back
            return redirect('quiz_res')
    else:
        flashcard = FlashCard.objects.order_by('?').first()
        request.session['flashcard_id'] = flashcard.id
        form = FlashCardForm()
    context = {
        'flashcard': flashcard,
        'form': form,
    }
    return render(request, 'flashcards/quiz.html', context)


def quiz_res(request):
    # request session pop - do czyszczenia danych sesji
    message = request.session.pop('quiz_message', None)
    if message is None:
        return redirect('quiz')

    context = {'message': message}
    return render(request, 'flashcards/quiz_res.html', context)




