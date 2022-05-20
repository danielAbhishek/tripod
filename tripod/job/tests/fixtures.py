import random

from faker import Faker
from datetime import date, timedelta

from job.forms import JobReqCreateForm
from company.forms import (EventForm, PackageForm, ProductForm,
                           PackageLinkProductAddForm)
from settings.forms import (WorkflowForm, EmailTemplateForm, SourceForm,
                            WorkTemplateForm, WorkTypeForm,
                            ContractTemplateForm, QuestionnaireTemplateForm)


class JobFixtureSetup:

    def __init__(self, user, client, secondary_client, workflows, events,
                 packages, sources):
        self.faker = Faker()
        self.data = {}
        self.seed = 0
        self.jobs = ['Wedding', 'Birthday', 'pre-shoot']
        self.job_objs = []
        self.user = user
        self.client = client
        self.secondary_client = secondary_client
        self.workflows = workflows
        self.events = events
        self.packages = packages
        self.sources = sources

    def get_data(self):
        for job in self.jobs:
            Faker.seed(self.seed)
            self.data[job] = {}
            inner_data = self.data[job]
            inner_data['job_name'] = job
            inner_data['description'] = self.faker.paragraph(nb_sentences=2)
            inner_data['primary_client'] = self.client
            if job == 'Wedding':
                inner_data['workflow'] = self.workflows[0]
                inner_data['event'] = self.events[0]
                inner_data['package'] = self.packages[0]
            else:
                inner_data['workflow'] = self.workflows[1]
                inner_data['event'] = self.events[random.randint(1, 4)]
                inner_data['package'] = self.packages[random.randint(1, 4)]
            inner_data['venue'] = self.faker.street_address()
            inner_data['venue_notes'] = self.faker.paragraph(nb_sentences=2)
            start_date = self.faker.date_between(
                start_date=date.today(),
                end_date=date.today()) + timedelta(days=30)
            end_date = start_date + timedelta(days=random.randint(0, 30))
            inner_data['start_date'] = start_date
            inner_data['end_date'] = end_date
            all_day = True if self.seed % 2 == 0 else False
            inner_data['all_day'] = all_day
            #  if not all_day:
            #  date_time = self.faker.date_time()
            #  inner_data['start_time'] = date_time.time()
            #  end_time = date_time + timedelta(hours=random.randint(0, 8))
            #  inner_data['end_time'] = end_time
            #  else:
            #  inner_data['start_time'] = None
            #  inner_data['end_time'] = None
            inner_data['note'] = self.faker.paragraph(nb_sentences=2)
            inner_data['secondary_client'] = self.secondary_client
            inner_data['source'] = self.sources[random.randint(0, 4)]
            self.seed += 1
        return None

    def create_and_get_objs(self):
        self.get_data()
        for key in self.data:
            data = self.data[key]
            jobForm = JobReqCreateForm(data=data, userObj=self.user)
            job_obj = jobForm.save()
            self.job_objs.append(job_obj)
        return self.data, self.job_objs


class EventFixtureSetup:

    def __init__(self, user):
        self.faker = Faker()
        self.data = {}
        self.seed = 0
        self.events = [
            'Wedding', 'Birthday', 'Pre-Shoot', 'Portrait', 'Outdoor'
        ]
        self.event_objs = []
        self.user = user

    def get_data(self):
        for event in self.events:
            Faker.seed(self.seed)
            self.data[event] = {}
            inner_data = self.data[event]
            inner_data['event_name'] = event
            inner_data['description'] = self.faker.paragraph(nb_sentences=3)
            self.seed += 1
        return None

    def create_and_get_objs(self):
        self.get_data()
        for key in self.data:
            data = self.data[key]
            eventForm = EventForm(data=data,
                                  userObj=self.user,
                                  operation='creating')
            event_obj = eventForm.save()
            self.event_objs.append(event_obj)
        return self.data, self.event_objs


class ProductFixtureSetup:

    def __init__(self, user):
        self.faker = Faker()
        self.data = {}
        self.seed = 0
        self.products = ['photo frame', 'short video', 'photo album']
        self.prod_objs = []
        self.user = user

    def get_data(self):
        for prod in self.products:
            Faker.seed(self.seed)
            self.data[prod] = {}
            inner_data = self.data[prod]
            inner_data['product_name'] = prod
            inner_data['unit_price'] = 5000 if prod == 'photo album' else 2000
            inner_data[
                'unit_measure_type'] = 'm' if prod == 'short video' else 'u'
            inner_data['product_type'] = 'vd' if prod == 'short vide' else 'ph'
            inner_data['description'] = self.faker.paragraph(nb_sentences=3)
            inner_data['display'] = True
            inner_data['is_active'] = True
        return None

    def create_and_get_objs(self):
        self.get_data()
        for key in self.data:
            data = self.data[key]
            prodForm = ProductForm(data=data,
                                   userObj=self.user,
                                   operation='creating')
            prod_obj = prodForm.save()
            self.prod_objs.append(prod_obj)
        return self.data, self.prod_objs


