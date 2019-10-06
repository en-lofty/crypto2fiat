import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {ConverterService} from '../core/services/converter.service';
import {Subject, Subscription} from 'rxjs';
import {debounceTime} from 'rxjs/operators';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  model = {
    currency: '',
    fiat: '',
    quantity: 0
  };
  answer = -1;
  swapDirection = false;
  loading = false;
  res = {
    swap: () => `Converting ${this.model.quantity}
    ${this.swapDirection ? this.model.fiat : this.model.currency.toLocaleUpperCase()} to
    ${!this.swapDirection ? this.model.fiat : this.model.currency.toLocaleUpperCase()}`
  };
  private subscription: Subscription;
  private inputChanged = new Subject<string>();
  private debounceTime = 1000;

  // inject conversion service
  constructor(private converterService: ConverterService,
              private changeDetectorRef: ChangeDetectorRef) {
    this.converterService.answer$.subscribe(num => {
      this.answer = num;
      this.loading = false;
      changeDetectorRef.detectChanges();
    });
  }

  ngOnInit(): void {
    this.subscription = this.inputChanged
      .pipe(debounceTime(this.debounceTime))
      .subscribe(() => this.convert());
  }

  get fiats(): string[] {
    return this.converterService.fiatCurrencies;
  }

  // create calculate function

  convert() {
    if (this.model.currency && this.model.currency.length > 2 && this.model.fiat && this.model.quantity) {
      this.loading = true;
      console.log('Converting...', this.model, this.swapDirection ? '--reverse' : '');
      this.converterService.convert(
        this.model.currency,
        this.model.fiat,
        this.model.quantity,
        this.swapDirection);
    }
  }
}
