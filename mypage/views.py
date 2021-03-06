from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.http import HttpResponse


def home(request):
    import sys_function
    tena = sys_function.listTenantsFuntion()
    hd_tena = ['ID', 'Name', 'Enable']
    user = sys_function.listUsersFuntion()
    hd_user = ['ID', 'Name', 'Enable']
    serv = sys_function.listServicesFuntion()
    hd_serv = ['ID', 'Name', 'Type', 'Description']
    endp = sys_function.listEndpointsFuntion()
    hd_endp = ['ID', 'Service ID','InternalURL', 'AdminURL', 'PublicURL']
    role = sys_function.listRolesFuntion()
    hd_role = ['ID', 'Name']
    return render_to_response('index.html', {'tena': tena, 'hd_tena': hd_tena, 'user': user, 'hd_user': hd_user, 'serv': serv, 'hd_serv': hd_serv, 'endp': endp, 'hd_endp': hd_endp, 'role': role, 'hd_role': hd_role })


def performance(request):
    import performance
    import hypervisor
    a = performance.tainguyen()
    lst = a.split()
    hd = ['RAM (total)', 'RAM (use)', 'Storage (total)', 'Storage (use)']
    lst2 = hypervisor.hypervisor()
    hd2 = ['CPU (total)','CPU (use)','RAM (total)', 'RAM (use)','Storage (total)', 'Storage (use)', 'Instances']
    return render_to_response('performance.html',{'hd': hd, 'lst': lst, 'hd2': hd2, 'lst2': lst2})

def instances(request):
    import infomations
    infos = infomations.listServerFuntion()
    name = infomations.getlistTenantsName()
    id_tenant = infomations.getlistIdTenant()
    hd = ['Hostname','ID','Int IP','Image ID','Status','Actions']
    kq = zip(name, infos, id_tenant)
    if request.method == "POST":
        if 'reboot' in request.POST:
            import actions
            instanceid = request.POST['instanceid']
            tenantid = request.POST['tenantid']
            actions.rebootmayao(tenantid,instanceid)
            return redirect(instances)
        elif 'start' in request.POST:
            import actions
            instanceid = request.POST['instanceid']
            tenantid = request.POST['tenantid']
            actions.startmayao(tenantid,instanceid)
            return redirect(instances)
        
        elif 'shutdown' in request.POST:
            import actions
            instanceid = request.POST['instanceid']
            tenantid = request.POST['tenantid']
            actions.shutdownmayao(tenantid,instanceid)
            return redirect(instances)
        elif 'pause' in request.POST:
            import actions
            instanceid = request.POST['instanceid']
            tenantid = request.POST['tenantid']
            actions.pausemayao(tenantid,instanceid)
            return redirect(instances)
        elif 'reboot_tenant' in request.POST:
            import actions
            tenant_id = request.POST['reboot_tenant']
            lst_id_tenant = infomations.getlistIdTenant()
            instances_id = infomations.listIdServerFuntion()
            lst = zip(lst_id_tenant, instances_id)
            for i, j in lst:
                if i == tenant_id:
                    lst_instance = j
                    break
            actions.reboot_tenant(tenant_id,lst_instance)
            return redirect(instances)
        elif 'reboot_all' in request.POST:
            import actions
            lst_id_tenant = infomations.getlistIdTenant()
            instances_id = infomations.listIdServerFuntion()
            lst = zip(lst_id_tenant, instances_id)
            for i,j in lst:
                actions.reboot_tenant(i,j)
            return redirect(instances)
        elif 'start_all' in request.POST:
            import actions
            lst_id_tenant = infomations.getlistIdTenant()
            instances_id = infomations.listIdServerFuntion()
            lst = zip(lst_id_tenant, instances_id)
            for i,j in lst:
                actions.start_tenant(i,j)
            return redirect(instances)
        elif 'shutdown_all' in request.POST:
            import actions
            lst_id_tenant = infomations.getlistIdTenant()
            instances_id = infomations.listIdServerFuntion()
            lst = zip(lst_id_tenant, instances_id)
            for i,j in lst:
                actions.shutdown_tenant(i,j)
            return redirect(instances)
    else:
        return render(request,'instances.html', {'hd': hd, 'kq': kq})

 
def containerss(request):
    import swift_test
    acc_info ,containers = swift_test.account_info()
    hd = ['Name', 'Objects', 'Size']
    if request.method == "POST":
        if 'del_container' in request.POST:
            name = request.POST['del_container']
            swift_test.del_container(name)
            return redirect(containerss)
        elif 'create_con' in request.POST:
            name = request.POST['con_name']
            swift_test.create_container(name)
            return redirect(containerss)
    return render(request,'swift/containers.html', {'hd': hd, 'containers': containers}, context_instance=RequestContext(request))
    
def objects(request):
    import swift_test
    cur_url = request.get_full_path()
    con_name = cur_url.split('/')[-2]
    con_info, objectss = swift_test.container_info(con_name)
    lst_file = []
    for i in objectss:
        a = swift_test.object_info(con_name,i['name'])
        lst_file.append(a['x-object-meta-orig-filename'])
        
    objectsss = zip(objectss, lst_file)
    hd = ['Object Name', 'Object Source', 'Created', 'Size']
    url = request.build_absolute_uri()
    if request.method == "POST":
        if 'del_object' in request.POST:
            name = request.POST['del_object']
            swift_test.del_object(con_name,name) 
            return redirect(url)
        elif 'obj_name' in request.POST:
            name = request.POST['obj_name']
            swift_test.download_object(con_name, name)
            return redirect(url)           
        elif 'upload_obj' in request.POST:
            name = request.POST['object_name']
            f_name = request.FILES['file_name']
            swift_test.upload_object(con_name, name, f_name)
            return redirect(url)
    return render(request,'swift/objects.html', {'hd': hd, 'objects': objectsss, 'con_name': con_name})
    
    
    
    
    
    
    
    
    
    