class PackageFixtureSetup:

    def __init__(self, events, user, products):
        self.faker = Faker()
        self.data = {}
        self.seed = 0
        self.prod_objs = products
        self.packages = [
            'early-bird wedding', 'December kids', 'September portraits',
            'Nuwara outdoor', 'Sampath bank customers'
        ]
        self.package_objs = []
        self.user = user
        self.events = events

    def get_data(self):
        for package in self.packages:
            Faker.seed(self.seed)
            self.data[package] = {}
            inner_data = self.data[package]
            inner_data['package_name'] = package
            inner_data['description'] = self.faker.paragraph(nb_sentences=2)
            if package == 'early-bird wedding':
                inner_data['event'] = self.events[0]
            elif package == 'December kids':
                inner_data['event'] = self.events[1]
            elif package == 'September portraits':
                inner_data['event'] = self.events[3]
            elif package == 'Nuwara outdoor':
                inner_data['event'] = self.events[4]
            else:
                inner_data['event'] = self.events[2]
            inner_data['is_active'] = [True, False][random.randint(0, 1)]
            self.seed += 1
        return None

    def create_and_get_objs(self):
        self.get_data()
        for key in self.data:
            data = self.data[key]
            packageForm = PackageForm(data=data,
                                      userObj=self.user,
                                      operation='creating')
            package_obj = packageForm.save()
            # adding products to package
            products = self.prod_objs[0:random.randint(1, 3)]
            for prod in products:
                form = PackageLinkProductAddForm(data={
                    'product': prod,
                    'units': random.randint(1, 5)
                })
                if form.is_valid():
                    obj, package = form.save(package=package_obj,
                                             operation='creating',
                                             userObj=self.user)
            self.package_objs.append(package)
        return self.data, self.package_objs


class WorkTypeFixtureSetup:

    def __init__(self):
        self.faker = Faker()
        self.data = {}
        self.seed = 0
        self.workType_objs = []

    def get_data(self):
        Faker.seed(self.seed)
        self.data = {
            'Job request': {
                'work_type': 'Job request',
                'work_order': 1,
                'description': self.faker.paragraph(nb_sentences=2)
            },
            'Contract booking': {
                'work_type': 'Contract booking',
                'work_order': 2,
                'description': self.faker.paragraph(nb_sentences=2)
            },
            'Job confirmation': {
                'work_type': 'Job confirmation',
                'work_order': 3,
                'description': self.faker.paragraph(nb_sentences=2)
            },
            'Pre shoot': {
                'work_type': 'Pre shoot',
                'work_order': 4,
                'description': self.faker.paragraph(nb_sentences=2)
            },
            'Main shoot': {
                'work_type': 'Main shoot',
                'work_order': 5,
                'description': self.faker.paragraph(nb_sentences=2)
            },
            'Post shoot': {
                'work_type': 'Post shoot',
                'work_order': 6,
                'description': self.faker.paragraph(nb_sentences=2)
            },
            'Job done': {
                'work_type': 'Job done',
                'work_order': 7,
                'description': self.faker.paragraph(nb_sentences=2)
            }
        }
        return None

    def create_and_get_objs(self):
        self.get_data()
        for key in self.data:
            data = self.data[key]
            workTypeForm = WorkTypeForm(data=data)
            wt_obj = workTypeForm.save()
            self.workType_objs.append(wt_obj)
        return self.data, self.workType_objs


class WorkflowFixtureSetup:

    def __init__(self, user):
        self.faker = Faker()
        self.data = {}
        self.seed = 0
        self.workflows = ['simple wedding', 'simple photography']
        self.workflow_objs = []
        self.user = user

    def get_data(self):
        for wf in self.workflows:
            Faker.seed(self.seed)
            self.data[wf] = {}
            inner_data = self.data[wf]
            inner_data['workflow_name'] = wf
            inner_data['status'] = True
            inner_data['description'] = self.faker.paragraph(nb_sentences=3)
            self.seed += 1
        return None

    def create_and_get_objs(self):
        self.get_data()
        for key in self.data:
            data = self.data[key]
            workflowForm = WorkflowForm(data=data,
                                        userObj=self.user,
                                        operation='creation')
            wf_obj = workflowForm.save()
            self.workflow_objs.append(wf_obj)
        return self.data, self.workflow_objs


