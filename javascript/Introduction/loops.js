/* Loops allow for the running of code multiple times
There are different types of loops:
    for loops
    while loops
*/

// Example of while loop:

var myArray = [];
var i = 0;

while (i < 5) {
    myArray.push(i)
    i++
};

// Example of for loop:
var mySecondArray = [];

/* 
The first parameter of the for loop is the initialization.
The second is condition.
The third is the final expression
*/
for (var i = 0; i < 5; i++) {
    mySecondArray.push(i)
};

var filledArray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
var arrayTotal = 0

for (var i = 0; i < filledArray.length; i++) {
    arrayTotal += filledArray[i]
}


// Do while loops always run one time and then checks the condition after

var myArray = [];
var i = 10;

do {
    myArray.push(i);
    i++;
} while (i < 5)

console.log(i, myArray)

console.log(arrayTotal)