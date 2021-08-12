import csv
from django.shortcuts import render, redirect, HttpResponse
from .models import Categorie, Item, Floor, Room, SubItem
from .forms import addCategoryForm, addItemForm, addExistingForm, allocateForm,addRoomForm,addFloorForm,categoryEditForm,editRoomForm,editItemForm,editCategoryForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import subItemForm
from datetime import datetime

# from django.db.models.signals import post_save
# from django.dispatch import receiver,Signal

# Create your views here.

@login_required
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!.LogIn again')
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'inventory/register.html', context)

# I understand this function, except for redirection part
@login_required
def add1(request):
    if request.method == 'POST':
        category = request.POST['categorySelect']
        c = Categorie.objects.get(category_name = category)
        # problem lies here
        return redirect('add2',c.pk)
    context = {'categoryObj': Categorie.objects.all()}
    return render(request, 'inventory/add1.html', context)

@login_required
def add2(request, key):
    categoryObj = Categorie.objects.get(pk=key)
    itemObj = Item.objects.filter(category=categoryObj)
    if request.method == 'POST':
        addItemform = addItemForm(data=request.POST)
        if (addItemform.is_valid()):
            addItemform.save()
            obj = Item.objects.latest('created')
            obj.category = categoryObj
            obj.save()
            if (request.POST['room']):
                pass
            else:
                try:
                     newroom = Room.objects.get(room_name__exact= 'Store')
                     obj.room = newroom
                     obj.save()
                except:
                     newroom = Room.objects.create(floor = Floor.objects.all()[0], room_no = 0, room_name = 'Store')
                     obj.room = newroom
                     obj.save()

            messages.success(request, f'Added Successfully!')
            obj = Item.objects.latest('created')

            return redirect('createSubItem',key=obj.id)

    else:
        addItemform = addItemForm()
    context = {'addItemform': addItemform,'category':categoryObj}
    return render(request, 'inventory/add2.html', context)

@login_required
def addExisting(request, key):
    obj = Item.objects.get(pk=key)
    working = obj.working
    outoforder = obj.out_of_order
    inmaintenance = obj.in_maintenance
    if request.method == 'POST':
        addExistingform = addExistingForm(request.POST)
        if addExistingform.is_valid:
            obj.working += int(request.POST['quantity'])
            obj.save()
            messages.success(request, f'Added Successfully!')
            return redirect('advancedSearch')
    else:
        addExistingform = addExistingForm(request.POST)
    context = {'addExistingform': addExistingform,'item':obj,'working':working,'out_of_order':outoforder,'in_maintenance':inmaintenance}
    return render(request, 'inventory/addExisting.html', context)

@login_required
def allocate(request, key):
    obj = Item.objects.get(pk=key)
    if request.method == 'POST':
        allocateform = allocateForm(request.POST)
        if allocateform.is_valid:
            wk = int(request.POST['working']) if (request.POST['working']) else 0
            oo = int(request.POST['out_of_order']) if (request.POST['out_of_order']) else 0
            im = int(request.POST['in_maintenance']) if (request.POST['in_maintenance']) else 0
            dr = int(request.POST['room'])
            if (dr):
                dr = Room.objects.get(pk=dr)
            if(wk > obj.working or oo > obj.out_of_order or im > obj.in_maintenance or (dr == None)):
                messages.warning(request, f'Error! Enter a valid value')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            else:
                itemDestination = Item.objects.filter(room=dr).filter(
                    name=obj.name).filter(model=obj.model)
                if (itemDestination):
                    itemDestination[0].working += wk
                    itemDestination[0].out_of_order += oo
                    itemDestination[0].in_maintenance += im
                    itemDestination[0].save()
                else:
                    Item.objects.create(category=obj.category, name=obj.name, model=obj.model, working=wk, out_of_order=oo, in_maintenance=im,
                                        date_of_acquire=obj.date_of_acquire, cost_per_item=obj.cost_per_item, room=dr, extra_value=obj.extra_value)
                obj.working -= wk
                obj.in_maintenance -= im
                obj.out_of_order -= oo
                obj.save()
                if (obj.working <= 0 and obj.in_maintenance <= 0 and obj.out_of_order <= 0):
                    obj.delete()
                messages.success(request, f'Allocated Successfully!')
    else:
        allocateform = allocateForm()
    dict ={}
    dict.update({"working":obj.working,"out_of_order":obj.out_of_order,"in_maintenance":obj.in_maintenance,"room":obj.room})
    context = {'allocateform': allocateform}
    context.update(dict)
    return render(request, 'inventory/allocate.html', context)



