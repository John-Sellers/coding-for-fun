// Define a variable
const temperature = 50;

// Check the value of the temperature variable using an if statement
if (temperature > 30) {
    console.log(`It is ${temperature} degrees outside. It's a hot day!`);
} else if (temperature >= 20 && temperature <= 30) {
    console.log(`It is ${temperature} degrees outside. It's a pleasant day.`);
} else {
    console.log(`It is ${temperature} degrees outside. It's a cold day.`);
}

const isLoggedIn = true;
const isAdmin = false;

if (isLoggedIn && isAdmin) {
    console.log("Hello Admin!");
} else if (isLoggedIn) {
    console.log("Hello User!");
} else {
    console.log("Please log in")
}