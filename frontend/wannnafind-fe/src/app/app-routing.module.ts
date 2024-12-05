import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { RegisterComponent } from './pages/register/register.component';
import { LoginComponent } from './pages/login/login.component';
import { PasswordResetComponent } from './pages/password-reset/password-reset.component';
import { ProfileComponent } from './pages/profile/profile.component';
import { SubmitItemComponent } from './pages/submit-item/submit-item.component';
import { ItemDetailComponent } from './pages/item-detail/item-detail.component';
import { MyRequestsComponent } from './pages/my-requests/my-requests.component';
import { ItemListComponent } from './pages/item-list/item-list.component';
import { AuthGuard } from './guards/auth.guard';
import { NotificationsComponent } from './pages/notifications/notifications.component';
import { ChatComponent } from './pages/chat/chat.component';


const routes: Routes = [
  { path: '', component: HomePageComponent }, // Default route
  { path: 'home', component: HomePageComponent }, // Optional: route for '/home'
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'password-reset', component: PasswordResetComponent },
  { path: 'profile', component: ProfileComponent, canActivate: [AuthGuard] },
  { path: 'submit-item', component: SubmitItemComponent },
  { path: 'item/:id', component: ItemDetailComponent },
  { path: 'item-list', component: ItemListComponent },
  { path: 'notifications', component: NotificationsComponent},
  {path: 'chat', component: ChatComponent},
  {
    path: 'my-requests',
    component: MyRequestsComponent,
    canActivate: [AuthGuard],
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
