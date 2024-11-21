import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment'; // Ensure correct environment file path

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private apiUrl = environment.apiUrl;
  constructor(private http: HttpClient) {}

  register(data: any) {
    return this.http.post(`${environment.apiUrl}/register/`, data);
  }

  login(data: { username: string; password: string }) {
    return this.http.post(`${environment.apiUrl}/login/`, data);
  }

  resetPassword(data: { email: string }) {
    return this.http.post(`${environment.apiUrl}/password-reset/`, data);
  }

  // Change password
  changePassword(data: any) {
    return this.http.post(`${environment.apiUrl}/change-password/`, data);
  }

  getProfile() {
    return this.http.get(`${this.apiUrl}/profile/`);
  }

  checkUsername(username: string) {
    return this.http.post(`${this.apiUrl}/check-username/`, { username });
  }

  checkEmail(email: string) {
    return this.http.post(`${this.apiUrl}/check-email/`, { email });
  }

  updateProfile(data: any) {
    return this.http.put(`${this.apiUrl}/profile/`, data);
  }
}
