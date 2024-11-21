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
  message: string = '';

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
    this.authService.checkUsername(this.newUsername).subscribe(
      (response: any) => {
        this.message = response.available
          ? 'Username is available.'
          : 'Username is already taken.';
      },
      (error) => {
        console.error('Error checking username:', error);
      }
    );
  }

  checkEmailAvailability(): void {
    this.authService.checkEmail(this.newEmail).subscribe(
      (response: any) => {
        this.message = response.available
          ? 'Email is available.'
          : 'Email is already in use.';
      },
      (error) => {
        console.error('Error checking email:', error);
      }
    );
  }

  saveChanges(): void {
    const updatedData: any = {};
    if (this.newUsername) updatedData.username = this.newUsername;
    if (this.newEmail) updatedData.email = this.newEmail;

    this.authService.updateProfile(updatedData).subscribe(
      (response: any) => {
        this.message = 'Profile updated successfully!';
        this.loadProfile(); // Reload the profile to show updated data
      },
      (error) => {
        this.message = error.error?.error || 'Error updating profile.';
      }
    );
  }
}
