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

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.loadPreviousChats();
  }

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

  openChat(userId: number, itemId: number): void {
    this.selectedUser = this.previousChats.find(
      (chat) => chat.userId === userId
    );
    this.selectedItemId = itemId;

    this.authService.getChatMessages(itemId, userId).subscribe(
      (response) => {
        this.currentChat = response;
      },
      (error) => {
        console.error('Error loading chat messages:', error);
      }
    );
  }

  sendMessage(): void {
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
          }
        );
    } else {
      alert('Message content cannot be empty.');
    }
  }
}
