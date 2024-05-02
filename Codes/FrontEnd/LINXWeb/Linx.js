const fileInput = document.getElementById('fileInput');
const fileNameInput = document.getElementById('fileName');

fileInput.addEventListener('change', (e) => {
  const fileName = e.target.files[0].name;
  fileNameInput.value = fileName;
});


function GetColumnsInJSON(columns){
    // Extract column names and types
    const headers = columns;
    const types = [];
    for (let i = 0; i < headers.length; i++) {
        const firstDataRow = columns;
        const cellValue = firstDataRow[i];
        const cellType = typeof cellValue;
        types.push(cellType);
    }

    // Store column names and types in JSON
    const columnInfo = {};
    for (let i = 0; i < headers.length; i++) {
        columnInfo[headers[i]] = types[i];
    }

    // Output the JSON
    return columnInfo;
}

 // Function to get random rows from an array
 function getRandomRows(array, maxCount) {
    const shuffled = array.slice().sort(() => Math.random() - 0.5);
    const rowsAsDict = [];
    const headers = array[0]; // Assuming the first row contains headers
    for (let i = 1; i < shuffled.length && i <= maxCount; i++) {
        const row = shuffled[i];
        const rowDict = {};
        for (let j = 0; j < headers.length; j++) {
            rowDict[headers[j]] = row[j];
        }
        rowsAsDict.push(rowDict);
    }
    return rowsAsDict;
}

function ProcessExcelFile(title, dataurl, prompt, columns, rows){
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://127.0.0.1:5000/Jobs/Add', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            console.log("Result Out");
            // Request successful
            const od = JSON.parse(xhr.response);
            console.log(od.message[0].replace("`", "").replace("python", ""));

            var JSCode = od.message[0].replace("`", "").replace("python", "");
            ExecuteJS(JSCode, rows);

        } else {
            // Request failed
            console.error('Request failed with status:', xhr.status);
        }
    };
    xhr.onerror = function () {
        console.error('Request failed');
    };

    data = {
        "title": title,
        "dataurl": dataurl,
        "prompt": prompt,
        "columns": columns,
        "rows": rows
    }
    
    xhr.send(JSON.stringify(data));
}

function Analyze(title, dataurl, prompt, columns, rows){
    ProcessExcelFile(title, dataurl, prompt, columns, rows);
}

function OnSubmit()
{
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];
            67

}


function ExecuteJS(code, rows){
    data = rows;
    eval(code);
}

// Function to handle file input change
function handleFileChange(event) {

    alert("Run");
    // Get the selected file
    const file = event.target.files[0];
    
    if (file) {
        // Create a FormData object
        const formData = new FormData();
        
        // Append the Excel file to the FormData object
        formData.append('datafile', file);
        
        // Append two strings to the FormData object
        formData.append('tabledescription', 'this table consist of the data of fatal police shooting');
        formData.append('anlysisprompt', 'tell me the relations between criminals and their mental health');
        
        // Create a new XMLHttpRequest object
        const xhr = new XMLHttpRequest();
        
        // Configure the request to send a POST request to the server
        xhr.open('POST', 'http://127.0.0.1:5000/Jobs/Add', true);
        
        // Set the request headers (optional)
        // You may want to set headers depending on your server requirements
        
        // Callback function to handle the response from the server
        xhr.onload = function() {
            if (xhr.status === 200) {
                // Handle success response
                console.log('File and strings uploaded successfully');
                console.log('Response:', xhr.responseText);
            } else {
                // Handle error response
                console.error('Error uploading file and strings:', xhr.status, xhr.statusText);
            }
        };
        
        // Handle errors during the request
        xhr.onerror = function() {
            console.error('Network error occurred while uploading the file and strings');
        };
        
        // Send the FormData object with the file and strings
        xhr.send(formData);
    }
}
document.getElementById('fileInput').addEventListener('change', handleFileChange);
