import { NgModule } from '@angular/core';
import {
  BrowserModule,
  provideClientHydration,
} from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { provideHttpClient } from '@angular/common/http'; // Updated import

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { ListingPageComponent } from './pages/home-page/listing-page/listing-page.component';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component';
import { PasswordResetComponent } from './pages/password-reset/password-reset.component';

@NgModule({
  declarations: [
    AppComponent,
    HomePageComponent,
    ListingPageComponent,
    HeaderComponent,
    FooterComponent,
    LoginComponent,
    RegisterComponent,
    PasswordResetComponent,
  ],
  imports: [BrowserModule, AppRoutingModule, FormsModule], // Removed HttpClientModule
  providers: [provideClientHydration(), provideHttpClient()], // Updated providers
  bootstrap: [AppComponent],
})
export class AppModule {}
