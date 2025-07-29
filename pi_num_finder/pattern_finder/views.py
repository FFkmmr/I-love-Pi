from django.shortcuts import render, get_object_or_404, redirect
from .models import PiMil
from .services import __main__
import os, sys, re

dpath = os.path.join(__main__.BASE_PATH, 'data/unsorted_billion/pi_billion_01/')

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
        pattern = request.POST.get('pattern')
        result = __main__.Main.process_files(pattern, dpath)
        request.session['search_result'] = result
        request.session['pattern'] = pattern
        return redirect('home')
    
    return redirect('home')






def pi_chunk_detail(request, mil_id):
    result = request.session.get('search_result')
    pattern = request.session.get('pattern')

    file_name = f'100millions_{mil_id - 1}.txt'
    file_path = os.path.join(dpath, file_name)

    match_index = int(request.GET.get('match_index', 1))
    pattern_pos_list = list(result[file_name]['matches'].values())
    match_pos = abs(mil_id * 100_000_000 - pattern_pos_list[match_index - 1] - 100_000_000)

    page_size = 1000
    start = max(0, match_pos - page_size // 2)

    with open(file_path, 'r') as f:
        f.seek(start)
        chunk = f.read(page_size)

    highlighted_chunk = re.sub(
        f'({re.escape(pattern)})',
        r'<span class="highlight">\1</span>',
        chunk
    )

    total_length_of_file = os.path.getsize(file_path)
    count_of_pages = total_length_of_file // page_size
    current_page = match_pos // page_size

    context = {
        'match_pos': match_pos,
        'result': result,
        'mil_id': mil_id,
        'count_of_find_patterns': result[file_name]['count'],
        'pattern': pattern,
        'highlighted_chunk': highlighted_chunk,
        'current_page': current_page,
        'count_of_pages': count_of_pages,
        'match_index': match_index,
        'has_next_match': match_index < len(pattern_pos_list),
        'has_prev_match': match_index > 1,
    }

    return render(request, 'pattern_finder/legacies/pi_chunk_details.html', context)
