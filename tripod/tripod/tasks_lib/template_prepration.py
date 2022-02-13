import re


class DatabaseObject:
    def __init__(self, user, company, template_objects):
        """
        This class represents the initiation/ copy of the database objects
        that needed for them Template class to preare the content
        * user object
        * company object
        * template_objects -> collection of template field objects
        * db_template_fields -> [field in TemplateField]
        * replace_dict -> {'field': 'object_field'} from TemplateField
        """
        self.user = user
        self.company = company
        self.db_template_fields = []
        self.replace_dict = {}
        self.template_objects = template_objects

    def set_db_template_fields(self):
        """
        Get the template fields that defined in the database table
        TemplateField and set it to the local variable
        """
        values = self.template_objects.values()
        result = [value['field'] for value in values]
        self.db_template_fields = result
        return None

    def set_db_data_for_field(self, field):
        """
        Get the object name for a particulat field/ row that passed, from
        the TemplateField table
        """
        temp_obj = self.template_objects.get(field=field)
        self.replace_dict[temp_obj.field] = eval("self."+temp_obj.object_field)
        return None


class EmailContent:
    """
    This class represents the creation of the content using the copy
    of the already existing template, by taking template_fields in the content
    and replacing with appropriate db values (using DatabaseObject)
    * template -> template object (email or contract)
    * subject/ thank_you/ signature -> True of False
    * pattern -> regex pattern to find '{text}'
    * template_fields -> collection of template field in the content
    """
    def __init__(self, template, subject, thank_you, signature):
        self._pattern = r"{([A-Za-z]+)}"
        self.template = template
        self.template_fields = []
        self.subject = subject
        self.thank_you = thank_you
        self.signature = signature

    def get_template_fields(self):
        """
        Taking tamplate fields from template body and setting
        the tempate_fields list
        """
        # adding template fields from body
        self.template_fields = re.findall(
            self._pattern, self.template.body)
        if self.subject:
            subject = re.findall(self._pattern, self.template.subject)
            self.template_fields = self.template_fields + subject
        if self.thank_you:
            pass
        if self.signature:
            pass

        self.template_fields = list(set(self.template_fields))

    def prepare_content(self, database_objects):
        """
        Looping thru the template_fields which taken using above function
        and with created replace_dict from DatabaseObject, replacing
        content of the body subject, thank you and signature
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
        self.template.body = self.template.body.format(
            **replace_dict)
        if self.subject:
            self.template.subject = self.template.subject.format(
                **replace_dict
            )
        if self.thank_you:
            pass
        if self.signature:
            pass
        return self.template
