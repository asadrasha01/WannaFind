import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'],
})
export class HomePageComponent {
  loginData = {
    username: '',
    password: '',
  };
  showPassword = false;
  errorMessage: string | null = null;

  constructor(private authService: AuthService, private router: Router) {}

  navigateToItemList() {
    console.log('Navigating to item list...');
    this.router.navigate(['/item-list']); // Ensure the route matches the app's route configuration
  }

  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  onSubmit(): void {
    this.authService.login(this.loginData).subscribe(
      (response: any) => {
        // Save the token
        this.authService.saveToken(response.token);

        // Redirect to the profile page or dashboard
        this.router.navigate(['/profile']);
      },
      (error: any) => {
        this.errorMessage = 'Invalid username or password.';
      }
    );
  }
  onFindWhatYouNeed(): void {
    if (this.authService.isAuthenticated()) {
      // Navigate to the desired page if logged in
      this.router.navigate(['/item-list']);
    } else {
      // Redirect to login if not logged in
      this.router.navigate(['/']);
      setTimeout(() => {
        document.querySelector('#login-section')?.scrollIntoView({
          behavior: 'smooth',
        });
      }, 200);
    }
  }
}
