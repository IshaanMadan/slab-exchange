import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Subscription } from 'rxjs';
import { environment } from 'src/environments/environment';
import { DataService } from '../_providers/data.service';

@Component({
  selector: 'app-collections',
  templateUrl: './collections.component.html',
  styleUrls: ['./collections.component.less'],
})
export class CollectionsComponent implements OnInit, OnDestroy {
  allExpandState = false;
  collectionList = [];
  dropdownSubscription: Subscription;
  dropdownList: any;
  imageUrl = environment.apiUrl;
  editCardId = null;
  years = [];
  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    // Create Year Dropdown
    for (let i = 2021; i > 1969; i--) {
      let str = i.toString();
      this.years.push(i);
    }

    if (!this.dataService.formDropDownList) {
      this.dataService.getDropdownList();
      this.dropdownSubscription = this.dataService.dropdown.subscribe(
        (dropdown) => {
          if (!dropdown) {
            // dropdown  is empty
          } else {
            this.dropdownList = dropdown;
          }
        }
      );
    } else {
      this.dropdownList = this.dataService.formDropDownList[0];
    }

    this.getCardData()
  }

  ngOnDestroy() {
    if (this.dropdownSubscription) {
      this.dropdownSubscription.unsubscribe();
    }
  }

  deleteCard(index) {
    this.dataService
      .confirmBox('Are you sure want to delete?')
      .then((result) => {
        if (result.isConfirmed) {
          this.dataService.deleteCard(this.collectionList[index].id).subscribe(
            (response: any) => {
              if (response.success) {
                this.collectionList.splice(index, 1);
              }
            },
            (error) => {}
          );
        }
      });
  }

  findCategoryLabel(id) {
    const label = this.dropdownList.category.find((x) => x.id == id);
    return label ? label.category_name : null;
  }

  findCertificationLabel(id) {
    const label = this.dropdownList.certification.find((x) => x.id == id);
    return label ? label.certificate_name : null;
  }

  findCardGradeLabel(id) {
    const label = this.dropdownList.card_grade.find((x) => x.id == id);
    return label ? label.card_grade_name : null;
  }

  findAutoGradeLabel(id) {
    const label = this.dropdownList.auto_grade.find((x) => x.id == id);
    return label ? label.grade_name : null;
  }

  changeImage(index, type = 'front') {
    const id = `image_upload_${type}${index}`;
    const fileInput = document.getElementById(id);
    fileInput.click();
  }

  // ImageUpload

  imageUploaded($event, index, is_front) {
    if (!$event.target.files.length) {
      return;
    }
    const fromData = new FormData();
    fromData.append('image', $event.target.files[0]);

    const card_id = this.collectionList[index].id;

    this.dataService.uploadImage(fromData, is_front, card_id).subscribe(
      (response: any) => {
        if (is_front) {
          this.collectionList[index].front_thumbnail =
            response.data.front_thumbnail;
        } else {
          this.collectionList[index].back_thumbnail =
            response.data.back_thumbnail;
        }
      },
      (error) => {}
    );
  }

  updateCardData(index) {
    const cardData = {};
    cardData['card_id'] = this.collectionList[index].id;
    cardData['category'] = this.collectionList[index].category;
    cardData['year'] = this.collectionList[index].year;
    cardData['brand_name'] = this.collectionList[index].brand_name;
    cardData['player_name'] = this.collectionList[index].player_name;
    cardData['card_number'] = this.collectionList[index].card_number;
    cardData['certification'] = this.collectionList[index].certification;
    cardData['card_grade'] = this.collectionList[index].card_grade;
    cardData['certification_number'] = this.collectionList[
      index
    ].certification_number;
    cardData['autographed'] = this.collectionList[index].autographed
      ? true
      : false;

    if (this.collectionList[index].auto_grade) {
      cardData['auto_grade'] = this.collectionList[index].auto_grade;
    }

    this.dataService.saveCardDetails(cardData).subscribe(
      (response) => {
        if (response.success == 'False') {
          return;
        }
        this.getCardData()
        this.editCardId = null;
      },
      (error) => {}
    );
  }

  getCardData(){
    this.dataService.getCardList('done').subscribe(
      (response: any) => {
        this.collectionList = response.data;
        this.collectionList.forEach((element) => {
          element['category_label'] = this.findCategoryLabel(element.category);
          element['certification_label'] = this.findCertificationLabel(
            element.certification
          );
          element['card_grade_label'] = this.findCardGradeLabel(
            element.card_grade
          );
          element['auto_grade_label'] = this.findAutoGradeLabel(
            element.auto_grade
          );
        });
      },
      (error) => {
        this.collectionList = [];
      }
    );
  }
}
