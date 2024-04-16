import { Component } from '@angular/core';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.css']
})
export class FileUploadComponent {
  selectedFile: File | null = null;
  inputText: string = '';

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  onSubmit() {
    // Implement logic to handle file upload and text submission (e.g., using a service)
    console.log('File:', this.selectedFile);
    console.log('Text:', this.inputText);

    // Reset for new submission (optional)
    this.selectedFile = null;
    this.inputText = '';
  }
}
