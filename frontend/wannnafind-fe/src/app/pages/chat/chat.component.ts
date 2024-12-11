// src/app/pages/chat/chat.component.ts

import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss'],
})
export class ChatComponent implements OnInit {
  previousChats: any[] = [];
  currentChat: any[] = [];
  selectedUser: any = null;
  selectedItemId: number | null = null;
  newMessage: string = '';
  menuOpen: boolean = false;
  showUserInfo: boolean = false;
  userInfo: any = {};
  currentUser: any = {};
  dealClosed: boolean = false; // Indicates if the deal is closed for the selected item

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.loadPreviousChats();
    // Load current user info if needed
    this.authService.getProfile().subscribe((profile) => {
      this.currentUser = profile;
    });
  }

  // Load the list of previous chats
  loadPreviousChats(): void {
    this.authService.getChatList().subscribe(
      (response) => {
        this.previousChats = response;
      },
      (error) => {
        console.error('Error loading chat list:', error);
      }
    );
  }

  // Open a specific chat
  openChat(userId: number, itemId: number): void {
    this.selectedUser = this.previousChats.find(
      (chat) => chat.userId === userId
    );
    this.selectedItemId = itemId;

    this.authService.getChatMessages(itemId, userId).subscribe(
      (response) => {
        this.currentChat = response;
        // Check item status to lock messaging if deal is closed
        this.authService.getItemDetail(itemId.toString()).subscribe(
          (itemData) => {
            console.log('Item Data:', itemData); // Debug log
            if (itemData.active) {
              this.dealClosed = false;
              console.log('Deal is active.');
            } else {
              this.dealClosed = true;
              console.log('Deal is closed.');
            }
          },
          (error) => {
            console.error('Error fetching item details:', error);
            // In case of error, assume deal is closed to prevent messaging
            this.dealClosed = true;
          }
        );
      },
      (error) => {
        console.error('Error loading chat messages:', error);
      }
    );
  }

  // Send a message in the current chat
  sendMessage(): void {
    if (this.dealClosed) {
      alert('Deal closed. No further messages allowed.');
      return;
    }

    if (this.newMessage.trim() && this.selectedUser && this.selectedItemId) {
      this.authService
        .sendChatMessage(
          this.selectedUser.userId,
          this.newMessage,
          this.selectedItemId
        )
        .subscribe(
          (response) => {
            this.currentChat.push(response);
            this.newMessage = '';
          },
          (error) => {
            console.error('Error sending message:', error);
            if (error.error && error.error.error) {
              alert(error.error.error);
            }
          }
        );
    } else {
      alert('Message content cannot be empty.');
    }
  }

  // Toggle the options menu
  toggleMenu(): void {
    this.menuOpen = !this.menuOpen;
  }

  // Prompt user to leave feedback
  promptForFeedback(): void {
    const comment = prompt('Please leave your feedback:');
    const ratingStr = prompt('Rate from 1 to 5:');
    const rating = ratingStr ? parseInt(ratingStr, 10) : 5;

    if (comment && this.selectedUser) {
      this.authService
        .leaveFeedback(this.selectedUser.userId, comment, rating)
        .subscribe(
          (response) => {
            alert('Feedback submitted successfully!');
          },
          (error) => {
            console.error('Error submitting feedback:', error);
          }
        );
    }
  }

  // Close the deal (Temporarily Disabled on Backend)
  closeDeal(): void {
    this.menuOpen = false;
    if (this.selectedUser && this.selectedItemId) {
      this.authService
        .closeDeal(this.selectedItemId, this.selectedUser.userId)
        .subscribe(
          (response) => {
            alert(response.message);
            // After closing the deal, prompt for feedback
            this.promptForFeedback();
            // Also lock messaging now that the deal is closed
            this.dealClosed = true;
          },
          (error) => {
            console.error('Error closing deal:', error);
          }
        );
    }
  }

  // Delete the current chat
  deleteChat(): void {
    this.menuOpen = false;
    if (this.selectedUser && this.selectedItemId) {
      const userIdToDelete = this.selectedUser.userId;
      const itemIdToDelete = this.selectedItemId;

      this.authService.deleteChat(itemIdToDelete, userIdToDelete).subscribe(
        (response) => {
          alert(response.message);
          // Clear current chat
          this.currentChat = [];
          this.selectedUser = null;
          this.selectedItemId = null;

          // Remove the deleted chat from previousChats
          this.previousChats = this.previousChats.filter(
            (chat) =>
              !(
                chat.userId === userIdToDelete && chat.itemId === itemIdToDelete
              )
          );
        },
        (error) => {
          console.error('Error deleting chat:', error);
        }
      );
    }
  }

  // Get initials for a user (for avatars)
  getInitials(name: string, surname?: string): string {
    let initials = '';
    if (name) initials += name.charAt(0).toUpperCase();
    if (surname) initials += surname.charAt(0).toUpperCase();
    return initials;
  }

  // Open user info modal
  openUserInfo(userId: number): void {
    // Fetch user info from a dedicated endpoint that returns user profile including feedback
    this.authService.getUserProfile(userId).subscribe(
      (profile) => {
        this.userInfo = profile;
        this.showUserInfo = true;
      },
      (error) => {
        console.error('Error fetching user info:', error);
      }
    );
  }

  // Close user info modal
  closeUserInfo(): void {
    this.showUserInfo = false;
  }
}
