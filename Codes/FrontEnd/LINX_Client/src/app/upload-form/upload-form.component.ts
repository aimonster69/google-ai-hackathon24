import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface UploadResponse {
  message: string;
}

@Component({
  selector: 'app-upload-form',
  templateUrl: './upload-form.component.html',
  styleUrls: ['./upload-form.component.css']
})
export class UploadFormComponent implements OnInit {
  selectedFile: File | null = null;
  text: string = '';
  response: UploadResponse | null = null;

  constructor(private http: HttpClient) {}

  ngOnInit(): void {}

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length) {
      this.selectedFile = input.files[0];
    }
  }

  onSubmit() {
    const formData = new FormData();
    formData.append('file', this.selectedFile);
    formData.append('text', this.text);

    this.http.post<UploadResponse>('your-api-url', formData)
      .subscribe(response => {
        this.response = response;
      });
  }
}