@login_required
def delete(request,key):
    Item.objects.get(pk=key).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def edit(request,key):
    obj = Item.objects.get(pk=key)
    categoryObj = obj.category
    if request.method == 'POST':
        form = editItemForm(data=request.POST,instance = obj)
        if (form.is_valid):
            form.save()
            # get and modify and save
            to_add = {'working': obj.working, 
            'in_maintenance': obj.in_maintenance,
             'out_of_order': obj.out_of_order,
             'remarks': obj.remarks,
             'verified_by': request.user.username,
             'verification_date': datetime.now().strftime("%Y-%m-%d")}
            
            obj.state['list'].append(to_add)
            obj.save()
            messages.success(request, f'Edit Successful!')
            return redirect('advancedSearch')

    else:
        form = editItemForm(instance = obj)
    context = {'addItemform':form,'item':obj.name}
    return render(request,'inventory/edit.html',context)


@login_required
def createroom(request):
    if request.method == 'POST':
        createRoomform = addRoomForm(request.POST)
        if createRoomform.is_valid:
            try:
                createRoomform.save()
                messages.success(request, f'Room is successfully created!')
            except:
                messages.warning(request, f'Room is either invalid or already available!')
            return redirect('createroom')
    else:
        createRoomform = addRoomForm()
    context = {'createRoomform': createRoomform}
    return render(request,'inventory/createroom.html',context)

@login_required
def createfloor(request):
    if request.method == 'POST':
        createFloorform = addFloorForm(request.POST)
        if createFloorform.is_valid:
            try:
                createFloorform.save()
                messages.success(request, f'Floor is successfully created!')
            except:
                messages.warning(request, f'Floor is either invalid or already available!')

            return redirect('createfloor')
    else:
        createFloorform = addFloorForm()
    context = {'createFloorform': createFloorform}
    return render(request,'inventory/createfloor.html',context)

@login_required
def advancedSearch(request):
    if not Categorie.objects.all().exists():
        return HttpResponse('There is no data in the inventory')
    if request.method == 'POST':
        floorValue = request.POST['floorSelect']
        roomValue = request.POST['roomSelect']
        categoryValue = request.POST['categorySelect']
    else:
        floorValue = 'All'
        roomValue = 'All'
        categoryValue = 'All'
        categoryValue = Categorie.objects.order_by('id')[0].category_name
    print(categoryValue)

    categoryObj = Categorie.objects.all()       #dropdown list for category section
    floorObj = Floor.objects.all()
    if (floorValue == 'All'):
        roomObj = Room.objects.all()
    else:
        tempFloor = Floor.objects.get(floor = floorValue)
        roomObj = Room.objects.filter(floor = tempFloor)

    if (roomValue != 'All'):
        # roomNumber = roomValue.split(':')
        # print(roomValue)
        tempRoomObj = Room.objects.get(room_no = int(roomValue))

        # print(floorValue)

        if (floorValue!='All') and (int(tempRoomObj.floor.floor) != int(floorValue)):
           roomValue = 'All'

    category = Categorie.objects.get(category_name = str(categoryValue))

    itemObj = Item.objects.filter(category = category)

    if (roomValue == 'All'):
        itemTempObj = itemObj
        count=0
        if (not roomObj):
            itemObj = []
        for instance in roomObj:
            if count == 0:
                itemObj = itemTempObj.filter(room = instance)

            else:
                itemObj |= itemTempObj.filter(room = instance)
            count = count+1
    else:
        myroom = Room.objects.get(room_no = int(roomValue))
        itemObj = itemObj.filter(room = myroom)
        print(itemObj)
    if (roomValue!='All'):
        roomValue = int(roomValue)
    if (floorValue!='All'):
        floorValue = int(floorValue)

    if (itemObj):
        tempItem = Item.objects.filter(category = category)[0]

    args = {'roomObj':roomObj, 'categoryObj':categoryObj, 'floorObj':floorObj, 'itemObj':itemObj,'floorValue':floorValue, 'roomValue':roomValue, 'categoryValue':categoryValue,'category':category}
    return render(request,'inventory/advancedSearch.html',args)

