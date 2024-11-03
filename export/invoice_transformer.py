import base64
import xml.etree.ElementTree as ET


class RossumInvoiceTransformer:
    def __init__(self, xml_content: str):
        """
        Initialize the transformer with the original XML content.

        :param xml_content: Original XML content as a string.
        """
        self.root = ET.fromstring(xml_content)
        self.transformed_xml = None

    def transform(self):
        """
        Transforms the XML content to the new structure and encodes it as base64.

        :return: Base64-encoded transformed XML content as a string.
        """
        # Extract relevant data from the original XML content
        invoice_number = self.root.findtext(".//datapoint[@schema_id='document_id']")
        invoice_date = self.root.findtext(".//datapoint[@schema_id='date_issue']")
        due_date = self.root.findtext(".//datapoint[@schema_id='date_due']")
        iban = self.root.findtext(".//datapoint[@schema_id='iban']")
        currency = self.root.findtext(".//datapoint[@schema_id='currency']")
        vendor = self.root.findtext(".//datapoint[@schema_id='sender_name']")
        vendor_address = self.root.findtext(".//datapoint[@schema_id='sender_address']")
        total_amount = self.root.findtext(".//datapoint[@schema_id='amount_due']")
        amount_total_tax = self.root.findtext(".//datapoint[@schema_id='amount_total_tax']")

        # Create the new XML structure
        invoice_registers = ET.Element("InvoiceRegisters")
        invoices = ET.SubElement(invoice_registers, "Invoices")
        payable = ET.SubElement(invoices, "Payable")

        ET.SubElement(payable, "InvoiceNumber").text = invoice_number
        ET.SubElement(payable, "InvoiceDate").text = f"{invoice_date}T00:00:00" if invoice_date else ""
        ET.SubElement(payable, "DueDate").text = f"{due_date}T00:00:00" if due_date else ""
        ET.SubElement(payable, "TotalAmount").text = total_amount
        ET.SubElement(payable, "Notes").text = ""
        ET.SubElement(payable, "Iban").text = iban
        ET.SubElement(payable, "Amount").text = amount_total_tax
        ET.SubElement(payable, "Currency").text = currency.upper() if currency else ""
        ET.SubElement(payable, "Vendor").text = vendor
        ET.SubElement(payable, "VendorAddress").text = vendor_address

        # Add line items to the details section
        details = ET.SubElement(payable, "Details")
        for item in self.root.findall(".//tuple[@schema_id='line_item']"):
            detail = ET.SubElement(details, "Detail")
            ET.SubElement(detail, "Amount").text = item.findtext("datapoint[@schema_id='item_amount']")
            ET.SubElement(detail, "AccountId").text = ""
            ET.SubElement(detail, "Quantity").text = item.findtext("datapoint[@schema_id='item_quantity']")
            ET.SubElement(detail, "Notes").text = item.findtext("datapoint[@schema_id='item_description']")

        # Convert the new XML structure to a string
        self.transformed_xml = ET.tostring(invoice_registers, encoding="utf-8", xml_declaration=True)

        # Return the annotation ID and XML content
        return self.transformed_xml

    def transform_base64(self) -> str:
        """
        Provides the transformed XML content as a base64-encoded string.

        :return: Base64-encoded transformed XML content as a string.
        """
        output_xml = self.transform()
        return base64.b64encode(output_xml).decode("utf-8")
