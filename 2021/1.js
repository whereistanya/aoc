const input = require('fs')
  .readFileSync(__dirname + '/input')
  .toString();

const depths = input.split('\n').map(Number);

const part1 = () => {
    var count = 0
    for (i = 1; i < depths.length; i++) {
        if (depths[i] > depths[i - 1]) {
            count += 1
        }
    }
    return count;
};

const part2 = () => {
    var count = 0
    for (i = 3; i < depths.length; i++) {
        if (depths[i] > depths[i - 3]) {
            count += 1
        }
    }
    return count;
};

console.log(part1());
console.log(part2());