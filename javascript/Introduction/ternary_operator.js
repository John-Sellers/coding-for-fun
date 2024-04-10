// Using ternary operator can help to minimize the lines of code used

var numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

const evenNumbers = numbers.filter(num => num % 2 === 1 ? true : false);

console.log(evenNumbers); // Output: [2, 4, 6, 8, 10]