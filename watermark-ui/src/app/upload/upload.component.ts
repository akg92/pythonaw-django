import { Component, OnInit } from '@angular/core';
import { UploadService } from '../upload.service';
import { saveAs } from "file-saver";
@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss']
})
export class UploadComponent implements OnInit {

  public fileName: string = null;
  public file: any = null;
  public fileFullName: any;
  public get fileText(){
    return this.fileName ? 'Selected File ' + this.fileName : 'No File Selected'; 
  }
  constructor(private uploadService: UploadService) { }
  ngOnInit() {
  }

  public fileSelect(fileInput: Event){
    this.file = 'files' in fileInput.target ? fileInput.target['files'][0] : null;
    this.fileName = this.file && 'name' in this.file ? this.file.name : '';
    console.log(this.fileName);
    // document.getElementById('customFileText').textContent = 'You selected' + this.fileName;
  }

  public submit(){
    if(this.file){
      this.uploadService.sendFile(this.fileName, this.file).subscribe((data)=>{
        console.log(data);
        saveAs(data, 'watermark.pdf');
      });
    }
  }

}
