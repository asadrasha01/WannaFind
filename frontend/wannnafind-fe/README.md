Here's a comprehensive `README.md` template for your **WannFind** project:

---

# **WannFind**

**WannFind** is a platform that facilitates seamless communication and exchange between users. Users can list items, request items, chat with other users, and manage their profiles efficiently. The platform integrates a robust backend with an interactive frontend for an optimized user experience.

---

## **Features**

### **Frontend**

- **User Authentication**: Login, logout, and token-based authentication.
- **Profile Management**:
  - Edit user details (name, surname, username, email, profile picture).
  - View profile with initials displayed if no profile picture is uploaded.
- **Item Listing**:
  - Users can list items with images, categories, and descriptions.
  - Filter and browse through items listed by other users.
- **Chat System**:
  - Real-time communication between users.
  - View previous chats and ongoing conversations.
  - Includes functionality to close deals or delete chats.
- **Notification Management**:
  - Users are notified when messages are received.
  - Option to accept or reject message requests.

### **Backend**

- **API Endpoints**:
  - User profile management.
  - Item listing and retrieval.
  - Chat messaging, including notifications and deal management.
- **Authentication**:
  - Token-based authentication using Django REST Framework.
- **Database Models**:
  - Item, User, Profile, Message, and Notifications.
- **Robust Error Handling**:
  - Validates inputs and returns meaningful error responses.

---

## **Tech Stack**

### **Frontend**

- **Framework**: Angular
- **Styling**: SCSS
- **State Management**: Angular Services
- **Additional Libraries**:
  - `ngx-toastr`: Notifications for better UX.

### **Backend**

- **Framework**: Django REST Framework (DRF)
- **Database**: SQLite / PostgreSQL (configurable)
- **Authentication**: Token-based authentication using DRF's `TokenAuthentication`.

---

## **Installation**

### **Backend**

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/wannafind.git
   cd wannafind/backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/macOS
   venv\Scripts\activate     # For Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations and create a superuser:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

### **Frontend**

1. Navigate to the frontend directory:

   ```bash
   cd wannafind/frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Run the development server:

   ```bash
   npm start
   ```

4. Access the application at [http://localhost:4200](http://localhost:4200).

---

## **Usage**

1. **Sign up / Log in**:

   - Create a new account or log in using your credentials.
   - Manage your profile in the profile section.

2. **List Items**:

   - Navigate to the items section.
   - Add items with images and descriptions.

3. **Chat**:

   - View chat history in the chat section.
   - Start new conversations or continue existing ones.
   - Manage chats with options to close deals or delete conversations.

4. **Notifications**:
   - Check notifications for new messages.
   - Accept or reject chat requests.

---

## **API Endpoints**

### **Authentication**

- `POST /api/token/`: Obtain token.
- `POST /api/token/refresh/`: Refresh token.

### **User Profile**

- `GET /api/profile/`: Get user profile.
- `PUT /api/profile/`: Update user profile.

### **Items**

- `GET /api/items/`: List all items.
- `POST /api/items/`: Add a new item.
- `GET /api/items/<id>/`: Get item details.

### **Chat**

- `GET /api/chat-list/`: List all chats.
- `GET /api/chat-messages/<item_id>/<other_user_id>/`: Retrieve chat messages.
- `POST /api/send-chat-message/`: Send a chat message.

### **Notifications**

- `GET /api/notifications/`: List notifications.
- `POST /api/notifications/<id>/accept/`: Accept a notification.
- `DELETE /api/notifications/<id>/reject/`: Reject a notification.

---

## **Environment Variables**

Create a `.env` file in the backend directory with the following variables:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

---

## **Contributing**

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message"
   ```
4. Push the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Create a pull request.

---

## **License**

---

## **Contact**

- **Author**: Asadbek Rashidov
- **Email**: arashidov2001@gmail.com.com
- **GitHub**: [asadrasha01](https://github.com/asadrasha01)

---

This README provides detailed instructions and ensures developers and users can effectively interact with your WannFind project. You can customize the details (e.g., repository URL, contact info) as necessary.
