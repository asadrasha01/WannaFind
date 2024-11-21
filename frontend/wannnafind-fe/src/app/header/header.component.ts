import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import { Router } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';

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

  constructor(
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  ngOnInit(): void {
    // Check if localStorage is accessible
    if (isPlatformBrowser(this.platformId)) {
      const token = localStorage.getItem('token');
      this.isAuthenticated = !!token;

      if (this.isAuthenticated) {
        const userData = JSON.parse(localStorage.getItem('user') || '{}');
        this.user.username = userData.username || 'Guest';

        if (userData.avatar) {
          this.user.avatar = userData.avatar;
        } else {
          const firstName = userData.firstName || 'A';
          const lastName = userData.lastName || 'R';
          this.user.initials = `${firstName.charAt(0)}${lastName.charAt(0)}`;
        }
      }
    }
  }

  toggleDropdown(): void {
    this.isDropdownOpen = !this.isDropdownOpen;
  }

  redirectToLogin(): void {
    this.router.navigate(['/']);
  }

  logout(): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
    this.isAuthenticated = false;
    this.router.navigate(['/']);
  }
}
