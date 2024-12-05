import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent implements OnInit {
  currentUsername: string = '';
  currentEmail: string = '';
  newUsername: string = '';
  newEmail: string = '';
  currentPassword: string = '';
  newPassword: string = '';
  usernameAvailable: boolean | null = null;
  emailAvailable: boolean | null = null;
  usernameMessage: string = '';
  emailMessage: string = '';
  updateMessage: string = '';
  passwordMessage: string = '';
  passwordError: string = '';

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.loadProfile();
  }

  loadProfile(): void {
    this.authService.getProfile().subscribe(
      (data: any) => {
        this.currentUsername = data.username || '';
        this.currentEmail = data.email || '';
      },
      (error) => {
        console.error('Error fetching profile:', error);
      }
    );
  }

  checkUsernameAvailability(): void {
    if (!this.newUsername.trim()) {
      this.usernameMessage = 'Username cannot be empty.';
      this.usernameAvailable = null;
      return;
    }
    this.authService.checkUsername(this.newUsername).subscribe(
      (response: any) => {
        this.usernameAvailable = response.available;
        this.usernameMessage = response.available
          ? 'Username is available.'
          : 'Username is already taken.';
      },
      (error) => {
        console.error('Error checking username:', error);
        this.usernameMessage = 'An error occurred. Please try again.';
      }
    );
  }

  checkEmailAvailability(): void {
    if (!this.newEmail.trim()) {
      this.emailMessage = 'Email cannot be empty.';
      this.emailAvailable = null;
      return;
    }
    this.authService.checkEmail(this.newEmail).subscribe(
      (response: any) => {
        this.emailAvailable = response.available;
        this.emailMessage = response.available
          ? 'Email is available.'
          : 'Email is already in use.';
      },
      (error) => {
        console.error('Error checking email:', error);
        this.emailMessage = 'An error occurred. Please try again.';
      }
    );
  }

  saveChanges(): void {
    const updatedData: any = {};
    if (this.newUsername) updatedData.username = this.newUsername;
    if (this.newEmail) updatedData.email = this.newEmail;

    this.authService.updateProfile(updatedData).subscribe(
      (response: any) => {
        this.updateMessage = 'Profile updated successfully!';
        this.loadProfile();
        this.resetFields();
      },
      (error) => {
        console.error('Error updating profile:', error);
        this.updateMessage =
          error.error?.error || 'An error occurred while updating the profile.';
      }
    );
  }

  changePassword(): void {
    if (!this.currentPassword || !this.newPassword) {
      this.passwordError = 'Both fields are required.';
      return;
    }
    this.authService
      .changePassword(this.currentPassword, this.newPassword)
      .subscribe(
        (response: any) => {
          this.passwordMessage =
            response.message || 'Password changed successfully!';
          this.passwordError = '';
          this.currentPassword = '';
          this.newPassword = '';
        },
        (error: any) => {
          console.error('Error changing password:', error);
          this.passwordError =
            error.error?.error || 'An error occurred. Please try again.';
          this.passwordMessage = '';
        }
      );
  }

  resetFields(): void {
    this.newUsername = '';
    this.newEmail = '';
    this.usernameAvailable = null;
    this.emailAvailable = null;
    this.usernameMessage = '';
    this.emailMessage = '';
  }
}
