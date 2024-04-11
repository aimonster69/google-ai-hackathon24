import { Component, Input } from '@angular/core';

interface UploadResponse {
  message: string;
}

@Component({
  selector: 'app-response',
  templateUrl: './response.component.html',
  styleUrls: ['./response.component.css']
})
export class ResponseComponent {
  @Input() response: UploadResponse | null = null;
}
