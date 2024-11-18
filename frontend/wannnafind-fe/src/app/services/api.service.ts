// src/app/services/api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private BASE_URL = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  register(data: any): Observable<any> {
    return this.http.post(`${this.BASE_URL}/register/`, data);
  }

  login(data: any): Observable<any> {
    return this.http.post(`${this.BASE_URL}/login/`, data);
  }

  passwordResetRequest(email: string): Observable<any> {
    return this.http.post(`${this.BASE_URL}/password-reset/`, { email });
  }

  changePassword(data: any): Observable<any> {
    return this.http.post(`${this.BASE_URL}/change-password/`, data);
  }

  getProfile(): Observable<any> {
    return this.http.get(`${this.BASE_URL}/profile/`);
  }
}
