import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent implements OnInit {
  isAuthenticated = false;
  isDropdownOpen = false;
  user: { avatar?: string; initials: string; username?: string } = {
    initials: '',
    username: '',
  };

  constructor(private router: Router) {}

  ngOnInit(): void {
    if (this.isBrowser()) {
      const token = localStorage.getItem('token');
      this.isAuthenticated = !!token;

      if (this.isAuthenticated) {
        const userData = JSON.parse(localStorage.getItem('user') || '{}');

        // Ensure username exists and extract initials
        if (userData.username) {
          this.user.username = userData.username; // Assign username
          this.user.initials = userData.username.slice(0, 2).toUpperCase(); // Extract initials
        } else {
          this.user.initials = 'GU'; // Fallback if username is missing
        }

        // Handle avatar
        this.user.avatar = userData.avatar || '';
      }
    }
  }

  toggleDropdown(): void {
    this.isDropdownOpen = !this.isDropdownOpen;
  }

  redirectToLogin(): void {
    this.router.navigate(['/']);
    setTimeout(() => {
      document.querySelector('#login-section')?.scrollIntoView({
        behavior: 'smooth',
      });
    }, 200); // Ensure smooth scrolling after route navigation
  }

  logout(): void {
    if (this.isBrowser()) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
    this.isAuthenticated = false;
    this.router.navigate(['/']);
  }

  private isBrowser(): boolean {
    return typeof window !== 'undefined' && typeof localStorage !== 'undefined';
  }
}
