import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-password-reset',
  templateUrl: './password-reset.component.html',
  styleUrls: ['./password-reset.component.scss'],
})
export class PasswordResetComponent {
  email: string = '';
  message: string | null = null;
  errorMessage: string | null = null;

  constructor(private authService: AuthService) {}

  onSubmit(): void {
    this.authService.passwordResetRequest(this.email).subscribe(
      (response: any) => {
        this.message = response.message;
        this.errorMessage = null;
      },
      (error: any) => {
        this.message = null;
        this.errorMessage = error.error?.error || 'Failed to send reset link.';
      }
    );
  }
}
