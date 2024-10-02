// src/app/services/item.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ItemService {
  private apiUrl = 'http://localhost:8000/api/items/';
  constructor(private http: HttpClient) { }

  getItems(): Observable<any> {
    return this.http.get(this.apiUrl);
  }

  createItem(data: any): Observable<any> {
    return this.http.post(this.apiUrl, data);
  }
}
