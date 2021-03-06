from finance.models import Invoice
from decimal import Decimal


def register_invoice_data_for_job(job, package=False):
    """
    when the job is created or when the instance is saved,
    invoice data will be updated with the correct information
    """
    if package:
        package_description = job.package.description
        package_price = job.package.price
    else:
        package_description = "none"
        package_price = 0

    if job.invoice is None:
        invoice = Invoice.objects.create(description=package_description,
                                         price=package_price,
                                         discount=0,
                                         total_price=package_price - 0)
    else:
        invoice = job.invoice
        invoice.description = package_description
        invoice.description = package_description
        invoice.price = Decimal(package_price)
        invoice.discount = invoice.discount if invoice.discount else Decimal(0)
        discounted_amount = invoice.price * invoice.discount
        invoice.total_price = invoice.price - Decimal(discounted_amount)
        invoice.save()
    job.invoice = invoice
    job.save()


def prepare_invoice_sharing(job):
    """preparing invoice summary to share"""
    if not job.package:
        raise Exception('Please select the package before generating invoice')
    products = job.package.products.all()
    invoice = job.invoice
    product_info = ""
    for product in products:

        product_info += f"""
                |------------------------------------------------------------------
                |_Product - {product.product_name}
                |_price - {product.unit_price}
                |_Description - {product.description}
                |------------------------------------------------------------------
                """

    invoice_summary = f"""


    |
    |  I N V O I C E   S U M M A R Y
    |
    |------------------------------------------------------------------
    |   Issue date - {invoice.issue_date}
    |   Issue number - {invoice.get_issue_number()}
    |   Job - {invoice.job}
    |   Package - {invoice.job.package}
    |
    |------------------------------------------------------------------
    |   PRODUCTS
    |------------------------------------------------------------------
    |
    """ + product_info
    invoice_summary += f"""
    |......................................................
    |......................................................
    |Subtotal                       {invoice.price}
    |......................................................
    |Discount                       {invoice.discount}
    |......................................................
    |Total                          {invoice.total_price}
    |......................................................
    """
    invoice.description = invoice_summary
    invoice.save()
    return invoice_summary
