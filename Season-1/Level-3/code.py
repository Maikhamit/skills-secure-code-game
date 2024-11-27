import os
from flask import Flask, request

### Unrelated to the exercise -- Starts here -- Please ignore
app = Flask(__name__)
@app.route("/")
def source():
    TaxPayer('foo', 'bar').get_tax_form_attachment(request.args["input"])
    TaxPayer('foo', 'bar').get_prof_picture(request.args["input"])
### Unrelated to the exercise -- Ends here -- Please ignore

class TaxPayer:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.prof_picture = None
        self.tax_form_attachment = None

    # Returns the path of an optional profile picture that users can set
    def get_prof_picture(self, path=None):
        # Setting a profile picture is optional
        if not path:
            return None

        # Defends against path traversal attacks
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.normpath(os.path.join(base_dir, path))

        # Ensure the path remains within the base directory
        if not full_path.startswith(base_dir):
            return None

        # Check if the file exists and is accessible
        if not os.path.isfile(full_path):
            return None

        with open(full_path, 'rb') as pic:
            picture = bytearray(pic.read())

        # Assume that the image is returned on screen after this
        return full_path

    # Returns the path of an attached tax form that every user should submit
    def get_tax_form_attachment(self, path=None):
    # Tax form submission is mandatory
        if not path:
            raise Exception("Error: Tax form is required for all users")

        # Defends against path traversal attacks
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.normpath(os.path.join(base_dir, path))

        # Ensure the path remains within the base directory
        if not full_path.startswith(base_dir):
            # Instead of raising an exception, return `None` for invalid paths
            return None

        # Check if the file exists and is accessible
        if not os.path.isfile(full_path):
            # Instead of raising an exception, return `None` for missing files
            return None

        with open(full_path, 'rb') as form:
            tax_data = bytearray(form.read())

        # Assume that tax data is returned on screen after this
        return full_path
