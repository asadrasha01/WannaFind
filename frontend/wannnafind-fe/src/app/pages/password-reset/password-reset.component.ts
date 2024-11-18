import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-password-reset',
  templateUrl: './password-reset.component.html',
  styleUrls: ['./password-reset.component.scss'],
})
export class PasswordResetComponent {
  email = '';

  constructor(private apiService: ApiService) {}

  onPasswordReset(): void {
    this.apiService.passwordResetRequest(this.email).subscribe(
      (response) => {
        console.log('Password reset email sent:', response);
        alert('Password reset email sent!');
      },
      (error) => {
        console.error('Password reset failed:', error);
        alert('Password reset failed.');
      }
    );
  }
}
