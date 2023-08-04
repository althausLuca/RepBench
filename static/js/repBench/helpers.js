const registerPlayAndReloadBtns = function (name, handler) {
    $('#play-' + name).on('click', function (event) {
        event.preventDefault();
        $(this).find('i').toggle();
        console.log('play')
        console.log(handler)
        handler.playing = !handler.playing
        if (handler.computing) {
        } else {
            handler.computing = true;
            handler.start()
        }
    });

    $('#reload-' + name).on('click', function (event) {
        // Prevent form submission if it's a submit button
        event.preventDefault();
        if (handler.data.length > 0) {
            handler.start()
        }

        if (handler.playing) {
            handler.playing = false
            $('#play-' + name).find('i').toggle();
        }

    });

}


function transposeArray(array) {
    return array[0].map((_, colIndex) => array.map(row => row[colIndex]));
}

function convertToCSV(dataObject) {
    var transposedData = transposeArray(Object.values(dataObject));
    var csvContent = "";

    // Get the header row from the object keys
    var headerRow = Object.keys(dataObject).join(",");
    csvContent += headerRow + "\n";

    // Get the data rows
    var rows = transposedData;

    // Iterate over the rows and convert each row to CSV format
    rows.forEach(function (row, rowIndex) {
        // Convert the row values to a comma-separated string
        var rowValues = row.join(",");
        csvContent += rowValues + "\n";
    });

    return csvContent;
}


function download(data, filename) {

    // Convert the data object to CSV format
    var csvContent = convertToCSV(data);

    // Create a Blob object with the CSV data
    var blob = new Blob([csvContent], {type: "text/csv;charset=utf-8;"});

    // Create a temporary URL for the Blob
    var url = URL.createObjectURL(blob);

    // Create a link element
    var link = document.createElement("a");
    link.href = url;
    link.download = filename;

    // Append the link to the document body
    document.body.appendChild(link);

    // Simulate a click event to trigger the download
    link.click();

    // Clean up the temporary URL and link
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}