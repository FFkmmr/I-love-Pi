from django.shortcuts import render, get_object_or_404, redirect
from .models import PiMil
from .services import __main__
import os, sys


def home_page(request):
    result = request.session.get('search_result')
    if result:
        context = {
            'result': result,
        }
    else:
        context = {
        }
    return render(request,'pattern_finder/legacies/search_page.html', context)


def pi_search(request):
    if request.method == 'POST':
                                    #  TEST       
        # dpath = os.path.join(__main__.BASE_PATH, 'data/TEST_trillion_000/billion_000') 
                        #  PROD 
        # dpath = os.path.join(__main__.BASE_PATH, 'data/unsorted_trillions/trillion_00/200billions_0/')
        dpath = os.path.join(__main__.BASE_PATH, 'data/unsorted_billions/pi_billion_00/')
        pattern = request.POST.get('pattern')

        result = __main__.Main.process_files(pattern, dpath)
        request.session['search_result'] = result
        request.session['pattern'] = pattern
        return redirect('home')
    
    return redirect('home')


def pi_chunk_detail(request, mil_id):
    result = request.session.get('search_result')
    pattern = request.session.get('pattern')
    count_of_find_patterns = result[f'pi_200mil_{mil_id}m.txt']['count']
    
    context = {
        'result': result,
        'mil_id': mil_id,
        'count_of_find_patterns': count_of_find_patterns,
        'pattern': pattern,

    }
    return render(request, 'pattern_finder/legacies/pi_chunk_details.html', context)
