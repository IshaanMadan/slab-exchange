import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { environment } from 'src/environments/environment';
import { DataService } from '../_providers/data.service';

@Component({
  selector: 'app-collections',
  templateUrl: './collections.component.html',
  styleUrls: ['./collections.component.less']
})
export class CollectionsComponent implements OnInit, OnDestroy {

  allExpandState = false;
  collectionList = [];
  dropdownSubscription: Subscription;
  dropdownList:any;
  imageUrl = environment.apiUrl

  constructor(
    private dataService: DataService
  ) { }

  ngOnInit(): void {
    this.dataService.getCardList('done')
    .subscribe((response: any) => {
      this.collectionList = response.data;
      this.collectionList.forEach(element => {
        element['category'] = this.findCategoryLabel(element.category)
        element['certification'] = this.findCertificationLabel(element.certification)
        element['card_grade'] = this.findCardGradeLabel(element.card_grade)
        element['auto_grade'] = this.findAutoGradeLabel(element.auto_grade)
      });
    }, error => {
      this.collectionList = [];
    })

    if(!this.dataService.formDropDownList) {
      this.dataService.getDropdownList();
      this.dropdownSubscription = this.dataService.dropdown.subscribe(dropdown => {
        if(!dropdown) {
          // dropdown  is empty
        } else {
          this.dropdownList = dropdown;
        }
      })

    } else {
      this.dropdownList = this.dataService.formDropDownList[0]
    }
  }

  ngOnDestroy() {
    if(this.dropdownSubscription) {
      this.dropdownSubscription.unsubscribe();
    }
  }

  deleteCard(index) {
    this.dataService
    .confirmBox('Are you sure want to delete?')
    .then((result) => {
      console.log(result);
      if (result.isConfirmed) {
        this.dataService.deleteCard(this.collectionList[index].id)
        .subscribe((response:any ) => {
          if(response.success) {
            this.collectionList.splice(index,1);
          }
        }, (error) => { });
      }
    });
  }

  findCategoryLabel(id) {
    const label = this.dropdownList.category.find(x => x.id == id)
    return label.category_name
  }

  findCertificationLabel(id) {
    const label = this.dropdownList.certification.find(x => x.id == id)
    return label.certificate_name
  }

  findCardGradeLabel(id) {
    const label = this.dropdownList.card_grade.find(x => x.id == id)
    return label.card_grade_name
  }

  findAutoGradeLabel(id) {
    const label = this.dropdownList.auto_grade.find(x => x.id == id)
    return label.grade_name
  }

}
