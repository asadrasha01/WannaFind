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

  getUserProfile(): Observable<any> {
    const url = `${this.apiUrl}/profile/`;
    const headers = this.getAuthHeaders();
    return this.http.get(url, { headers });
  }

  updateUserProfile(data: any): Observable<any> {
    const url = `${this.apiUrl}/profile/`;
    const headers = this.getAuthHeaders();
    return this.http.put(url, data, { headers });
  }

  checkUsernameAvailability(
    username: string
  ): Observable<{ available: boolean }> {
    return this.http.post<{ available: boolean }>(
      `${this.apiUrl}/check-username/`,
      { username }
    );
  }

  checkEmailAvailability(email: string): Observable<{ available: boolean }> {
    return this.http.post<{ available: boolean }>(
      `${this.apiUrl}/check-email/`,
      { email }
    );
  }

  updateProfileImage(formData: FormData): Observable<any> {
    const url = `${this.apiUrl}/profile/`; // Assuming the same endpoint handles profile image updates
    const headers = this.getAuthHeaders();
    return this.http.put(url, formData, { headers });
  }

  updateProfile(data: any): Observable<any> {
    const headers = this.getAuthHeaders();
    return this.http.put(`${this.apiUrl}/profile/`, data, { headers });
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
  getAuthHeaders(): HttpHeaders {
    if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
      const token = localStorage.getItem('token');
      if (token) {
        console.log('Using token:', token); // Debug log
        return new HttpHeaders({
          Authorization: `Token ${token}`,
          'Content-Type': 'application/json',
        });
      } else {
        console.error('Authentication token is missing.');
        throw new Error('User is not authenticated.');
      }
    } else {
      console.error('localStorage is not available in this environment.');
      throw new Error('localStorage is not accessible.');
    }
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
    return this.http.get(url, { headers }); // Pass headers in the options object
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
    content: string,
    receiverId?: number
  ): Observable<any> {
    const url = `${this.apiUrl}/send-message/${itemId}/`;
    const headers = this.getAuthHeaders();
    const body = {
      content,
      receiver_id: receiverId, // Optional
    };

    return this.http.post(url, body, { headers });
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
}
