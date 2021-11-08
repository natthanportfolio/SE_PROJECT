from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from ciis_app.models import Authors


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user
        b=request.user.id
    
        if user.is_authenticated:
            t=request.user.user_type
            d = ""
            if t== "3": 
                c=Authors.objects.filter(admin_id=b) 
                d=str(c[0].status)
            if user.user_type == "1":
                if modulename == "ciis_app.AdminViews":
                    pass
                elif modulename == "ciis_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "ciis_app.FinancialViews":
                    pass
                elif modulename == "ciis_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("financial_home"))
            elif user.user_type == "3" and d == "authorthai":
                if modulename == "ciis_app.authorViews":
                    pass
                elif modulename == "ciis_app.views":
                    pass
                
                else:
                    return HttpResponseRedirect(reverse("author_home"))
            elif user.user_type == "3" and d == "authorforeigner":
                if modulename == "ciis_app.authorFViews":
                    pass
                elif modulename == "ciis_app.views":
                    pass
                
                else:
                    return HttpResponseRedirect(reverse("authorf_home"))
            elif user.user_type == "4":
                if modulename == "ciis_app.participantViews":
                    pass
                elif modulename == "ciis_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("participant_home"))
            
            else:
                return HttpResponseRedirect(reverse("show_login"))

        elif modulename == "ciis_app.views":
                    pass

        else:
            if request.path == reverse("show_login") or request.path == reverse("do_login"):
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))