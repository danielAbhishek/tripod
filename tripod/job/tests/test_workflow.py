"""
This test cases is created to test the automation of the workflow
creation once the job is initiated
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from job.models import Work, Task, Job
from company.models import PackageLinkProduct

from job.forms import JobUpdateConfirmForm
from job.tests.fixtures import (
    JobFixtureSetup, EventFixtureSetup, ProductFixtureSetup,
    PackageFixtureSetup, WorkflowFixtureSetup, WorkTemplateFixturesSetup,
    EmailTemplateFixtureSetup, SourceFixtureSetup, WorkTypeFixtureSetup,
    QuestionnaireTemplateFixtureSetup, ContractTemplateFixtureSetup)

from job.workflow_factory.workflow import WorkFlowBase

from finance.forms import PaymentHistoryForm
from finance.utils import register_invoice_data_for_job


class WorkFlowTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test_user@mail.com', 'abcd@1234')
        self.client = get_user_model().objects.create_user(
            'test_client@mail.com', 'abcd@123')
        self.secondary_client = get_user_model().objects.create_user(
            'test_secondClient@mail.com', 'abcd@123')

        # source
        self.sourceFixture = SourceFixtureSetup()
        (self.source_data,
         self.source_objs) = self.sourceFixture.create_and_get_objs()

        # workflow
        self.workflowFixture = WorkflowFixtureSetup(self.user)
        (self.workflow_data,
         self.workflow_objs) = self.workflowFixture.create_and_get_objs()

        # email template
        self.emailTempFixture = EmailTemplateFixtureSetup(
            self.workflow_objs, self.user)
        (self.emailTemp_data,
         self.emailTemp_objs) = self.emailTempFixture.create_and_get_objs()

        # Contract template
        self.contractTempFixture = ContractTemplateFixtureSetup(self.user)
        (self.contTemp_data,
         self.contTemp_objs) = self.contractTempFixture.create_and_get_objs()

        # Questionnaire template
        self.questTempFixture = QuestionnaireTemplateFixtureSetup(self.user)
        (self.questTemp_data,
         self.questTemp_objs) = self.questTempFixture.create_and_get_objs()

        # work type
        self.workTypeFixture = WorkTypeFixtureSetup()
        (self.workType_data,
         self.workType_objs) = self.workTypeFixture.create_and_get_objs()

        # work template
        self.workTempFixture = WorkTemplateFixturesSetup(
            self.workflow_objs, self.emailTemp_objs, self.workType_objs,
            self.contTemp_objs, self.questTemp_objs)
        (self.workTemp_data,
         self.workTemp_objs) = self.workTempFixture.create_and_get_objs()

        # event
        self.eventFixture = EventFixtureSetup(self.user)
        (self.event_data,
         self.event_objs) = self.eventFixture.create_and_get_objs()

        # product
        self.productFixture = ProductFixtureSetup(self.user)
        (self.prod_data,
         self.prod_objs) = self.productFixture.create_and_get_objs()

        # package
        self.packageFixture = PackageFixtureSetup(self.event_objs, self.user,
                                                  self.prod_objs)
        (self.package_data,
         self.package_objs) = self.packageFixture.create_and_get_objs()

        # job
        self.jobFixture = JobFixtureSetup(self.user, self.client,
                                          self.secondary_client,
                                          self.workflow_objs, self.event_objs,
                                          self.package_objs, self.source_objs)
        (self.job_data, self.job_objs) = self.jobFixture.create_and_get_objs()

    def test_sourcesObjects_added(self):
        """
        testing the source number of the data equals the number of db objects
        created
        """
        self.assertEqual(len(self.source_data), len(self.source_objs))

    def test_workflow_objects_added(self):
        """
        testing the workflow number of the data equals the number of db objects
        created
        """
        self.assertEqual(len(self.workflow_data), len(self.workflow_objs))

    def test_emailtemplate_objects_added(self):
        """
        testing the workflow number of the data equals the number of db objects
        created
        since it is added to list need to count it separetly
        """
        emailTemplate_data = [
            len(self.emailTemp_data[i]) for i in self.emailTemp_data
        ]
        self.assertEqual(sum(emailTemplate_data), len(self.emailTemp_objs))

    def test_workTemp_objects_added(self):
        """
        testing the workTemp number of the data equals the number of db objects
        created
        since it is added to list need to count it separetly
        """
        workTemplate_data = [
            len(self.workTemp_data[i]) for i in self.workTemp_data
        ]
        self.assertEqual(sum(workTemplate_data), len(self.workTemp_objs))

    def test_event_objects_added(self):
        """
        testing the event number of the data equals the number of db objects
        created
        """
        self.assertEqual(len(self.event_data), len(self.event_objs))

    def test_package_objects_added(self):
        """
        testing the package number of the data equals the number of db objects
        created
        """
        self.assertEqual(len(self.package_data), len(self.package_objs))

    def test_job_objects_added(self):
        """
        testing the job number of the data equals the number of db objects
        created
        """
        self.assertEqual(len(self.job_data), len(self.job_objs))

    def get_works_workflow(self, workflow_name):
        jobs = 0
        for job in self.job_objs:
            if job.workflow.workflow_name == workflow_name:
                works = Work.objects.filter(job=job)
                jobs += 1
                return jobs, works
            else:
                return 0, []

    def test_job_workflow_automation_not_created_for_birthday_photography(
            self):
        """
        testing the job workflow automation created for birthday photography
        since the work template is only available for wedding
        """
        jobs, works = self.get_works_workflow('birthday')
        self.assertEqual(len(works), 0)

    def confirming_job(self, job):
        """using JobUpdateConfirmForm to confirm the job"""
        job_data = job.__dict__
        job_data['primary_client'] = self.client
        job_data['workflow'] = job.workflow
        form = JobUpdateConfirmForm(instance=job,
                                    data=job_data,
                                    userObj=self.client,
                                    operation='confirming Job')
        if form.is_valid():
            form.save()

        return job

    def birthday_job_confirm(self):
        """returning confirmed birthday job"""
        birthday_job = [
            job for job in self.job_objs if job.job_name == 'pre-shoot'
        ][0]
        job = self.confirming_job(birthday_job)

        return job

    def wedding_job_confirm(self):
        """returning confirmed wedding job"""
        wedding_job = [
            job for job in self.job_objs if job.job_name == 'Wedding'
        ][0]
        job = self.confirming_job(wedding_job)

        return job

    def test_confirming_job(self):
        """
        Confirmed job status should be changed from req to job
        """
        job = self.birthday_job_confirm()

        self.assertEqual(job.status, 'job')

    def test_confiemd_job_task_auto_complete(self):
        """while confirming job task can be auto completed
        by providing True value to auto_complete field in the table"""
        job = self.wedding_job_confirm()
        work = job.work_set.filter(work_name='Job request').last()
        jrc_task = work.task_set.filter(task_name='Job request created').last()

        self.assertTrue(jrc_task.completed)

    def test_exception_raised_for_confirming_without_workflow(self):
        """trying to confirm a job without a workflow will raise an error"""
        wedding_job = [
            job for job in self.job_objs if job.job_name == 'Wedding'
        ][0]
        wedding_job.workflow = None
        wedding_job.save()

        with self.assertRaises(Exception):
            self.wedding_job_confirm()

    def test_invoice_not_created_if_package_is_not_available(self):
        """when confirming a job, if the package is not available then invoice should be 0"""
        wedding_job = [
            job for job in self.job_objs if job.job_name == 'Wedding'
        ][0]
        wedding_job.package = None
        wedding_job.save()

        job = self.wedding_job_confirm()

        self.assertEqual(job.invoice.price, 0)

    def test_invoice_creation_after_confirming_job(self):
        """invoice should be created after the job is confirmed"""
        job = self.wedding_job_confirm()
        plp = PackageLinkProduct.objects.filter(package=job.package)
        package_amount = 0
        for item in plp:
            package_amount += item.units * item.product.unit_price

        self.assertEqual(job.invoice.price, package_amount)

    def test_works_created_for_wedding(self):
        """
        testing that works db objects were created as a part of workflow
        automation, for jobs with wedding workflow
        each job will have 7 works by default
        """
        job = self.wedding_job_confirm()
        works = job.work_set.all()

        self.assertEqual(len(works), 7)

    def test_tasks_created_for_the_work(self):
        """
        testing that tasks relavent to work have been created
        """
        job = self.wedding_job_confirm()
        works = job.work_set.all()

        task_count = 0
        for work in works:
            tasks = work.task_set.all()
            task_count += len(tasks)
        self.assertEqual(task_count, 6)

    def test_processing_already_completed_task(self):
        """Already completed task should raise exception as completed"""
        job = self.wedding_job_confirm()
        jr_work = job.work_set.filter(work_name='Job request').last()
        jrc_task = jr_work.task_set.filter(
            task_name='Job request created').last()

        with self.assertRaises(Exception):
            jrc_task.process_task(self.client)

    def test_processing_not_completed_simpletask(self):
        """
        processing a simple task, and expecting task completed to be 
        updated as True
        """
        job = self.wedding_job_confirm()
        jr_work = job.work_set.filter(work_name='Job request').last()
        jrc_task = jr_work.task_set.filter(
            task_name='Initial follow up to the request').last()

        jrc_task.process_task(self.client)

        self.assertTrue(jrc_task.completed)
