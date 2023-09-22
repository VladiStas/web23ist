from django.shortcuts import render


def index(request):
    context = {
        'products': ['Яблоко', 'Банан', 'Апельсин'],
    }
    return render(request, 'webapp/index.html', context)
