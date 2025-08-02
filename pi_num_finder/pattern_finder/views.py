from django.shortcuts import render, redirect
from django.utils.html import escape
from .services import __main__
import os, re, random, itertools


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
    pattern = request.session.get('pattern')
    result = request.session.get('search_result')

    if not pattern or not result:
        return redirect('home')

    try:
        match_index = int(request.GET.get('match_index', 1))
    except (ValueError, TypeError):
        match_index = 1

    page_size = 1000
    find_patterns = request.session.get('find_patterns', [])

    file_names = list(result.keys())
    try:
        file_name = file_names[mil_id - 1]
    except IndexError:
        return redirect('home')

    match = re.search(r'_(\d+)\.txt', file_name)
    if not match:
        return redirect('home')

    file_number = int(match.group(1))
    file_path = os.path.join(dpath, file_name)

    pattern_pos_list = list(result[file_name]['matches'].values())
    try:
        match_pos = abs(file_number * 100_000_000 - pattern_pos_list[match_index - 1])
    except IndexError:
        match_pos = 0

    start = max(0, match_pos - page_size // 2)
    current_page = match_pos // page_size

    with open(file_path, 'r') as f:
        f.seek(start)
        chunk = f.read(page_size)

    # Подсветка основного шаблона
    highlighted_chunk = re.sub(
        f'({re.escape(pattern)})',
        r'<span class="highlight">\1</span>',
        chunk
    )

    # Обработка формы
    if request.method == 'POST':
        new_pattern = request.POST.get('find_pattern', '').strip()
        if new_pattern and new_pattern not in find_patterns:
            find_patterns.append(new_pattern)
            if len(find_patterns) > 10:
                find_patterns.pop(0)
            request.session['find_patterns'] = find_patterns

    # Подсветка дополнительных шаблонов
    if find_patterns:
        color_classes = [f'highlight-color{i}' for i in range(10)]
        random.shuffle(color_classes)
        pattern_colors = dict(zip(find_patterns, itertools.cycle(color_classes)))

        safe_chunk = highlighted_chunk
        for p in find_patterns:
            regex = re.escape(p)
            color_class = pattern_colors[p]
            safe_chunk = re.sub(
                regex,
                lambda m: f'<span class="{color_class}">{m.group(0)}</span>',
                safe_chunk
            )
        highlighted_chunk = safe_chunk
        pattern_colors_list = list(pattern_colors.items())
    else:
        pattern_colors_list = []

    total_length_of_file = os.path.getsize(file_path)
    count_of_pages = total_length_of_file // page_size

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
        'find_patterns': find_patterns,
        'pattern_colors': pattern_colors_list,
    }
    return render(request, 'pattern_finder/legacies/pi_chunk_details.html', context)

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

    find_patterns = request.session.get('find_patterns', [])

    if request.method == 'POST':
        new_pattern = request.POST.get('find_pattern', '').strip()
        if new_pattern:
            if new_pattern not in find_patterns:
                if len(find_patterns) >= 10:
                    find_patterns.pop(0)
                find_patterns.append(new_pattern)
                request.session['find_patterns'] = find_patterns

    with open(file_path, 'r') as f:
        f.seek(start_pos)
        page_chunk = f.read(page_size)

    if find_patterns:
        safe_chunk = escape(page_chunk)
        color_classes = [f'highlight-color{i}' for i in range(10)]
        random.shuffle(color_classes)
        pattern_colors = dict(zip(find_patterns, itertools.cycle(color_classes)))

        for p in find_patterns:
            regex = re.escape(p)
            css_class = pattern_colors[p]
            safe_chunk = re.sub(
                regex,
                lambda m: f'<span class="{css_class}">{m.group(0)}</span>',
                safe_chunk
            )
        highlighted_chunk = safe_chunk
        pattern_colors_list = list(pattern_colors.items())
    else:
        highlighted_chunk = page_chunk
        pattern_colors_list = []

    context = {
        'highlighted_chunk': highlighted_chunk,
        'current_page': current_page,
        'page_range': page_range,
        'total_pages': total_pages,
        'find_patterns': find_patterns,
        'pattern_colors': pattern_colors_list,
    }
    return render(request, 'pattern_finder/legacies/all_page.html', context)


def clear_find_patterns(request):
    request.session['find_patterns'] = []
    request.session.modified = True
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('home')