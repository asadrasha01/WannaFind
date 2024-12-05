import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-password-reset-confirm',
  templateUrl: './password-reset-confirm.component.html',
  styleUrls: ['./password-reset-confirm.component.scss'],
})
export class PasswordResetConfirmComponent {
  newPassword: string = '';
  message: string | null = null;
  errorMessage: string | null = null;
  uidb64: string | null = null;
  token: string | null = null;

  constructor(private route: ActivatedRoute, private authService: AuthService) {
    this.uidb64 = this.route.snapshot.paramMap.get('uidb64');
    this.token = this.route.snapshot.paramMap.get('token');
  }

  onSubmit(): void {
    if (!this.uidb64 || !this.token) {
      this.errorMessage = 'Invalid reset link.';
      return;
    }

    this.authService
      .passwordResetConfirm(this.uidb64, this.token, this.newPassword)
      .subscribe(
        (response: any) => {
          this.message = response.message;
          this.errorMessage = null;
        },
        (error: any) => {
          this.message = null;
          this.errorMessage = error.error?.error || 'Failed to reset password.';
        }
      );
  }
}
