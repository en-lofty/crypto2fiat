import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { HomeRoutingModule } from './home-routing.module';

import { HomeComponent } from './home.component';
import { SharedModule } from '../shared/shared.module';
import {NbButtonModule, NbIconModule, NbInputModule, NbSelectModule, NbSpinnerModule, NbTooltipModule} from '@nebular/theme';
import {FormsModule} from '@angular/forms';

@NgModule({
  declarations: [HomeComponent],
  imports: [CommonModule, SharedModule, HomeRoutingModule, NbIconModule, NbSelectModule, NbInputModule, NbButtonModule, FormsModule, NbSpinnerModule, NbTooltipModule]
})
export class HomeModule {}
