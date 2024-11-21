import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'],
})
export class HomePageComponent {
  loginData = {
    username: '',
    password: '',
  };
  showPassword = false;
  errorMessage: string | null = null;

  constructor(private authService: AuthService, private router: Router) {}

  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  onSubmit() {
    this.authService.login(this.loginData).subscribe(
      (response: any) => {
        console.log('Login successful:', response);
        // Save the token and redirect
        localStorage.setItem('token', response.token);
        this.errorMessage = null;
        this.router.navigate(['/profile']);
      },
      (error: any) => {
        console.error('Login error:', error);
        this.errorMessage = 'Invalid username or password.';
      }
    );
  }
}