class WorkTemplateFixturesSetup:

    def __init__(self, workflow_objs, emailTemp_objs, workType_objs,
                 contTemp_objs, questTemp_objs):
        self.faker = Faker()
        self.data = {}
        self.seed = 0
        self.workTemplates = ['simple wedding']
        self.workTemplate_objs = []
        self.workflow_objs = workflow_objs
        self.emailTemplate_objs = emailTemp_objs
        self.contTemplate_objs = contTemp_objs
        self.questTemplate_objs = questTemp_objs
        self.workType_objs = workType_objs

    def get_data(self):
        for temp in self.workTemplates:
            Faker.seed(self.seed)
            self.data[temp] = []
            inner_data = self.data[temp]
            emailTempObjs = [
                email_temp_obj for email_temp_obj in self.emailTemplate_objs
                if email_temp_obj.workflow.workflow_name in 'simple wedding'
            ]
            # worflow first record
            wf_one = {
                'work_type': self.workType_objs[0],
                'class_object': 'ToDoTask',
                'job_confirmation': False,
                'step_number': 1,
                'name': 'Job request created',
                'workflow': self.workflow_objs[0],
                'description': self.faker.paragraph(nb_sentences=3),
                'auto_complete': True,
                'day_delta': 3,
                'check_invoice': False,
                'email_template': '',
                'contract_template': '',
                'quest_template': ''
            }
            inner_data.append(wf_one)

            # workflow second record
            wf_two = {
                'work_type': self.workType_objs[0],
                'class_object': 'EmailTask',
                'job_confirmation': False,
                'step_number': 2,
                'name': 'Initial follow up to the request',
                'workflow': self.workflow_objs[0],
                'description': self.faker.paragraph(nb_sentences=3),
                'auto_complete': False,
                'day_delta': 3,
                'check_invoice': False,
                'email_template': emailTempObjs[0],
                'contract_template': '',
                'quest_template': ''
            }
            inner_data.append(wf_two)

            # workflow third record
            wf_three = {
                'work_type': self.workType_objs[1],
                'class_object': 'EmailTask',
                'job_confirmation': False,
                'step_number': 3,
                'name': 'Second follow up to the request',
                'workflow': self.workflow_objs[0],
                'description': self.faker.paragraph(nb_sentences=3),
                'auto_complete': False,
                'day_delta': 5,
                'check_invoice': False,
                'email_template': emailTempObjs[1],
                'contract_template': '',
                'quest_template': ''
            }
            inner_data.append(wf_three)

            # workflow third record
            wf_four = {
                'work_type': self.workType_objs[1],
                'class_object': 'ContractTask',
                'job_confirmation': False,
                'step_number': 4,
                'name': 'Sharing the advance booking details and contract',
                'workflow': self.workflow_objs[0],
                'description': self.faker.paragraph(nb_sentences=3),
                'auto_complete': False,
                'day_delta': 5,
                'check_invoice': False,
                'email_template': '',
                'contract_template': self.contTemplate_objs[0],
                'quest_template': ''
            }
            inner_data.append(wf_four)

            # workflow third record
            wf_five = {
                'work_type': self.workType_objs[1],
                'class_object': 'AppointmentTask',
                'job_confirmation': False,
                'step_number': 5,
                'name': 'Job accepted',
                'workflow': self.workflow_objs[0],
                'description': self.faker.paragraph(nb_sentences=3),
                'auto_complete': False,
                'day_delta': 5,
                'check_invoice': False,
                'email_template': emailTempObjs[2],
                'contract_template': '',
                'quest_template': ''
            }
            inner_data.append(wf_five)

            # workflow third record
            wf_six = {
                'work_type': self.workType_objs[1],
                'class_object': 'QuestTask',
                'job_confirmation': False,
                'step_number': 6,
                'name': 'Get to know the customer',
                'workflow': self.workflow_objs[0],
                'description': self.faker.paragraph(nb_sentences=3),
                'auto_complete': False,
                'day_delta': 5,
                'check_invoice': False,
                'email_template': '',
                'contract_template': '',
                'quest_template': self.questTemplate_objs[0]
            }
            inner_data.append(wf_six)

            self.seed += 1
        return None

    def create_and_get_objs(self):
        self.get_data()
        for key in self.data:
            for item in self.data[key]:
                workTempForm = WorkTemplateForm(data=item)
                work_temp_obj = workTempForm.save()
                self.workTemplate_objs.append(work_temp_obj)
        return self.data, self.workTemplate_objs


