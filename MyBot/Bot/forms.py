from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django_select2.forms import Select2Widget, Select2TagWidget

from Bot.models import MyUser, OperationUser, CategoryOperation, CardUser, Recipient


class RegisterUserForm(UserCreationForm):
    MALE = 'M'
    FEMALE = 'Ж'
    GENDER_CHOICES = [
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина')
    ]
    username = forms.IntegerField(label='Логин', widget=forms.NumberInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label='Пол')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'first_name', 'last_name', 'gender', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.IntegerField(label='Логин', widget=forms.NumberInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ProfileUpdateForm(forms.ModelForm):
    MALE = 'M'
    FEMALE = 'Ж'
    GENDER_CHOICES = [
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина')
    ]
    username = forms.IntegerField(label='Логин', widget=forms.NumberInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label='Пол')

    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'birth_date']


class AddCardForm(forms.ModelForm):
    class Meta:
        model = CardUser
        fields = ['bank', 'name_card', 'number_card', 'balans_card']


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryOperation
        fields = ['type', 'name_cat']


class AddRecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['name_recipient']


class AddOperationForm(forms.ModelForm):
    class Meta:
        model = OperationUser
        fields = ['card', 'category', 'datetime_amount', 'amount_operation', 'balans', 'note_operation']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Извлечение пользователя
        super().__init__(*args, **kwargs)
        self.query_card = CardUser.objects.filter(telegram_user__telegram_id=user.username)
        if user:
            self.fields['card'] = forms.ModelChoiceField(
                label='Выберите карту списания',
                required=False,
                queryset=self.query_card,
                widget=forms.Select(attrs={'class': 'form-control'}),
                empty_label="Выбрать/добавить карту",
            )
    category = forms.ModelChoiceField(
        label='Выберете категорию операции',
        required=False,
        queryset=CategoryOperation.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Выбрать/добавить категорию",
    )
    datetime_amount = forms.DateTimeField(
        label='Время операции',
        widget=forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'})
    )
    amount_operation = forms.DecimalField(
        label='Сумма по операции',
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-input'})
    )
    balans = forms.DecimalField(
        label='Баланс после операции',
        widget=forms.NumberInput(attrs={'class': 'form-input'})
    )
    recipient = forms.ModelChoiceField(
        label='Выберете получателя',
        required=False,
        queryset=Recipient.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Выбрать/добавить получателя",
    )
    note_operation = forms.CharField(
        label='Описание операции',
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3})
    )

    def clean_amount_operation(self):
        """Валидация суммы операции."""
        amount = self.cleaned_data.get('amount_operation')
        if amount <= 0:
            raise forms.ValidationError("Сумма операции должна быть положительной.")
        return amount
