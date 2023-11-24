var memory = null;
var cache = null;
var cache_snapshot = null;

var animationTimeout;
var currentIndex = 0;
alert("Simulate First before other controls!");
async function buttonClick() {
    var buttons = document.getElementsByClassName("buttondesign");
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].removeAttribute("disabled");
    }
    clearTimeout(animationTimeout);
    // Clear the existing cache display
    document.getElementById('cache-iterations').value = '';
    document.getElementById('cache-container').innerHTML = '';

    let test_case = document.getElementById("test-case").value;
    let data = await eel.get_data(test_case)();

    cache = data[0];
    memory = data[1];
    cache_snapshot = data[2];
    cache_stats = data[3];

    // Display cache stats
    document.getElementById('memory-access-count').innerHTML = cache_stats[0];
    document.getElementById('cache-hit').innerHTML = cache_stats[1];
    document.getElementById('cache-miss').innerHTML = cache_stats[2];
    document.getElementById('cache-hit-rate').innerHTML = (cache_stats[3] * 100).toFixed(2);
    document.getElementById('cache-miss-rate').innerHTML = (cache_stats[4] * 100).toFixed(2);
    document.getElementById('average-time').innerHTML = cache_stats[5];
    document.getElementById('total-time').innerHTML = cache_stats[6];

    // Create cache block
    var table = document.createElement('table');
    var tbody = document.createElement('tbody');
    for (var i = 0; i < cache.length; i++) {
        var row = document.createElement('tr');

        for (var j = 0; j < cache[i].length; j++) {
            var cell = document.createElement('td');
            cell.appendChild(document.createTextNode(cache[i][j]));
            row.appendChild(cell);
        }
        tbody.appendChild(row);
    }

    table.appendChild(tbody);
    document.getElementById('cache-container').appendChild(table);

    // Display cache snapshots in a textarea
    var iterationsText = '';
    for (var k = 0; k < cache_snapshot.length; k++) {
        iterationsText += 'Iteration ' + (k + 1) + ':\n';

        for (var l = 0; l < cache_snapshot[k].length; l++) {
            iterationsText += cache_snapshot[k][l].map(value => {
                if (value === null) {
                    return 'null';
                } else if (memory[k] !== undefined && memory[k] !== null && memory[k] === value) {
                    return '[' + value + ']';
                } else {
                    return value;
                }
            }).join('\t') + '\n';
        }
    }

    document.getElementById('cache-iterations').value = iterationsText;
}


// Rest of your code...


//  ANIMATION
var currentIndex = 0; // Keep track of the current index in cache_snapshot array
var animationTimeout; // Variable to store the timeout ID for the animation
var isPaused = false; // Flag to track if the animation is paused

function animate() {
    if (!isPaused && currentIndex < cache_snapshot.length) {
        // Update the displayed cache state with highlighting
        updateCacheDisplay(cache_snapshot[currentIndex], memory[currentIndex]);

        // Call animate function recursively with a delay of 0.5 seconds
        animationTimeout = setTimeout(animate, 250);
        currentIndex++;
    }
}

function updateCacheDisplay(cacheState, currentValue) {

    document.getElementById('current-snapshot').innerHTML = currentIndex + "/" + cache_snapshot.length

    // Clear the existing cache display
    document.getElementById('cache-container').innerHTML = '';

    // Create a new table for the updated cache state
    var table = document.createElement('table');
    var tbody = document.createElement('tbody');

    for (var i = 0; i < cacheState.length; i++) {
        var row = document.createElement('tr');

        for (var j = 0; j < cacheState[i].length; j++) {
            var cell = document.createElement('td');

            // Check if this is the current value being added to the cache
            if (cacheState[i][j] === currentValue) {
                cell.style.backgroundColor = "#008170";
                cell.style.boxShadow = '0px 50px 50px #005B41';
            }

            cell.appendChild(document.createTextNode(cacheState[i][j]));
            row.appendChild(cell);
        }
        tbody.appendChild(row);
    }

    table.appendChild(tbody);
    document.getElementById('cache-container').appendChild(table);
}

// Call animate function after button click
// Assuming you have a button with id "start-animation" to trigger the animation
document.getElementById("start-animation").addEventListener("click", function () {
    currentIndex = 0; // Reset the current index
    isPaused = false; // Reset pause state
    animate();
});

// Stop Animation Button
document.getElementById("stop-animation").addEventListener("click", function () {
    clearTimeout(animationTimeout); // Clear the timeout to stop the animation
    isPaused = false; // Reset pause state
});

// Pause/Resume Animation Button
document.getElementById("pause-animation").addEventListener("click", function () {
    isPaused = !isPaused; // Toggle pause state
    if (!isPaused) {
        animate(); // If unpausing, resume the animation
    }
});

// Next Button
document.getElementById("next-animation").addEventListener("click", function () {
    if (currentIndex < cache_snapshot.length - 1) {
        currentIndex++;
        updateCacheDisplay(cache_snapshot[currentIndex], memory[currentIndex]);
    }
});

// Previous Button
document.getElementById("prev-animation").addEventListener("click", function () {
    if (currentIndex > 0) {
        currentIndex--;
        updateCacheDisplay(cache_snapshot[currentIndex], memory[currentIndex]);
    }
});