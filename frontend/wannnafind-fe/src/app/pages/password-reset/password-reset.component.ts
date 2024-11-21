import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-password-reset',
  templateUrl: './password-reset.component.html',
  styleUrls: ['./password-reset.component.scss'],
})
export class PasswordResetComponent {
  resetData = {
    email: '',
  };
  successMessage: string | null = null;
  errorMessage: string | null = null;

  constructor(private authService: AuthService) {}

  onSubmit() {
    this.authService.resetPassword(this.resetData).subscribe(
      (response: any) => {
        this.successMessage = 'Password reset email sent successfully.';
        this.errorMessage = null;
      },
      (error: any) => {
        this.errorMessage = 'Failed to send password reset email.';
        this.successMessage = null;
      }
    );
  }
}
