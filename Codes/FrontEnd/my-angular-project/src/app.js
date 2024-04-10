angular.module('myApp', ['ngMaterial'])
  .controller('UploadController', function UploadController() {
    this.selectedFile = null;
    this.promptText = '';

    this.handleFileChange = () => {
      const allowedExtensions = ['.csv', '.xls', '.xlsx'];
      const extension = this.selectedFile.name.split('.').pop().toLowerCase();

      if (!allowedExtensions.includes(extension)) {
        alert('Invalid file type. Please select a CSV or Excel file.');
        this.selectedFile = null;
        return;
      }
    };

    this.handleSubmit = () => {
      // Implement logic to handle file upload and process the prompt text
      console.log('Selected file:', this.selectedFile);
      console.log('Prompt text:', this.promptText);
      // Replace with your backend interaction or processing
    };
  });