import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private apiUrl = 'http://127.0.0.1:8000/api'; // Base API URL

  constructor(private http: HttpClient) {}

  register(userData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/register/`, userData);
  }

  login(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/login/`, data);
  }

  saveToken(token: string): void {
    if (typeof window !== 'undefined' && localStorage) {
      localStorage.setItem('token', token);
    }
  }

  isAuthenticated(): boolean {
    const token = localStorage.getItem('token');
    return !!token;
  }

  logout(): Observable<any> {
    return this.http.post(`${this.apiUrl}/logout/`, {});
  }

  getProfile(): Observable<any> {
    return this.http.get(`${this.apiUrl}/profile/`, {
      headers: this.getAuthHeaders(),
    });
  }

  getUserProfile(userId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/user-profile/${userId}/`, {
      headers: this.getAuthHeaders(),
    });
  }

  updateProfile(payload: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/profile/`, payload, {
      headers: this.getAuthHeaders(),
    });
  }

  checkUsernameAvailability(username: string): Observable<any> {
    return this.http.get<any>(
      `${this.apiUrl}/check-username/?username=${username}`,
      {
        headers: this.getAuthHeaders(),
      }
    );
  }

  checkEmailAvailability(email: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/check-email/?email=${email}`, {
      headers: this.getAuthHeaders(),
    });
  }

  uploadProfileImage(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('profile_image', file);

    return this.http.post<any>(
      `${this.apiUrl}/upload-profile-image/`,
      formData,
      {
        headers: this.getAuthHeaders(false), // Disable Content-Type header for FormData
      }
    );
  }

  passwordResetRequest(email: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/password-reset/`, { email });
  }

  passwordResetConfirm(
    uidb64: string,
    token: string,
    newPassword: string
  ): Observable<any> {
    return this.http.post(
      `${this.apiUrl}/password-reset-confirm/${uidb64}/${token}/`,
      { new_password: newPassword }
    );
  }

  changePassword(
    currentPassword: string,
    newPassword: string
  ): Observable<any> {
    return this.http.post(`${this.apiUrl}/change-password/`, {
      current_password: currentPassword,
      new_password: newPassword,
    });
  }

  // Get Authorization headers
  getAuthHeaders(includeToken: boolean = true): HttpHeaders {
    const headers: { [key: string]: string } = {
      'Content-Type': 'application/json',
    };

    if (includeToken && typeof window !== 'undefined' && localStorage) {
      const token = localStorage.getItem('token');
      if (token) {
        headers['Authorization'] = `Token ${token}`;
      }
    }

    return new HttpHeaders(headers);
  }

  submitItemRequest(data: FormData): Observable<any> {
    const url = `${this.apiUrl}/submit-item/`;
    const headers = new HttpHeaders({
      Authorization: `Token ${localStorage.getItem('token')}`,
    });
    // Debug log the data being sent
    data.forEach((value, key) => {
      console.log(`${key}: ${value}`);
    });

    return this.http.post(url, data, { headers });
  }

  getItemList(): Observable<any> {
    const url = `${this.apiUrl}/item-list/`;
    const headers = this.getAuthHeaders();
    return this.http.get(url, { headers });
  }

  getItemDetail(itemId: string): Observable<any> {
    const url = `${this.apiUrl}/item-request-detail/${itemId}/`;
    const headers = this.getAuthHeaders();
    return this.http.get(url, { headers });
  }

  getMyRequests(): Observable<any> {
    const url = `${this.apiUrl}/my-requests/`;
    const headers = this.getAuthHeaders();
    return this.http.get(url, { headers }); // Pass headers in the options object
  }

  // Toggle item active/inactive status
  toggleItemStatus(itemId: number): Observable<any> {
    const url = `${this.apiUrl}/toggle-item-status/${itemId}/`;
    const headers = this.getAuthHeaders();
    return this.http.post(url, {}, { headers });
  }

  deleteRequest(itemId: number): Observable<any> {
    const url = `${this.apiUrl}/delete-request/${itemId}/`; // Ensure this matches api_urls.py
    const headers = this.getAuthHeaders();
    return this.http.delete(url, { headers });
  }

  sendRequest(
    itemId: number,
    messageContent: string,
    receiverId?: number
  ): Observable<any> {
    const payload: any = {
      content: messageContent,
    };

    // If the item is self-posted, include receiver_id
    if (receiverId) {
      payload.receiver_id = receiverId;
    }

    return this.http.post<any>(
      `${this.apiUrl}/send-message/${itemId}/`,
      payload,
      {
        headers: this.getAuthHeaders(),
      }
    );
  }

  getNotifications(): Observable<any> {
    const url = `${this.apiUrl}/notifications/`;
    const headers = this.getAuthHeaders();
    return this.http.get(url, { headers });
  }

  acceptNotification(messageId: number): Observable<any> {
    const url = `${this.apiUrl}/notifications/accept/${messageId}/`;
    const headers = this.getAuthHeaders();
    return this.http.post(url, {}, { headers });
  }

  rejectNotification(messageId: number): Observable<any> {
    const url = `${this.apiUrl}/notifications/reject/${messageId}/`;
    const headers = this.getAuthHeaders();
    return this.http.delete(url, { headers });
  }

  getChatList(): Observable<any> {
    const url = `${this.apiUrl}/chat-list/`;
    const headers = this.getAuthHeaders();
    return this.http.get(url, { headers });
  }

  getChatMessages(itemId: number, otherUserId: number): Observable<any> {
    const url = `${this.apiUrl}/chat-messages/${itemId}/${otherUserId}/`;
    const headers = this.getAuthHeaders();
    return this.http.get(url, { headers });
  }

  sendChatMessage(
    receiverId: number,
    content: string,
    itemId: number
  ): Observable<any> {
    const url = `${this.apiUrl}/send-chat-message/`;
    const headers = this.getAuthHeaders();
    const body = { receiver_id: receiverId, content, item_id: itemId };
    return this.http.post(url, body, { headers });
  }

  closeDeal(itemId: number, otherUserId: number): Observable<any> {
    const url = `${this.apiUrl}/close-deal/${itemId}/${otherUserId}/`;
    return this.http.post(url, {}, { headers: this.getAuthHeaders() });
  }

  deleteChat(itemId: number, otherUserId: number): Observable<any> {
    const url = `${this.apiUrl}/delete-chat/${itemId}/${otherUserId}/`;
    return this.http.delete(url, { headers: this.getAuthHeaders() });
  }

  leaveFeedback(
    revieweeId: number,
    comment: string,
    rating: number
  ): Observable<any> {
    const url = `${this.apiUrl}/leave-feedback/${revieweeId}/`;
    return this.http.post(
      url,
      { comment, rating },
      { headers: this.getAuthHeaders() }
    );
  }
}