@login_required
def downloadCSV(request,key):
    obj = Categorie.objects.get(pk=key)
    itemsObj = Item.objects.filter(category = obj)
    response = HttpResponse(content_type='text/csv')
    response['Inventory-Log'] = 'attachment; filename="inventory.csv"'
    writer = csv.writer(response)
    listOfFields=['Name','Model','Cost per item','Room','Date of acquirement', 'Working', 'Repairable', 'Out of order', 'Created', 'Last Modified']

    writer.writerow(listOfFields)

    for obj in itemsObj:
        valueField = [obj.name,obj.model,obj.cost_per_item,obj.room,obj.date_of_acquire,obj.working,obj.in_maintenance,obj.out_of_order,obj.created,obj.last_modified]
        if (obj.extra_value):
            for key,value in obj.extra_value.items():
                valueField.append(value)

        writer.writerow(valueField)

    return response


@login_required
def chooseCategory(request):
    return render(request,'inventory/chooseCategory.html',{'categoryObj':Categorie.objects.all()})


@login_required
def chooseCategory(request):
    return render(request,'inventory/chooseCategory.html',{'categoryObj':Categorie.objects.all()})

@login_required
def createSubItem(request,key):
    itemObj = Item.objects.get(pk=key)
    itemName = itemObj.name
    if request.method == 'POST':

        form = subItemForm(request.POST)
        if form.is_valid:
            try:

                form.save()
                obj = SubItem.objects.latest('id')
                obj.item = itemObj
                obj.save()
                messages.success(request, f'Sub-item is successfully created!')
            except:
                messages.warning(request, f'Sub-item is either invalid or already available!')
            return redirect('createSubItem',key=key)
    else:
        form = subItemForm()
    context = {'subItemForm': form,'itemName':itemName}
    return render(request,'inventory/createsubItem.html',context)

