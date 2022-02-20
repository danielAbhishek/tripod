"""
This test cases is created to test the automation of the workflow
creation once the job is initiated
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from job.models import Work, Task

from job.tests.fixtures import (
    JobFixtureSetup, EventFixtureSetup, PackageFixtureSetup,
    WorkflowFixtureSetup, WorkTemplateFixturesSetup,
    EmailTemplateFixtureSetup, SourceFixtureSetup
)


class WorkFlowTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test_user@mail.com',
            'abcd@1234'
        )
        self.client = get_user_model().objects.create_user(
            'test_client@mail.com',
            'abcd@123'
        )
        self.secondary_client = get_user_model().objects.create_user(
            'test_secondClient@mail.com',
            'abcd@123'
        )

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
            self.workflow_objs, self.user
            )
        (self.emailTemp_data,
            self.emailTemp_objs) = self.emailTempFixture.create_and_get_objs()

        # work template
        self.workTempFixture = WorkTemplateFixturesSetup(
            self.workflow_objs, self.emailTemp_objs)
        (self.workTemp_data,
            self.workTemp_objs) = self.workTempFixture.create_and_get_objs()

        # package
        self.eventFixture = EventFixtureSetup(self.user)
        (self.event_data,
            self.event_objs) = self.eventFixture.create_and_get_objs()

        # package
        self.packageFixture = PackageFixtureSetup(self.event_objs, self.user)
        (self.package_data,
            self.package_objs) = self.packageFixture.create_and_get_objs()

        # job
        self.jobFixture = JobFixtureSetup(
            self.user, self.client, self.secondary_client,
            self.workflow_objs, self.event_objs, self.package_objs,
            self.source_objs
        )
        (self.job_data,
            self.job_objs) = self.jobFixture.create_and_get_objs()

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
        """
        # since it is added to list need to count it separetly
        emailTemplate_data = [
            len(self.emailTemp_data[i])
            for i in self.emailTemp_data]
        self.assertEqual(
            sum(emailTemplate_data),
            len(self.emailTemp_objs))

    def test_workTemp_objects_added(self):
        """
        testing the workTemp number of the data equals the number of db objects
        created
        """
        # since it is added to list need to count it separetly
        workTemplate_data = [
            len(self.workTemp_data[i])
            for i in self.workTemp_data]
        self.assertEqual(
            sum(workTemplate_data),
            len(self.workTemp_objs))

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

    def test_job_workflow_automation_not_created_for_photography(self):
        """
        testing the job workflow automation created for photography
        since the work template is only available for wedding
        """
        jobs, works = self.get_works_workflow('birthday')
        self.assertEqual(len(works), 0)

    def test_job_workflow_automation_created_for_wedding(self):
        """
        testing that works db objects were created as a part of workflow
        automation, for jobs with wedding workflow
        """
        jobs, works = self.get_works_workflow('simple wedding')
        self.assertEqual(len(works), jobs*3)

    def test_tasks_created_for_the_work(self):
        """
        testing that tasks relavent to work have been created
        """
        jobs, works = self.get_works_workflow('simple wedding')
        task_count = 0
        for work in works:
            tasks = Task.objects.filter(work=work)
            task_count += len(tasks)
        self.assertEqual(task_count, 5)
