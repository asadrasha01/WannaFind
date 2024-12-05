import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-notifications',
  templateUrl: './notifications.component.html',
  styleUrls: ['./notifications.component.scss'],
})
export class NotificationsComponent implements OnInit {
  notifications: any[] = [];
  errorMessage: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit(): void {
    this.loadNotifications();
  }

  loadNotifications(): void {
    this.authService.getNotifications().subscribe(
      (response) => {
        this.notifications = response;
      },
      (error) => {
        console.error('Error loading notifications:', error);
        this.errorMessage = 'Failed to load notifications.';
      }
    );
  }

  acceptNotification(messageId: number): void {
    this.authService.acceptNotification(messageId).subscribe(
      (response) => {
        alert('Notification accepted.');
        this.notifications = this.notifications.filter(
          (notification) => notification.id !== messageId
        );
        this.router.navigate(['/chat']);
      },
      (error) => {
        console.error('Error accepting notification:', error);
      }
    );
  }

  rejectNotification(messageId: number): void {
    this.authService.rejectNotification(messageId).subscribe(
      (response) => {
        alert('Notification rejected.');
        this.notifications = this.notifications.filter(
          (notification) => notification.id !== messageId
        );
      },
      (error) => {
        console.error('Error rejecting notification:', error);
      }
    );
  }
}