@login_required
def createCategory(request):
    if request.method == 'POST':
        addCategoryform = addCategoryForm(request.POST)
        if addCategoryform.is_valid():
            Categorie.objects.create(
                category_name=request.POST['categoryName'])
            messages.success(request, f'Category created successfully!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        addCategoryform = addCategoryForm()
    context = {'addCategoryForm': addCategoryform}
    return render(request, 'inventory/addCategory.html', context)


def logoutPrompt(request):
    return render(request,'inventory/logout.html')

@login_required
def settings(request):
    return render(request,'inventory/settings.html')

@login_required
def deletefloor(request):
    if request.method == 'POST':
        try:
           Floor.objects.get(floor = request.POST['floorNumber']).delete()
           messages.success(request, f'Floor deleted successfully!')
        except:
           messages.warning(request, f'Unable to delete the floor!')
        return redirect('deletefloor')
    return render(request,'inventory/deleteFloor.html',{'floorObj':Floor.objects.all()})


@login_required
def showRooms(request):
    return render(request,'inventory/showrooms.html',{'roomObj':Room.objects.all()})

@login_required
def editRoom(request,key):
    obj = Room.objects.get(pk=key)
    if request.method=='POST':
        form = editRoomForm(request.POST,instance=obj)
        if form.is_valid:
            form.save()
            messages.success(request, f'Room updated successfully!')
            return redirect('showRooms')
        else:
            messages.warning(request, f'Invalid input')
    else:
        form = editRoomForm(instance=obj)
    args = {'form':form}
    return render(request,'inventory/editroom.html',args)

@login_required
def deleteRoom(request):
    if request.method == 'POST':
        try:
          print(request.POST['roomNumber'])
          print(Room.objects.get(room_no = request.POST['roomNumber']))
          Room.objects.get(room_no = request.POST['roomNumber']).delete()
          messages.success(request, f'Room deleted successfully!')
        except:
          messages.warning(request, f'Unable to delete the room')
        return redirect('deleteRoom')
    return render(request,'inventory/deleteRoom.html',{'roomObj':Room.objects.all()})

@login_required
def editCategoryView(request,key):
    categoryObj = Categorie.objects.get(pk=key)
    if request.method == 'POST':
        form = editCategoryForm(data=request.POST,instance = categoryObj)
        if (form.is_valid):
            form.save()
            categoryObj.save()
            itemObj = Item.objects.filter(category = categoryObj)
            messages.success(request, f'Edit Successful!')
            return redirect('home')

    else:

        form = editCategoryForm(instance = categoryObj)
    context = {'form':form}
    return render(request,'inventory/editcategory.html',context)

@login_required
def showCategories(request):
    return render(request,'inventory/showCategories.html',{'categoryObj':Categorie.objects.all()})

@login_required
def deleteCategorie(request):
    if request.method == 'POST':
        try:
            Categorie.objects.get(category_name = request.POST['category']).delete()
            messages.success(request, f'Category deleted successfully!')
        except:
            messages.warning(request, f'Unable to delete the category!')
        return redirect('deleteCategory')
    return render(request,'inventory/deleteCategory.html',{'categoryObj':Categorie.objects.all()})

@login_required
def editFloor(request):
    if request.method == 'POST':
        try:
            floorObj = Floor.objects.get(floor = request.POST['oldFloor'])
            floorObj.floor = request.POST['newFloor']
            floorObj.save()
            messages.success(request, f'Floor updated successfully!')
        except:
            messages.warning(request, f'Unable to update the floor!')
        return redirect('editFloor')
    return render(request,'inventory/editFloor.html',{'floorObj':Floor.objects.all()})


@login_required
def editAccount(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account updated for {username}! Login Again')
            return redirect('login')
    else:
        form = UserCreationForm(instance=request.user)
    context = {'form': form}
    return render(request, 'inventory/editAccount.html', context)

@login_required
def homeView(request):
    return render(request,'inventory/home.html')

@login_required
def editSubItem(request,key):
    subItemObj = SubItem.objects.get(pk=key)
    itemObj = Item.objects.get(pk = subItemObj.item.pk)

    if request.method == 'POST':

        form = subItemForm(request.POST,instance=subItemObj)
        if form.is_valid:
            try:
                form.save()
                subItemObj.item = itemObj
                subItemObj.save()
                messages.success(request, f'Sub-item is successfully updated!')
            except:
                messages.warning(request, f'Unable to update sub-item')
            return redirect('advancedSearch')
    else:
        form = subItemForm(instance=subItemObj)
    context = {'subItemForm': form,'subitem':subItemObj.name,'item':itemObj.name}
    return render(request,'inventory/editSubItem.html',context)

@login_required
def addExistingSubItem(request,key):
    subItemObj = SubItem.objects.get(pk=key)
    working = subItemObj.working
    outoforder = subItemObj.out_of_order
    inmaintenance = subItemObj.in_maintenance
    if request.method == 'POST':
        addExistingform = addExistingForm(request.POST)
        if addExistingform.is_valid:
            subItemObj.working += int(request.POST['quantity'])
            subItemObj.save()
            messages.success(request, f'Added Successfully!')
            return redirect('advancedSearch')
    else:
        addExistingform = addExistingForm(request.POST)
    context = {'addExistingform':addExistingform,'subitem':subItemObj,'working':working,'out_of_order':outoforder,'in_maintenance':inmaintenance}
    return render(request,'inventory/addExistingSubItem.html',context)

@login_required
def deleteSubItem(request,key):
    try:
        SubItem.objects.get(pk=key).delete()
        messages.success(request, f'Deleted Successfully!')
    except:
        messages.warning(request, f'Unable to delete sub-item')
    return redirect('advancedSearch')

@login_required
def details(request, key):
    try:
        return render(request,'inventory/details.html',{'itemObj':Item.objects.get(pk=key)})
    except:
        messages.warning(request, f'Unable to find item')
    return redirect('advancedSearch')