class EmailTemplateFixtureSetup:

    def __init__(self, workflow_objs, user):
        # self.faker = Faker()
        self.data = {}
        # self.seed = 0
        self.templates = ['wedding email template']
        self.template_objs = []
        self.workflow_objs = workflow_objs
        self.user = user

    def get_data(self):
        for temp in self.templates:
            self.data[temp] = []
            inner_data = self.data[temp]
            inner_data.append({
                'workflow': self.workflow_objs[0],
                'template_name': 'Initial follow up email',
                'subject': 'Follow up email - company',
                'body': 'Hi customer, \n\n email is from company',
                'thank_you': 'Best regards'
            })
            inner_data.append({
                'workflow': self.workflow_objs[0],
                'template_name': 'Second follow up email',
                'subject': 'Second follow up email - company',
                'body': 'Hi customer, \n\n email is from company',
                'thank_you': 'Best regards'
            })
            inner_data.append({
                'workflow': self.workflow_objs[0],
                'template_name': 'Thank you for booking',
                'subject': 'Thank you email - company',
                'body': 'Hi customer, \n\n email is from company',
                'thank_you': 'Best regards'
            })
        return None

    def create_and_get_objs(self):
        self.get_data()
        for key in self.data:
            for item in self.data[key]:
                emailTempForm = EmailTemplateForm(data=item,
                                                  userObj=self.user,
                                                  operation='creating')
                email_temp_obj = emailTempForm.save()
                self.template_objs.append(email_temp_obj)
        return self.data, self.template_objs


class ContractTemplateFixtureSetup:

    def __init__(self, user):
        # self.faker = Faker()
        self.data = {}
        self.user = user
        self.template_objs = []
        # self.seed = 0

    def get_data(self):
        self.data['template_name'] = 'Sample Commercial Contract'
        self.data['subject'] = 'Commercial Contract'
        self.data['body'] = """
                            Short-Form General Photography Contract
                            This agreement is between {company} (hereafter “Photographer” “the Photographer” or
                            “Photography Company”) and {customer} (hereafter referred to as “CLIENT”).
                        """
        self.data['thank_you'] = 'thank you and regards'
        self.data['signature'] = 'company'

        return None

    def create_and_get_objs(self):
        self.get_data()
        contractTempForm = ContractTemplateForm(data=self.data,
                                                userObj=self.user,
                                                operation='creating')
        contract_temp_obj = contractTempForm.save()
        self.template_objs.append(contract_temp_obj)
        return self.data, self.template_objs


class QuestionnaireTemplateFixtureSetup:

    def __init__(self, user):
        # self.faker = Faker()
        self.data = {}
        self.user = user
        self.template_objs = []
        # self.seed = 0

    def get_data(self):
        self.data['template_name'] = 'Simple Wedding Questionnaire'
        self.data['subject'] = 'Simple Wedding Questionnaire'
        self.data['body'] = "Please get back to us"
        self.data['thank_you'] = 'thank you and regards'
        self.data['signature'] = 'company'
        self.data[
            'question_one'] = 'What is the address of where couple will be getting ready?'
        self.data[
            'question_two'] = 'Please confirm exact details of the ceremony?'
        self.data['question_three'] = 'Will there be first dance?'
        self.data['question_four'] = 'Will there be formal speeches?'
        self.data['question_five'] = 'Will there be a toss?'

        return None

    def create_and_get_objs(self):
        self.get_data()
        questTempForm = QuestionnaireTemplateForm(data=self.data,
                                                  userObj=self.user,
                                                  operation='creating')
        quest_temp_obj = questTempForm.save()
        self.template_objs.append(quest_temp_obj)
        return self.data, self.template_objs


class SourceFixtureSetup:

    def __init__(self):
        self.faker = Faker()
        self.data = {}
        self.seed = 0
        self.sources = ['web', 'facebook', 'instagram', 'friend', 'twitter']
        self.source_objs = []

    def get_data(self):
        """
        creating source data
        """
        for source in self.sources:
            Faker.seed(self.seed)
            self.data[source] = {}
            inner_data = self.data[source]
            inner_data['source'] = source
            inner_data['description'] = self.faker.paragraph(nb_sentences=3)
            self.seed += 1
        return None

    def create_and_get_objs(self):
        self.get_data()
        for key in self.data:
            key_data = self.data[key]
            sourceForm = SourceForm(data=key_data)
            source_obj = sourceForm.save()
            self.source_objs.append(source_obj)
        return self.data, self.source_objs
