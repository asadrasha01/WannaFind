import { Component, OnInit, HostListener } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router'; // Import Router

@Component({
  selector: 'app-item-list',
  templateUrl: './item-list.component.html',
  styleUrls: ['./item-list.component.scss'],
})
export class ItemListComponent implements OnInit {
  items: any[] = [];
  errorMessage: string = '';
  selectedItem: any = null;
  requestMessage: string = '';
  showRequestForm: boolean = false;

  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit(): void {
    this.loadItems();
  }

  loadItems(): void {
    this.authService.getItemList().subscribe(
      (response) => {
        this.items = response;
      },
      (error) => {
        if (error.status === 401) {
          this.errorMessage = 'Session expired. Please log in again.';
          // Redirect to login page or show a message
          this.router.navigate(['/']);
          setTimeout(() => {
            if (
              typeof window !== 'undefined' &&
              typeof document !== 'undefined'
            ) {
              document.querySelector('#login-section')?.scrollIntoView({
                behavior: 'smooth',
              });
            }
          }, 200);
        } else {
          this.errorMessage = 'Failed to load items. Please try again later.';
        }
      }
    );
  }

  openModal(item: any): void {
    this.selectedItem = item; // Sets the selected item
  }

  closeModal(): void {
    this.selectedItem = null; // Resets the selected item
    this.showRequestForm = false;
    this.requestMessage = '';
  }

  // Toggle request form
  toggleRequestForm(): void {
    this.showRequestForm = !this.showRequestForm;
  }

  // Send request to item owner
  sendRequest(): void {
    if (this.selectedItem && this.requestMessage.trim()) {
      this.authService
        .sendRequest(this.selectedItem.id, this.requestMessage)
        .subscribe(
          (response) => {
            alert('Request sent successfully!');
            this.showRequestForm = false;
            this.requestMessage = '';
          },
          (error) => {
            console.error('Error sending request:', error);
            alert('Failed to send request. Please try again.');
          }
        );
    } else {
      alert('Please enter a valid message.');
    }
  }

  // Cancel request form
  cancelRequest(): void {
    this.showRequestForm = false;
    this.requestMessage = '';
  }

  // Close modal when pressing Escape key
  @HostListener('document:keydown.escape', ['$event'])
  onEscapePressed(event: KeyboardEvent) {
    if (this.selectedItem) {
      this.closeModal();
    }
  }
}
