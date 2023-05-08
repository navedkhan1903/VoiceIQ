function submitQuery() {
  const enteredQuery = document.getElementById("query");
  const userInput = document.getElementById("userInput");
  const reqWrapper = document.getElementById("reqWrapper");
  const welcome_screen = document.getElementById("welcome_screen");
  const res = document.getElementById("response");
  const resWrapper = document.getElementById("resWrapper");
  const spinner = document.getElementById("animation-overlay")

  if (enteredQuery.value == '') return;

  reqWrapper.style.visibility = 'visible';
  userInput.innerHTML = enteredQuery.value;
  reqWrapper.style.height = userInput.offsetHeight + 50 + 'px';
  welcome_screen.style.display = 'none';
  resWrapper.style.visibility = 'visible';
  spinner.style.display = 'block';
  resWrapper.style.height = res.offsetHeight + 'px';

  eel.queryHandler(enteredQuery.value)(response);
  enteredQuery.value = '';
}

function response(response) {
  const res = document.getElementById("response");
  const resWrapper = document.getElementById("resWrapper");
  const spinner = document.getElementById("animation-overlay")

  spinner.style.display = 'none';
  res.innerHTML = response;
  resWrapper.style.height = res.offsetHeight + 'px'
  eel.speak()
}