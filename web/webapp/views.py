from django.shortcuts import render, redirect


def index(request):
    context = {
        'products': ['Яблоко', 'Банан', 'Апельсин'],
    }
    return render(request, 'webapp/index.html', context)

def profile(request):
    return render(request, 'webapp/profile.html')


def authorization(request):
    if request.method == 'POST':
        return redirect('profile')
    else:
        return render(request, 'webapp/authorization.html')
