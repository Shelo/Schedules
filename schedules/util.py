from strings.weekdays import *

def number_to_day(number):
    if 0 <= number <= len(DAYS_OF_THE_WEEK):
        return DAYS_OF_THE_WEEK[number]

    return False


def user_is_member(request, project, membership_model):
    submitter = request.user
    return membership_model.objects.filter(user=submitter, project=project).exists()
