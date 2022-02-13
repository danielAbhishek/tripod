def add_basic_html_tags(main_component, fields, description=False):
    for field in fields:
        fields[str(field)].widget.attrs.update(
            {
                "placeholder": f"{main_component}-str(field)",
                "class": "form-control"
            }
        )
    if description:
        fields['description'].widget.attrs.update({'rows': '2'})
