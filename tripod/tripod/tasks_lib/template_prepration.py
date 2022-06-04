"""
TemplateDatabaseObjects is a class that init relavent database objects, such
like user and company, so the template fields and access the database values
using the class function.
"""

import re


class TemplateDatabaseObjects:

    def __init__(self, company, task, template_objects):
        """
        This class represents the initiation/ copy of the database objects
        that needed for them Template class to preare the content
        * user object
        * company object
        * template_objects -> collection of template field objects
        * db_template_fields -> [field in TemplateField]
        * replace_dict -> {'field': 'object_field'} from TemplateField
        """
        self.company = company
        self.task = task
        self.appointment = task.appointment if task.appointment else None
        self.job = self.task.get_job()
        self.user = self.job.primary_client
        self.db_template_fields = []
        self.replace_dict = {}
        self.template_objects = template_objects

    def set_db_template_fields(self):
        """
        This will get the exact model name and column in the format of model.column
        for the template name in template objects query
        """
        values = self.template_objects.values()
        # print(values)
        result = [value['field'] for value in values]
        # print(result)
        self.db_template_fields = result
        return None

    def set_db_data_for_field(self, field):
        """
        Once the exact model.column has been taken, using eval method the database value will
        be taken and added to te replace_dict
        """
        temp_obj = self.template_objects.get(field=field)
        self.replace_dict[temp_obj.field] = eval("self." +
                                                 temp_obj.object_field)
        return None


class TemplateContent:
    """
    This class represents the creation of the content using the copy
    of the already existing template, by taking template_fields in the content
    and replacing with appropriate db values (using TemplateDatabaseObjects)
    * template -> template object (email or contract)
    * subject/ thank_you/ signature -> True of False
    * pattern -> regex pattern to find '{text}'
    * template_fields -> collection of template field in the content
    """

    def __init__(self, template):
        self._pattern = r"{([A-Za-z]+)}"
        self.template = template
        self.template_fields = []

    def get_template_fields(self):
        """
        From the template body (can be email body or contract body) using regex pattern
        words with this patter -> "{example}" will be taken and added to template_fields
        """
        # adding template fields from body
        self.template_fields = re.findall(self._pattern, self.template.body)

        # adding template fields from subject
        subject = re.findall(self._pattern, self.template.subject)
        self.template_fields = self.template_fields + subject

        self.template_fields = list(set(self.template_fields))

    def prepare_content(self, database_objects):
        """
        Replacing dictionary will be created by taking model.column combination field and word
        from template body with "{}" the pattern
        """
        database_objects.set_db_template_fields()
        db_template_fields = database_objects.db_template_fields
        self.get_template_fields()

        for field in self.template_fields:
            if field not in db_template_fields:
                raise Exception(f'Passes field ({field}) not valid')
            database_objects.set_db_data_for_field(field)

        self.template = self.replace_data(database_objects.replace_dict)
        return self.template

    def replace_data(self, replace_dict):
        """passing replace_dict replace template fields with db values"""
        try:
            self.template.body = self.template.body.format(**replace_dict)
            self.template.subject = self.template.subject.format(
                **replace_dict)
            # if self.thank_you:
            #     pass
            # if self.signature:
            #     pass
        except KeyError:
            raise Excpetion('Replace Dictionary missing keys')
        return self.template
