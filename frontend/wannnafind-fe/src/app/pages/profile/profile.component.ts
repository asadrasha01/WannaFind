import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent {
  profile: any = {};
  editingField: string | null = null; // 'general', 'username', 'email'
  editValue: string = '';
  availabilityStatus: string = ''; // 'available', 'unavailable', 'error'
  availabilityMessage: string = '';

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.loadProfile();
  }

  // Load user profile from backend
  loadProfile(): void {
    this.authService.getProfile().subscribe(
      (profile) => {
        this.profile = profile;
        console.log('Loaded profile:', this.profile);
      },
      (error) => {
        console.error('Error loading profile:', error);
      }
    );
  }

  // Get initials from name and surname
  getInitials(name: string, surname: string): string {
    return ((name?.[0] || '') + (surname?.[0] || '')).toUpperCase();
  }

  // Initiate editing of a specific field
  editField(field: string): void {
    this.editingField = field;
    if (field === 'username' || field === 'email') {
      this.editValue = this.profile[field];
    } else if (field === 'general') {
      // No single editValue for general fields
    }
    this.availabilityStatus = '';
    this.availabilityMessage = '';
  }

  // Cancel editing
  cancelEdit(): void {
    this.editingField = null;
    this.editValue = '';
    this.availabilityStatus = '';
    this.availabilityMessage = '';
    this.loadProfile(); // Reload profile to discard unsaved changes
  }

  // Check availability for username and email
  checkAvailability(field: string, value: string): void {
    this.availabilityStatus = '';
    this.availabilityMessage = '';

    if (!value) return;

    const apiCall =
      field === 'username'
        ? this.authService.checkUsernameAvailability(value)
        : this.authService.checkEmailAvailability(value);

    apiCall.subscribe(
      (response: any) => {
        this.availabilityStatus = response.available
          ? 'available'
          : 'unavailable';
        this.availabilityMessage = response.message;
      },
      (error) => {
        this.availabilityStatus = 'error';
        this.availabilityMessage = 'Error checking availability.';
      }
    );
  }

  // Save edited field
  saveField(field: string): void {
    if (field === 'username' || field === 'email') {
      const updateData: any = { [field]: this.editValue };
      this.authService.updateProfile(updateData).subscribe(
        (data) => {
          this.profile[field] = data[field];
          this.cancelEdit();
        },
        (error) => {
          console.error(`Error updating ${field}:`, error);
          if (error.error && error.error.error) {
            this.availabilityStatus = 'unavailable';
            this.availabilityMessage = error.error.error;
          }
        }
      );
    } else if (field === 'general') {
      const updateData: any = {
        name: this.profile.profile.name,
        surname: this.profile.profile.surname,
        phone_number: this.profile.profile.phone_number,
        city: this.profile.profile.city,
        country: this.profile.profile.country,
      };
      this.authService.updateProfile(updateData).subscribe(
        (data) => {
          this.profile = data;
          this.cancelEdit();
        },
        (error) => {
          console.error('Error updating profile:', error);
        }
      );
    }
  }

  // Handle profile image selection
  onProfileImageSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.authService.uploadProfileImage(file).subscribe({
        next: (response) => {
          this.profile.profile.profile_image = response.profile_image;
        },
        error: (err) => {
          console.error('Error uploading image:', err);
        },
      });
    }
  }
}
