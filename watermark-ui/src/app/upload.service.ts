import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class UploadService {
  baseUrl = '/upload/';
  constructor(private http: HttpClient) { }

  private getURl(fileName: string){
    return this.baseUrl + fileName;
  }
  public sendFile(fileName, file){
    return this.http.put( this.getURl(fileName), file,  {headers: new HttpHeaders(),
            responseType: "blob"
            });

  }
}
