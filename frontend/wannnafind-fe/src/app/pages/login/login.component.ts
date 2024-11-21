import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  loginData = {
    username: '',
    password: '',
  };
  errorMessage: string | null = null;

  constructor(private authService: AuthService, private router: Router) {}

  onSubmit() {
    this.authService.login(this.loginData).subscribe(
      (response: any) => {
        console.log('Login successful:', response);
        // Save the token (if applicable) and redirect
        localStorage.setItem('token', response.token);
        this.router.navigate(['/home']);
      },
      (error: any) => {
        console.error('Login error:', error);
        this.errorMessage = 'Invalid username, email, or password.';
      }
    );
  }
}
