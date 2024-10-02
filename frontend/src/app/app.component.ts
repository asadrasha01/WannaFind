import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ItemService } from './services/item.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'], // Note: it should be styleUrls, not styleUrl
})
export class AppComponent implements OnInit {
  title = 'WannaFind'; // Define the title property
  items: any[] = [];

  constructor(private itemService: ItemService) {}

  ngOnInit() {
    this.itemService.getItems().subscribe(data => {
      this.items = data;
    });
  }
}
