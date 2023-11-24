async function buttonClick() {
    // Fill Up Memory Blocks
    

    // Fill Up Cache Blocks
    document.getElementById("cache-container").innerHTML = null
    let test_case = document.getElementById("test-case").value;
    let data = await  eel.get_data(test_case)();
    let cache = data[0]
    let memory = data[1]

    // CREATE CACHE BLOCK
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
}