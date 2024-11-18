import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment'; // Ensure correct environment file path

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(private http: HttpClient) {}

  register(data: any) {
    return this.http.post(`${environment.apiUrl}/register/`, data);
  }

  login(data: any) {
    return this.http.post(`${environment.apiUrl}/login/`, data);
  }

  passwordReset(data: any) {
    return this.http.post(`${environment.apiUrl}/password-reset/`, data);
  }

  // Change password
  changePassword(data: any) {
    return this.http.post(`${environment.apiUrl}/change-password/`, data);
  }
}
