const form = document.getElementById('form-login');

form.addEventListener('submit', (event) => {
  //TODO implement a real authentication
  event.preventDefault();
  input_email = form.elements['email'].value;
  console.log("email entered:" + input_email);
  if(input_email === "1" | input_email === "2"){
    form.submit();
  }
});
