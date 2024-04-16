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
            const data = JSON.parse(xhr.response);
            console.log(data);
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
            const reader = new FileReader();

            let columns = {};

            reader.onload = function (e) {
                const data = new Uint8Array(e.target.result);
                const workbook = XLSX.read(data, { type: 'array' });

                // Assuming the first sheet is the one you want to read
                const sheetName = workbook.SheetNames[0];
                const sheet = workbook.Sheets[sheetName];

                // Convert sheet data to JSON
                const jsonData = XLSX.utils.sheet_to_json(sheet, { header: 1 });

                // Create HTML table
                const tableContainer = document.getElementById('tableContainer');
                const table = document.createElement('table');
                const headerRow = table.insertRow();
                const headers = jsonData[0];

                columns = GetColumnsInJSON(headers);
                const randomRows = getRandomRows(jsonData, 50);
                const rows = JSON.stringify(randomRows, null, 2);
                console.log(rows);

                // Add headers to table
                for (let i = 0; i < headers.length; i++) {
                    const headerCell = document.createElement('th');
                    headerCell.textContent = headers[i];
                    headerRow.appendChild(headerCell);
                }

                // Add data rows to table
                for (let i = 1; i < jsonData.length; i++) {
                    const dataRow = table.insertRow();
                    const rowData = jsonData[i];
                    for (let j = 0; j < rowData.length; j++) {
                        const cell = dataRow.insertCell();
                        cell.textContent = rowData[j];
                    }
                }

                // Append table to container
                tableContainer.innerHTML = '';
                tableContainer.appendChild(table);

                Analyze("Testing", "", "Analyze the data", columns, rows);
            };

            reader.readAsArrayBuffer(file);

}