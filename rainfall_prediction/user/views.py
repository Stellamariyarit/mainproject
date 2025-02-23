# from django.shortcuts import render

# def user_dashboard(request):
#     return render(request, 'user/user_dashboard.html')


from django.shortcuts import render

def user_dashboard(request):
    # Sample data with Red Alert included
    alerts = [
        {"date": "2025-02-21", "status": "Red"},
        {"date": "2025-02-20", "status": "Green"},
        {"date": "2025-02-19", "status": "Yellow"},
        {"date": "2025-02-18", "status": "Orange"},
    ]
    latest_alert = alerts[0]
    return render(request, 'user/user_dashboard.html', {
        'latest_alert': latest_alert,
        'alerts': alerts
    })
