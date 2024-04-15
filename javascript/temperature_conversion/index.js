// Creating a function that will convert F to C and visa versa

const numBox = document.getElementById("numBox");
const fToC = document.getElementById("F => C");
const cToF = document.getElementById("C => F");
const result = document.getElementById("result");
let temp;

function Convert() {
  if (fToC.checked) {
    temp = Number(numBox.value);
    temp = (5 / 9) * (temp - 32);
    result.textContent = temp.toFixed(1) + "°C";
  } else if (cToF.checked) {
    temp = Number(numBox.value);
    temp = (9 / 5) * temp + 32;
    result.textContent = temp.toFixed(1) + "°F";
  } else result.textContent = "Select a unit!!";
}
