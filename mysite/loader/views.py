from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from extra_views import ModelFormSetView

from loader.forms import UploadFileForm
from loader.tools.logic import save_file
from logs.logger import log_metal


class FileSetLoader(LoginRequiredMixin, ModelFormSetView):
    """ Базовый класс для загрузки и обработки excel файлов"""
    form_class = UploadFileForm
    model = form_class.Meta.model
    local_instance = None     # экземпляр класса от DB_ExcelEntry
    factory_kwargs = {'extra': 1, 'max_num': 5, }
    initial = []

    def get_queryset(self):
        # Возвращаем пустой queryset
        return self.model.objects.none()

    def formset_valid(self, formset):
        """ Обработка формы """
        for form in formset:
            uploaded_files = form.cleaned_data['file_to_upload']
            """ Ловля ошибок здесь нужна только для того что бы редиректить на определённые страницы, если есть надобность """
            try:
                save_file(self, uploaded_files, self.local_instance)     # сюда нужно передавать экземпляр DB_ExcelEntry
            except FileNotFoundError:
                return HttpResponseRedirect(self.request.path)
            except PermissionError:                 # Обработка ошибки, когда нет прав на запись
                log_metal.info(f"Доступ запрещён", exc_info=True)
                return HttpResponseRedirect(self.request.path)
            except Exception:                       # прочие ошибки
                log_metal.info(f"Непредвиденная ошибка", exc_info=True)
                return HttpResponseRedirect(self.request.path)
        return HttpResponseRedirect(self.request.path)


class FileLoader(LoginRequiredMixin, FormView):
    """ Базовый класс для загрузки и обработки excel файлов"""
    form_class = UploadFileForm
    model = form_class.Meta.model
    local_instance = None     # экземпляр класса от DB_ExcelEntry

    def form_valid(self, form):
        """ Обработка формы """
        # for _form in form:
        uploaded_files = form.cleaned_data['file_to_upload']
        print(uploaded_files)
        """ Ловля ошибок здесь нужна только для того что бы редиректить на определённые страницы, если есть надобность """
        try:
            save_file(self, uploaded_files, self.local_instance)     # сюда нужно передавать экземпляр DB_ExcelEntry
        except FileNotFoundError:
            return HttpResponseRedirect(self.request.path)
        except PermissionError:                 # Обработка ошибки, когда нет прав на запись
            log_metal.info(f"Доступ запрещён", exc_info=True)
            return HttpResponseRedirect(self.request.path)
        except Exception:                       # прочие ошибки
            log_metal.info(f"Непредвиденная ошибка", exc_info=True)
            return HttpResponseRedirect(self.request.path)
        return HttpResponseRedirect(self.request.path)
