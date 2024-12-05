import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-my-requests',
  templateUrl: './my-requests.component.html',
  styleUrls: ['./my-requests.component.scss'],
})
export class MyRequestsComponent implements OnInit {
  requests: any[] = [];
  errorMessage: string = '';

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.loadMyRequests();
  }

  loadMyRequests(): void {
    this.authService.getMyRequests().subscribe(
      (response) => {
        this.requests = response;
      },
      (error) => {
        console.error('Error fetching requests:', error);
        this.errorMessage = 'Failed to load requests. Please try again later.';
      }
    );
  }

  toggleStatus(request: any): void {
    this.authService.toggleItemStatus(request.id).subscribe(
      (response) => {
        request.active = !request.active; // Toggle the active status
      },
      (error) => {
        console.error('Error toggling status:', error);
        this.errorMessage = 'Failed to toggle request status.';
      }
    );
  }

  deleteRequest(itemId: number): void {
    if (!confirm('Are you sure you want to delete this request?')) {
      return;
    }

    this.authService.deleteRequest(itemId).subscribe(
      () => {
        // Remove the request from the list
        this.requests = this.requests.filter(
          (request) => request.id !== itemId
        );
        this.errorMessage = ''; // Clear any previous error message
      },
      (error) => {
        console.error('Error deleting request:', error);
        this.errorMessage = 'Failed to delete request.';
      }
    );
  }

  private getAuthHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({
      Authorization: `Token ${token}`,
      'Content-Type': 'application/json',
    });
  }
}
