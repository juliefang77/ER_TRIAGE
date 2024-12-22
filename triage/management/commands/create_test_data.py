from django.core.management.base import BaseCommand
from triage.models import Patient, MedicalStaff, TriageRecord, VitalSigns
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Creates test data for the ER Triage system'

    def handle(self, *args, **kwargs):
        # Create Medical Staff
        staff_data = [
            {
                'staff_id': 'DOC001',
                'name': '张医生',
                'role': 'DOC',
                'department': '急诊科'
            },
            {
                'staff_id': 'NUR001',
                'name': '李护士',
                'role': 'NUR',
                'department': '急诊科'
            },
            {
                'staff_id': 'ADM001',
                'name': '王管理',
                'role': 'ADM',
                'department': '行政'
            }
        ]

        for staff in staff_data:
            MedicalStaff.objects.create(**staff)
        self.stdout.write('Created medical staff')

        # Create Patients
        patient_data = [
            {
                'id_type': 'ID',
                'id_number': '110101199001011234',
                'name_chinese': '张三',
                'pinyin_name': 'zhang san',
                'gender': 'M',
                'date_of_birth': '1990-01-01',
                'phone': '13800138000',
                'blood_type': 'A+',
                'emergency_contact': '张四',
                'emergency_phone': '13900139000'
            },
            {
                'id_type': 'ID',
                'id_number': '110101199207084321',
                'name_chinese': '李梅',
                'pinyin_name': 'li mei',
                'gender': 'F',
                'date_of_birth': '1992-07-08',
                'phone': '13811138111',
                'blood_type': 'B+',
                'emergency_contact': '李华',
                'emergency_phone': '13911139111'
            }
        ]

        created_patients = []
        for patient in patient_data:
            created_patients.append(Patient.objects.create(**patient))
        self.stdout.write('Created patients')

        # Create Triage Records
        nurse = MedicalStaff.objects.get(staff_id='NUR001')
        
        for patient in created_patients:
            triage = TriageRecord.objects.create(
                patient=patient,
                nurse=nurse,
                arrival_method='WALK',
                chief_complaint='发烧，咳嗽三天',
                medical_history='无特殊病史',
                priority_level=random.randint(2, 4),
                area='YELLOW',
                treatment_area='TREAT',
                department='急诊内科',
                preliminary_diagnosis='疑似上呼吸道感染'
            )

            # Create Vital Signs for each triage record
            VitalSigns.objects.create(
                triage_record=triage,
                temperature=round(random.uniform(37.5, 39.0), 1),
                systolic_bp=random.randint(110, 140),
                diastolic_bp=random.randint(60, 90),
                heart_rate=random.randint(60, 100),
                respiratory_rate=random.randint(16, 20),
                oxygen_saturation=random.randint(95, 100),
                avpu_status='A',
                pain_score=random.randint(1, 5)
            )

        self.stdout.write(self.style.SUCCESS('Successfully created all test data'))