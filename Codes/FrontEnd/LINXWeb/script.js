// JavaScript for handling file upload
document.getElementById("uploadArea").addEventListener("dragover", function (event) {
    event.preventDefault();
    event.stopPropagation();
    this.classList.add("dragover");
});

document.getElementById("uploadArea").addEventListener("dragleave", function (event) {
    this.classList.remove("dragover");
});

document.getElementById("uploadArea").addEventListener("drop", function (event) {
    event.preventDefault();
    event.stopPropagation();
    this.classList.remove("dragover");
    handleFileUpload(event.dataTransfer.files);
});

document.getElementById("browseFiles").addEventListener("click", function () {
    document.getElementById("fileInput").click();
});

document.getElementById("fileInput").addEventListener("change", function (event) {
    handleFileUpload(event.target.files);
});

var file = null;

function handleFileUpload(files) {
    // Handle file upload logic here
    console.log("Files uploaded:", files);
    file = files[0];
    console.log(file);
}

// Handle form submission
document.getElementById("submitButton").addEventListener("click", function () {
    const input1 = document.getElementById("textInput1").value;
    const input2 = document.getElementById("textInput2").value;
    
    console.log("Form submitted with values:", input1, input2);
    // Handle form submission logic here
    
    if (file) {
        // Create a FormData object
        const formData = new FormData();
        
        // Append the Excel file to the FormData object
        formData.append('datafile', file);
        
        // Append two strings to the FormData object
        formData.append('tabledescription', input1);
        formData.append('anlysisprompt', input2);
        
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

        document.getElementById("Card").style.display = "block";

        const fileName = file.name.toLowerCase();
        if (fileName.endsWith('.csv')) {
            readCSVFile(file);
        } else if (fileName.endsWith('.xlsx')) {
            readExcelFile(file);
        }
    }
});


function handleFileChange(event) {

    alert("Run");
    // Get the selected file
    
}


    // Function to read a CSV file
    function readCSVFile(file) {
        Papa.parse(file, {
            complete: function(results) {
                const data = results.data;
                displayRandomRows(data);
            }
        });
    }

    // Function to read an Excel file
    function readExcelFile(file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            const arrayBuffer = event.target.result;
            const workbook = XLSX.read(arrayBuffer, { type: 'array' });
            const sheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[sheetName];
            const data = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
            displayRandomRows(data);
        };
        reader.readAsArrayBuffer(file);
    }


// Function to display random rows from the data
function displayRandomRows(data) {
    // Display the header row
    const headerRow = data[0];
    // const headerRowElement = document.getElementById('headerRow');
    // headerRowElement.innerHTML = '';
    // headerRow.forEach(cell => {
    //     const th = document.createElement('th');
    //     th.innerText = cell;
    //     headerRowElement.appendChild(th);
    // });

    // Remove the header row from data
    data.shift();

    // Select 5 random rows
    const randomRows = selectRandomRows(data, 5);

    // Display the random rows in the table
    const bodyRowsElement = document.getElementById('bodyRows');
    bodyRowsElement.innerHTML = '';

    const bodyRowsElementheader = document.createElement("tr");

    headerRow.forEach(cell =>{
        const th = document.createElement('th');
        th.innerText = cell;
        bodyRowsElementheader.appendChild(th);
    });

    bodyRowsElement.append(bodyRowsElementheader);
    
    randomRows.forEach(row => {
        const tr = document.createElement('tr');
        row.forEach(cell => {
            const td = document.createElement('td');
            td.innerText = cell;
            tr.appendChild(td);
        });
        bodyRowsElement.appendChild(tr);
    });
}

// Function to select n random rows from the data
function selectRandomRows(data, n) {
    const shuffled = data.sort(() => 0.5 - Math.random());
    return shuffled.slice(0, n);
}

function HideCard(){
    document.getElementById("Card").style.display = "none";
}