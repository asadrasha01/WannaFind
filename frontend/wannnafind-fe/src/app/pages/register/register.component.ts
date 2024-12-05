import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent {
  userData = {
    username: '',
    email: '',
    password: '',
  };
  message: string = '';
  errorMessage: string = '';

  constructor(private authService: AuthService) {}

  onSubmit(): void {
    this.authService.register(this.userData).subscribe(
      (response) => {
        this.message = response.message;
        this.errorMessage = '';
      },
      (error) => {
        this.errorMessage = error.error.error || 'Registration failed.';
        this.message = '';
      }
    );
  }
}
