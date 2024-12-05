import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-submit-item',
  templateUrl: './submit-item.component.html',
  styleUrls: ['./submit-item.component.scss'],
})
export class SubmitItemComponent {
  itemData = {
    title: '',
    description: '',
    category: '',
    condition: '',
    brand: '',
  };
  selectedFile: File | null = null;
  categories: string[] = ['Electronics', 'Fashion', 'Home', 'Books', 'Sports'];
  successMessage: string = '';
  errorMessage: string = '';

  constructor(private authService: AuthService) {}

  onFileSelect(event: any): void {
    this.selectedFile = event.target.files[0];
  }

  submitItem(): void {
    if (
      !this.itemData.title ||
      !this.itemData.description ||
      !this.itemData.category ||
      !this.itemData.condition ||
      !this.selectedFile
    ) {
      this.errorMessage = 'Please fill out all required fields.';
      return;
    }

    const formData = new FormData();
    formData.append('title', this.itemData.title);
    formData.append('description', this.itemData.description);
    formData.append('category', this.itemData.category.toLowerCase());
    formData.append('condition', this.itemData.condition);
    formData.append('brand', this.itemData.brand);
    if (this.selectedFile) formData.append('image', this.selectedFile);

    this.authService.submitItemRequest(formData).subscribe(
      (response) => {
        console.log('Item submitted:', response);
        this.successMessage =
          response.message || 'Item submitted successfully!';
        this.errorMessage = '';
        this.resetForm();
      },
      (error) => {
        console.error('Error submitting item:', error);
        this.errorMessage =
          error.error?.errors?.category ||
          'Error submitting item. Please try again.';
        this.successMessage = '';
      }
    );
  }

  resetForm(): void {
    this.itemData = {
      title: '',
      description: '',
      category: '',
      condition: '',
      brand: '',
    };
    this.selectedFile = null;
    this.errorMessage = '';

    // Clear the file input in the DOM
    const fileInput = document.getElementById('image') as HTMLInputElement;
    if (fileInput) {
      fileInput.value = ''; // Clear the file input value
    }
  }
}
