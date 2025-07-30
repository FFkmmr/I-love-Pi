from django.shortcuts import render, redirect
from .services import __main__
import os, sys, re

dpath = os.path.join(__main__.BASE_PATH, 'data/unsorted_billion/pi_billion_01/')



def home_page(request):
    result = request.session.get('search_result')
    file_entries = []

    if result:
        for filename, data in result.items():
            if filename.endswith('.txt'):
                match = re.search(r'_(\d+)\.txt', filename)
                if match:
                    file_number = int(match.group(1))
                    file_entries.append((file_number, filename, data))

        context = {
            'file_entries': file_entries,
        }
    else:
        context = {}

    return render(request, 'pattern_finder/legacies/search_page.html', context)


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
 
    keys = [key for key in result.keys()]
    file_name = keys[mil_id - 1]

    match = re.search(r'_(\d+)\.txt', file_name)
    file_number = int(match.group(1))
    file_path = os.path.join(dpath, file_name)



    match_index = int(request.GET.get('match_index', 1))
    pattern_pos_list = list(result[file_name]['matches'].values())
    match_pos = abs(file_number * 100_000_000 - pattern_pos_list[match_index - 1])

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
        'mil_id': file_number,
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


# def all_page(request):
#     file_path = os.path.join(__main__.BASE_PATH, 'data/unsorted_billion/200million/pi_200mil_0.txt')

#     total_pages = 200
#     range_size = 14
#     page_size = 1_000_000

#     current_page = int(request.GET.get('current_page', 1))
#     current_page = max(1, min(current_page, total_pages))

#     start_page = max(1, current_page - range_size)
#     end_page = min(total_pages, current_page + range_size)
#     page_range = range(start_page, end_page + 1)

#     start_pos = (current_page - 1) * page_size

#     with open(file_path, 'r') as f:
#         f.seek(start_pos)
#         page_chunk = f.read(page_size)




#     context = {
#         'highlighted_chunk': page_chunk,
#         'current_page': current_page,
#         'page_range': page_range,
#         'total_pages': total_pages,
#         'page_chunk': page_chunk,
#     }
#     return render(request, 'pattern_finder/legacies/all_page.html', context)

from django.utils.html import escape
import re

def all_page(request):
    file_path = os.path.join(__main__.BASE_PATH, 'data/unsorted_billion/200million/pi_200mil_0.txt')

    total_pages = 200
    range_size = 14
    page_size = 1_000_000

    current_page = int(request.GET.get('current_page', 1))
    current_page = max(1, min(current_page, total_pages))

    start_page = max(1, current_page - range_size)
    end_page = min(total_pages, current_page + range_size)
    page_range = range(start_page, end_page + 1)

    start_pos = (current_page - 1) * page_size

    # --- POST: Добавляем новый паттерн ---
    if request.method == 'POST':
        pattern = request.POST.get('pattern', '').strip()
        if pattern:
            find_patterns = request.session.get('find_patterns', [])
            if pattern not in find_patterns:
                find_patterns.append(pattern)
            request.session['find_patterns'] = find_patterns
    else:
        find_patterns = request.session.get('find_patterns', [])

    with open(file_path, 'r') as f:
        f.seek(start_pos)
        page_chunk = f.read(page_size)

    # --- Подсветка паттернов ---
    if find_patterns:
        safe_chunk = escape(page_chunk)
        for pattern in find_patterns:
            regex = re.escape(pattern)
            safe_chunk = re.sub(
                regex,
                lambda m: f'<span class="highlight">{m.group(0)}</span>',
                safe_chunk
            )
        highlighted_chunk = safe_chunk
    else:
        highlighted_chunk = page_chunk

    context = {
        'highlighted_chunk': highlighted_chunk,
        'current_page': current_page,
        'page_range': page_range,
        'total_pages': total_pages,
        'find_patterns': find_patterns,
    }
    return render(request, 'pattern_finder/legacies/all_page.html', context)


def clear_find_patterns(request):
    request.session.pop('find_patterns', None)
    return redirect('all_page')

def find(request):

    context = {

    }
    return render(request, 'pattern_finder/legacies/all_page.html', context)