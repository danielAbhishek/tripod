from finance.models import Invoice


def register_invoice_data_for_job(job):
    """
    when the job is created or when the instance is saved,
    invoice data will be updated with the correct information
    """
    try:
        Invoice.objects.update_or_create(
            job=job,
            description=job.package.description,
            price=job.package.price,
            defaults={"job": job}
        )
    except Exception as e:
        pass


def prepare_invoice_sharing(invoice):
    """preparing invoice summary to share"""
    products = invoice.job.package.products.all()
    product_info = ""
    for product in products:
        product_info += f"""
            {product.product_name} - {product.unit_price}
            -- {product.description}
        """
    invoice_summary = f"""
        invoice_summary
        ---------------------------------------------
        ---------------------------------------------
        Issue date - {invoice.issue_date}
        Issue number - {invoice.get_issue_number}

        Job - {invoice.job}
        ---------------------------------------------
        selected package is {invoice.job.package}
        {invoice.job.package.description}
    """ + product_info
    invoice_summary += f"""
    ------------------------------------------------------
    Subtotal                                    {invoice.price}
    Subtotal                                    {invoice.discount}
    Subtotal                                    {invoice.total_price}
    """
    return invoice_summary
