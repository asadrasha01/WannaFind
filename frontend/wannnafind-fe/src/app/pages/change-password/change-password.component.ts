import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-change-password',
  templateUrl: './change-password.component.html',
  styleUrls: ['./change-password.component.scss'],
})
export class ChangePasswordComponent {
  currentPassword: string = '';
  newPassword: string = '';
  message: string | null = null;
  errorMessage: string | null = null;

  constructor(private authService: AuthService) {}

  onSubmit(): void {
    this.authService
      .changePassword(this.currentPassword, this.newPassword)
      .subscribe(
        (response: any) => {
          this.message = response.message;
          this.errorMessage = null;
        },
        (error: any) => {
          this.message = null;
          this.errorMessage =
            error.error?.error || 'Failed to change password.';
        }
      );
  }
}
