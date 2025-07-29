function submitPageInput() {
    let input = document.getElementById('page-input');
    let valStr = input.value.trim();

    if (!/^\d+$/.test(valStr)) {
      window.location.href = window.location.pathname;
      return;
    }

    let val = parseInt(valStr);
    if (val < 1) val = 1;
    else if (val > 200) val = 200;

    window.location.href = `?current_page=${val}`;
}


function changePage(delta) {
    let input = document.getElementById('page-input');
    let val = parseInt(input.value);

    if (isNaN(val)) val = 1;

    val += delta;
    if (val < 1) val = 1;
    if (val > 200) val = 200;

    window.location.href = `?current_page=${val}`;
}