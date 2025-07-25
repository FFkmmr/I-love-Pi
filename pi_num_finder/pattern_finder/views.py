from django.shortcuts import render, get_object_or_404, redirect
from .models import PiMil
from .services import __main__
import os, sys


def home_page(request):
    result = request.session.get('search_result')
    chunks = PiMil.objects.order_by('mil_number')
    if result:
        context = {
            'result': result,
            'chunks': chunks
        }
    else:
        context = {
            'chunks': chunks
        }
    return render(request,'pattern_finder/legacies/search_page.html', context)


def pi_search(request):
    if request.method == 'POST':
       
        dpath = os.path.join(__main__.BASE_PATH, 'data')
        pattern = request.POST.get('pattern')

        result = __main__.Main.process_files(pattern, dpath)
        request.session['search_result'] = result
        return redirect('home')
    
    return redirect('home')


def pi_chunk_detail(request, mil_number):
    chunk = get_object_or_404(PiMil, mil_number=mil_number)



    context = {

        'chunk': chunk
    }
    return render(request, 'pi_chunk_detail.html', context)
