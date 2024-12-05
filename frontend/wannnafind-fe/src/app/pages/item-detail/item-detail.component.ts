import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-item-detail',
  templateUrl: './item-detail.component.html',
  styleUrls: ['./item-detail.component.scss'],
})
export class ItemDetailComponent implements OnInit {
  item: any = null; // Object to hold the item details
  loading: boolean = false; // To manage the loading state
  errorMessage: string = ''; // To display error messages if fetching fails

  constructor(
    private route: ActivatedRoute,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    const itemId = this.route.snapshot.paramMap.get('id'); // Get the item ID from the route
    if (itemId) {
      this.fetchItemDetails(itemId); // Fetch item details using the ID
    }
  }

  fetchItemDetails(itemId: string): void {
    this.loading = true; // Show loading indicator
    this.errorMessage = ''; // Clear any previous error messages

    this.authService.getItemDetail(itemId).subscribe(
      (response: any) => {
        this.item = response; // Assign fetched item to the object
        this.loading = false; // Hide the loading indicator
      },
      (error) => {
        console.error('Error fetching item details:', error);
        this.errorMessage =
          'Failed to fetch item details. Please try again later.';
        this.loading = false; // Hide the loading indicator
      }
    );
  }
}
