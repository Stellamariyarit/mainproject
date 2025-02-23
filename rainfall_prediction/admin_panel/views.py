# from django.shortcuts import render

# def admin_dashboard(request):
#     return render(request, 'admin_panel/admin_dashboard.html')



from django.shortcuts import render

def admin_dashboard(request):
    # Sample alert statistics
    alert_stats = {
        "Red": 5,
        "Orange": 10,
        "Yellow": 15,
        "Green": 20,
    }
    return render(request, 'admin_panel/admin_dashboard.html', {
        'alert_stats': alert_stats
    })
