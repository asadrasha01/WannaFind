import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { HeaderComponent } from './header.component';

describe('HeaderComponent', () => {
  let component: HeaderComponent;
  let fixture: ComponentFixture<HeaderComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HeaderComponent],
      imports: [RouterTestingModule], // Import RouterTestingModule for routing
    }).compileComponents();

    fixture = TestBed.createComponent(HeaderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should toggle dropdown', () => {
    component.isDropdownOpen = false;
    component.toggleDropdown();
    expect(component.isDropdownOpen).toBeTrue();
  });

  it('should redirect to login if not authenticated', () => {
    spyOn(component['router'], 'navigate');
    component.redirectToLogin();
    expect(component['router'].navigate).toHaveBeenCalledWith(['/']);
  });

  it('should log out user', () => {
    spyOn(component['router'], 'navigate');
    localStorage.setItem('token', 'test-token');
    localStorage.setItem(
      'user',
      JSON.stringify({ firstName: 'Test', lastName: 'User' })
    );

    component.logout();

    expect(localStorage.getItem('token')).toBeNull();
    expect(localStorage.getItem('user')).toBeNull();
    expect(component['router'].navigate).toHaveBeenCalledWith(['/']);
  });
});
