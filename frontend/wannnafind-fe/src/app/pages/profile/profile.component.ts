import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent implements OnInit {
  profile: any = {};
  countries: string[] = [
    'United States',
    'Canada',
    'United Kingdom',
    'India',
    'Australia',
  ];
  usernameAvailable: boolean | null = null;
  emailAvailable: boolean | null = null;
  isEditing: boolean = false;
  isEditingUsername: boolean = false;
  isEditingEmail: boolean = false;

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.loadProfile();
  }

  loadProfile(): void {
    this.authService.getUserProfile().subscribe(
      (response) => {
        this.profile = response;
      },
      (error) => {
        console.error('Error loading profile:', error);
      }
    );
  }

  toggleEdit(): void {
    this.isEditing = !this.isEditing;
  }

  toggleEditUsername(): void {
    this.isEditingUsername = true;
  }

  toggleEditEmail(): void {
    this.isEditingEmail = true;
  }

  saveProfile(): void {
    console.log('Updating profile with data:', this.profile);
    this.authService.updateProfile(this.profile).subscribe(
      (response) => {
        alert('Profile updated successfully.');
        this.isEditing = false;
        this.loadProfile();
      },
      (error) => {
        console.error('Error updating profile:', error);
        alert('Failed to update profile.');
      }
    );
  }

  saveUsername(): void {
    this.authService
      .updateProfile({ username: this.profile.username })
      .subscribe(
        (response) => {
          alert('Username updated successfully.');
          this.isEditingUsername = false;
          this.loadProfile();
        },
        (error) => {
          console.error('Error updating username:', error);
          alert('Failed to update username.');
        }
      );
  }

  saveEmail(): void {
    this.authService.updateProfile({ email: this.profile.email }).subscribe(
      (response) => {
        alert('Email updated successfully.');
        this.isEditingEmail = false;
        this.loadProfile();
      },
      (error) => {
        console.error('Error updating email:', error);
        alert('Failed to update email.');
      }
    );
  }

  cancelEditUsername(): void {
    this.isEditingUsername = false;
    this.loadProfile();
  }

  cancelEditEmail(): void {
    this.isEditingEmail = false;
    this.loadProfile();
  }

  cancelEdit(): void {
    this.isEditing = false;
    this.loadProfile();
  }

  onUsernameChange(username: string): void {
    this.authService.checkUsernameAvailability(username).subscribe(
      (response) => {
        this.usernameAvailable = response.available;
      },
      (error) => {
        console.error('Error checking username availability:', error);
      }
    );
  }

  onEmailChange(email: string): void {
    this.authService.checkEmailAvailability(email).subscribe(
      (response) => {
        this.emailAvailable = response.available;
      },
      (error) => {
        console.error('Error checking email availability:', error);
      }
    );
  }
}
