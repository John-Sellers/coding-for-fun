/* Object creation uses property:value pairs 

Example:
    var car = {
        "make":  "Ford", // "make" would be the property and "Ford" would be the value
        "model": "Mustang",
        "year": "2018",
        "trim": "Ecoboost"
    }

Object values can be any data type: boolean, string, integer, etc.

*/

var human = {
    "gender": "male",
    "age": 32,
    "height": "137 meters",
    "clothes": ["Jacket", "Shirt", "Shoes", "Pants", "Hat"],
    "is happy": true
};

// Dot notation can be used to select specific values from properites
var gender = human.gender;
var age = human.age;

// Bracket notation can be used as well. It is required if the naming scheme has a space
var isHappy = human["is happy"];

// Bracket notation can also be used to look up properties in a object
const humanAge = "age";
var age1 = human[humanAge];

// Objects can also be updated
human.age = 25;
human["is happy"] = false;

// New properties can be added
human["shirt size"] = "M";

// Properties can deleted
delete human["shirt size"];

var myObj = {
    gift: "pony",
    pet: "kitten",
    bed: "sleigh"
};

function checkObj(checkProp) {
    if (myObj.hasOwnProperty(checkProp)) {
        return myObj[checkProp]
    } else {
        return "Not Found"
    }
}

// Retrieving values from nested arrays/objects

var myStorage = {
    car: {
        inside: {
            "glove box": "maps",
            "passenger seat": "candy wrappers"
        },
        outside: {
            "trunk": "spare tire"
        }
    }
};