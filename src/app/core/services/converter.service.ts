import {Injectable} from '@angular/core';
import {exec} from 'child_process';
import {Subject} from 'rxjs';
import {NbGlobalPhysicalPosition, NbToastrService} from '@nebular/theme';

@Injectable({
  providedIn: 'root'
})
export class ConverterService {
  // create variable holding all available FIAT currencies
  fiatCurrencies = [
    'USD', 'AUD', 'BRL', 'CAD', 'CHF', 'CLP', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP', 'HKD',
    'HUF', 'IDR', 'ILS', 'INR', 'JPY', 'KRW', 'MXN', 'MYR', 'NOK', 'NZD', 'PHP',
    'PKR', 'PLN', 'RUB', 'SEK', 'SGD', 'THB', 'TRY', 'TWD', 'ZAR'
  ];
  public answer$ = new Subject<number>();

  constructor(private toastrService: NbToastrService) {
  }

  // create function that sends calls to crypto2fiat
  convert(cryptoName: string, fiatName: string, amount: number,
          swapDirection: boolean = true) {
    const argList = [`${cryptoName}`,
      `${fiatName}`,
      `${amount}`,
      `${!swapDirection ? '' : '--reverse'}`];
    const argString = argList.join(' ').trimRight();
    console.log('Running: c2f', argString);
    const convert = exec(`/home/raphael/.local/bin/c2f ${argString}`);
    convert.stdout.on('data', (data) => {
      console.log('Received data:', data);
      this.answer$.next(data);
    });
    convert.stderr.on('data', (error) => {
      console.log('Error data received from c2f:', error);
      this.answer$.next(-1);
      this.toastrService.danger(error, 'Error', {
        destroyByClick: true,
        icon: 'slash-outline', preventDuplicates: true,
        position: NbGlobalPhysicalPosition.TOP_RIGHT,
        duplicatesBehaviour: 'previous'
      });
    });
  }

}
