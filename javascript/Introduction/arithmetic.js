// Basic arithmetic can be done as well
var sum = 10 + 10;
var subtraction = 10 - 10;
var multiply = 10 * 10;
var division = 10 / 10;

console.log(sum, subtraction, multiply, division);

/* Another way to do basic arithmetic is by using the following operators:

+=
-=
*=
/=

*/

sum += 1;
subtraction -= 2;
multiply *= 3;
division /= 4;

console.log(sum, subtraction, multiply, division);

/* Incrementing and decrementing a number can be done in a simpler way

Orginal Way: var myVar = 28
    increment myVar = myvar + or - 1

New Way: myVar++ or myVar--

*/

var myVar = 28;
var myVar2 = 1;
myVar++;
myVar2--;
console.log(myVar, myVar2);