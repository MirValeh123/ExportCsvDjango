from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import csv
User=get_user_model()

# Create your views here.

def index(request):
    users = get_user_model().objects.all()
    user_model_meta = get_user_model()._meta
    excluded_field_names = ['logentry', 'id', 'password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions']
    column_names = [field.name for field in user_model_meta.get_fields() if field.name not in excluded_field_names]

    selected_columns = request.GET.getlist('selected_columns')  # Get the selected columns as a list

    # Filter the queryset based on the selected columns
    filtered_users = users.values(*selected_columns)

    # Convert the queryset to a list of dictionaries
    filtered_users = list(filtered_users)

    context = {
        'users': users,
        'column_names': column_names,
        'selected_columns': selected_columns,
        'filtered_users': filtered_users,
    }
    if 'export_csv' in request.GET:  # Check if the export CSV button is clicked
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="filtered_users.csv"'

        # Create a CSV writer
        writer = csv.writer(response)

        # Write the header row
        writer.writerow(selected_columns)

        # Write the data rows
        for user in filtered_users:
            writer.writerow([user[column] for column in selected_columns])

        return response

    return render(request, 'test.html', context)
