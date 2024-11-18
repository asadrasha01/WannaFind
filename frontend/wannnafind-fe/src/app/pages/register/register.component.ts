import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent {
  user = {
    username: '',
    email: '',
    password: '',
  };

  constructor(private authService: AuthService) {}

  onSubmit() {
    this.authService.register(this.user).subscribe({
      next: (response) => {
        alert('Registration successful. Please confirm your email.');
      },
      error: (error) => {
        alert('Registration failed. Please try again.');
        console.error(error);
      },
    });
  }
}
