/* Functions help to make code more reusable and easily modifiable.
They can take parameters as inputs and be used throughout the code base

Example:
function firstFunction(a,b,c) {
    console.log("This is our first function!");
    console.log(a+b+c);
}

firstFunction(1,2,3)

firstFunction is the object that can be used when coding, while a, b, and c
are parameters that we input into the function

Local variable holds priority over global variables when used in the context of a function
*/

var globalVariable = 10; // Global variables are variables that can be access by any object

function ourReusableFunction() {
    console.log("Hello World");
}

function reusableFunction() {
    console.log("Hi World");
}

function function1() {
    /* This is a local variable. It can only be used in the scope of this function,
    otherwise an error occur stating that the variable is undefined
    
    Using the var keyword makes this variable a scope variable    
    */
    var localVariable = 10;

    /* This is a global variable as well, even though it is used in this function
    
    If the var keyword is not assigned to the variable, it is considered global 
    */
    otherGlobalVariable = 20;
}

function function2() {
    var output = "";
    if (typeof globalVariable != "undefined") {
        output += "Global Variable: " + globalVariable;
    }
    if (typeof otherGlobalVariable != "undefined") {
        output += " Other Global Variable: " + otherGlobalVariable;
    }
    console.log(output);
}

function addition(num) {
    // This return keyword specifies the value that the function should return when called
    return console.log(num + 10);
}

function nextInLine(arr, item) {
    arr.push(item);
    return arr.shift();
}

var testArr = [1, 2, 3, 4, 5];

function square(int) {
    return int * int
}


var number = 8

console.log("Before: " + JSON.stringify(testArr));
console.log(nextInLine(testArr, 6));
console.log("After: " + JSON.stringify(testArr))
console.log(square(number))