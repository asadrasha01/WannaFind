import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  loginData = { email: '', password: '' };

  constructor(private apiService: ApiService) {}

  onLogin(): void {
    this.apiService.login(this.loginData).subscribe(
      (response) => {
        console.log('Login successful:', response);
        localStorage.setItem('token', response.token); // Save token
        alert('Login successful!');
      },
      (error) => {
        console.error('Login failed:', error);
        alert('Invalid credentials.');
      }
    );
  }
}
