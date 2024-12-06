import { NgModule } from '@angular/core';
import {
  BrowserModule,
  provideClientHydration,
} from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { provideHttpClient } from '@angular/common/http';
import { withFetch } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { HttpClientModule } from '@angular/common/http';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { RegisterComponent } from './pages/register/register.component';
import { LoginComponent } from './pages/login/login.component';
import { PasswordResetComponent } from './pages/password-reset/password-reset.component';
import { ProfileComponent } from './pages/profile/profile.component';
import { SubmitItemComponent } from './pages/submit-item/submit-item.component';
import { ItemListComponent } from './pages/item-list/item-list.component';
import { ItemDetailComponent } from './pages/item-detail/item-detail.component';
import { MyRequestsComponent } from './pages/my-requests/my-requests.component';
import { NotificationsComponent } from './pages/notifications/notifications.component';
import { ChatComponent } from './pages/chat/chat.component';
import { SafeUrlPipe } from './safe-url.pipe';


@NgModule({
  declarations: [
    AppComponent,
    HomePageComponent,
    HeaderComponent,
    FooterComponent,
    RegisterComponent,
    LoginComponent,
    PasswordResetComponent,
    ProfileComponent,
    ItemListComponent,
    SubmitItemComponent,
    ItemDetailComponent,
    MyRequestsComponent,
    NotificationsComponent,
    ChatComponent,
    SafeUrlPipe,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    RouterModule,
    CommonModule,
  ],
  providers: [provideClientHydration(), provideHttpClient(withFetch())],
  bootstrap: [AppComponent],
})
export class AppModule {}
