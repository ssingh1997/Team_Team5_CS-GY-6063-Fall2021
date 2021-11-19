from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import FoodAvailForm, TimeSlotForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# from django.views.generic import CreateView, UpdateView

# from django.views.generic.base import View
from django.contrib import messages

# Create your views here.


def check_existing_post(request):
    data = request.POST.copy()
    data["author"] = request.user
    if len(FoodAvail.objects.filter(author=request.user)) > 0:
        return True
    else:
        return False


@login_required
def post_available_food(request):
    if not check_existing_post(request):
        instance = FoodAvail()
        data = request.POST.copy()
        data["author"] = request.user
        form = FoodAvailForm(data or None, instance=instance)
        if request.POST and form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("food_avail:view_food_avail_res"))
    else:
        instance = get_object_or_404(FoodAvail, author=request.user)
        form = FoodAvailForm(request.POST, request.FILES, instance=instance)
        if request.method == "POST":
            form = FoodAvailForm(request.POST or None, instance=instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("food_avail:view_food_avail_res"))
        else:
            form = FoodAvailForm(instance=instance)
    return render(request, "food_avail/post_food_avail.html", {"food": form})


@login_required
def view_available_food(request):
    context = {}
    instance = FoodAvail.objects.get(author=request.user)
    context["food"] = instance
    if request.method == "POST":
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        print("PRINT START TIME: ", start_time)
        print("PRINT END TIME: ", end_time)

        # if not check_existing_timeslot(request):
        print("Time slot does not exist")
        print("DATA")
        time_slot = TimeSlot()
        data = request.POST.copy()
        print(time_slot)
        data["time_slot_owner"] = request.user
        time_slot_owner = request.POST.get("time_slot_owner")
        print("PRINT CREATOR: ", time_slot_owner)
        print(
            TimeSlot.objects.filter(
                time_slot_owner=request.user, start_time=start_time, end_time=end_time
            )
        )
        if (
            len(
                TimeSlot.objects.filter(
                    time_slot_owner=request.user,
                    start_time=start_time,
                    end_time=end_time,
                )
            )
            == 0
        ):
            # data["food_avail_id"] = FoodAvail.objects.get(author=request.user).pk
            form = TimeSlotForm(data or None, instance=time_slot)
            if form.is_valid():
                form.save()
                print("its working")
                context["time_slot"] = form
            else:
                messages.info(request, "Start time cannot be after end time!")
        else:
            print("it already exists")
            messages.info(request, "Time Slot Already Exists")

    time_slots_all = TimeSlot.objects.filter(time_slot_owner=request.user)
    context["time_slots_all"] = time_slots_all
    return render(request, "food_avail/view_food.html", context)

def update_time_slot(request, pk):
    instance = get_object_or_404(TimeSlot, pk=pk)
    form = TimeSlotForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("food_avail:view_food_avail_res"))
    else:
        print("not working")
        messages.info(request, "Start time cannot be after end time!")
    return render(request, "food_avail/update_time_slot.html", {"timeslot": form})

def delete_time_slot(request, pk):
    timeslot = get_object_or_404(TimeSlot, pk=pk)
    if request.method == "POST":
        timeslot.delete()
        # return HttpResponseRedirect(reverse("food_avail:view_food_avail_res"))
    return HttpResponseRedirect(reverse("food_avail:view_food_avail_res"))
    # return render(request, "food_avail/delete_time_slot.html", {"timeslot": timeslot})

def check_food_availibility(request):
    food = FoodAvail.objects.all()
    return render(request, "food_avail/view_food_avail.html", {"food": food})

