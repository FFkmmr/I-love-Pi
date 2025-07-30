function submitPageInput(input) {
  if (!input) return;
  let valStr = input.value.trim();
  if (!/^\d+$/.test(valStr)) {
    window.location.href = window.location.pathname;
    return;
  }
  let val = Math.min(200, Math.max(1, parseInt(valStr)));
  window.location.href = `?current_page=${val}`;
}

function changePage(delta) {
  let input = document.querySelector('.page-input');
  if (!input) return;
  let val = parseInt(input.value);
  if (isNaN(val)) val = 1;
  val = Math.min(200, Math.max(1, val + delta));
  window.location.href = `?current_page=${val}`;
}
